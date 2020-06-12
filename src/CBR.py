# I expect constraints to be a dict
# {'dough': dough,
# 'sauce': [s1, s2, ...],
# 'toppings_must': [t1, t2, ...],
# 'toppings_must_not': [t1, t2, ...]}
import numpy as np

from pizza_knowledge_base import get_recipe_from_toppings, KnowledgeBase, group_toppings, get_toppings_in_same_group
import utils

DOUGH_WEIGHT = 0.15
SAUCE_WEIGHT = 0.15
TOPPING_WEIGHT = 0.7

INSERTION_WEIGHT = 0.67
DELETION_WEIGHT = 0.33

THRESHOLD_INSERTION = 0.4
MAX_CBY = 40  # MAX ELEMENTS CASE BASE LIBRARY


def retrieve(case_base, constraints, k=3):
    k = min(k, len(case_base))
    # Calculate distances
    distances = {}
    for i, pizza in enumerate(case_base):
        d = pizza_distance(pizza, constraints)
        distances[i] = d

    # Rank by distance
    sorted_pizzas = sorted(distances, key=distances.get)  # Petit a gran
    most_similar = [(case_base[sorted_pizzas[i]], distances[sorted_pizzas[i]]) for i in range(k)]
    return most_similar


def pizza_distance(pizza, constraints):
    d_dough = dough_distance(pizza.dough, constraints['dough'])
    d_sauce = sauce_distance(pizza.sauce, constraints['sauce'])
    d_toppings = topping_distance(pizza.toppings, constraints['toppings_must'], constraints['toppings_must_not'])

    return DOUGH_WEIGHT * d_dough + SAUCE_WEIGHT * d_sauce + TOPPING_WEIGHT * d_toppings


def pizza_distance_class(pizza, constraints):
    d_dough = dough_distance(pizza.dough, constraints.dough)
    if len(pizza.sauce) > 0 and len(constraints.sauce) > 0:
        d_sauce = sauce_distance(pizza.sauce, constraints.sauce)
    else:
        d_sauce = 1
    d_toppings = topping_distance_class(pizza.toppings, constraints.toppings)

    return DOUGH_WEIGHT * d_dough + SAUCE_WEIGHT * d_sauce + TOPPING_WEIGHT * d_toppings


def dough_distance(source, target):
    # Hamming distance
    return int(source != target)


# Option 1. We ask for exactly same sauces than query
def sauce_distance(source, target):
    # Jaccard distance
    intersection = set(source).intersection(set(target))
    union = set(source).union(set(target))
    return 1 - len(intersection) / len(union)


# Option 2. We ask for at least sauces in query
def sauce_distance_2(source, target):
    # Intersection over cardinality of target
    intersection = set(source).intersection(set(target))
    return 1 - len(intersection) / len(set(target))


def topping_distance(source, target_must, target_must_not):
    # Edit distance with insertion and deletion
    insertions = len(set(target_must) - set(source))
    normalized_insertions = insertions / len(set(target_must))
    deletions = len(set(target_must_not).intersection(set(source)))
    normalized_deletions = deletions / len(set(target_must_not))
    return INSERTION_WEIGHT * normalized_insertions + DELETION_WEIGHT * normalized_deletions


def adapt(constraints, closest_pizza):
    new_recipe = np.array(closest_pizza.recipe, copy=True)
    actions = new_recipe[:, 0]

    closest_pizza.set_recipe()  # To create new references
    new_ingredients = closest_pizza.toppings.copy()

    topping_deletions, topping_insertions, topping_substitutions = get_delete_insert_substitute_toppings(closest_pizza,
                                                                                                         constraints)

    new_ingredients.extend(topping_insertions)
    new_ingredients = np.asarray(new_ingredients)

    insert_tasks = np.asarray(get_recipe_from_toppings('', [], topping_insertions))
    insert_tasks = insert_tasks[(insert_tasks[:, 0] != 'bake') & (insert_tasks[:, 0] != 'extend')]
    substitute_tasks = np.asarray(get_recipe_from_toppings('', [], topping_substitutions))
    substitute_tasks = substitute_tasks[(substitute_tasks[:, 0] != 'bake') & (substitute_tasks[:, 0] != 'extend')]

    add_tasks_index = [task_tuple[0] not in actions for task_tuple in insert_tasks]

    add_tasks = insert_tasks[add_tasks_index] if add_tasks_index else []
    insert_tasks = insert_tasks[~np.asarray(add_tasks_index)] if add_tasks_index else []

    new_recipe = update_recipe_from_baseline(actions, add_tasks, constraints, insert_tasks, new_ingredients, new_recipe,
                                             substitute_tasks, topping_deletions)

    return Pizza(constraints['dough'], constraints['sauce'], new_ingredients, new_recipe)


def update_recipe_from_baseline(actions, add_tasks, constraints, insert_tasks, new_ingredients, baseline_recipe,
                                substitute_tasks, topping_deletions):
    # Dough and sauce always changed
    baseline_recipe[0][1] = constraints['dough']
    baseline_recipe[actions == 'spread'][0][1] = constraints['sauce']
    # Add new tasks
    if add_tasks.size > 0:
        baseline_recipe = np.append(baseline_recipe, add_tasks, axis=0)
    for task_tuple in baseline_recipe:
        substitute_topping(constraints, new_ingredients, substitute_tasks, task_tuple)
        insert_topping(insert_tasks, task_tuple)
    # Delete toppings
    if topping_deletions:
        baseline_recipe = delete_topping(baseline_recipe, topping_deletions)
    baseline_recipe = [tuple for x in KnowledgeBase.default_recipe_task_order for tuple in baseline_recipe if
                       tuple[0] == x]
    return baseline_recipe


def get_delete_insert_substitute_toppings(closest_pizza, constraints):
    new_toppings = set(constraints['toppings_must']) - set(closest_pizza.toppings)
    new_toppings_group = group_toppings(list(new_toppings))
    closest_toppings_group = group_toppings(closest_pizza.toppings)
    topping_deletions = list(set(constraints['toppings_must_not']).intersection(set(closest_pizza.toppings)))
    topping_insertions, topping_substitutions = get_toppings_in_same_group(new_toppings_group,
                                                                           closest_toppings_group,
                                                                           constraints['toppings_must'])
    return topping_deletions, topping_insertions, topping_substitutions


def substitute_topping(constraints, new_ingredients, substitute_tasks, task_tuple):
    # Substitute toppings
    substitution_index = task_tuple[0] == substitute_tasks[:, 0]
    if any(substitution_index):
        topping_replacements = substitute_tasks[substitution_index][0][1]
        topping_index = [topping not in constraints['toppings_must'] for topping in task_tuple[1]]
        topping_index = np.where(topping_index)[0]
        for index, replacement in zip(topping_index, topping_replacements):
            new_ingredients[new_ingredients == task_tuple[1][index]] = replacement
            task_tuple[1][index] = replacement


def insert_topping(insert_tasks, task_tuple):
    # Insert toppings
    if insert_tasks.size > 0:
        insert_index = task_tuple[0] == insert_tasks[:, 0]
        if any(insert_index):
            task_tuple[1].extend(insert_tasks[insert_index][0][1])


def delete_topping(new_recipe, topping_deletions):
    topping_deletions = set(topping_deletions)
    for i, task_tuple in enumerate(new_recipe):
        found_toppings = topping_deletions.intersection(set(task_tuple[1]))

        if found_toppings:
            if len(task_tuple[1]) == len(found_toppings):
                new_recipe = np.delete(new_recipe, i, 0)
            else:
                task_tuple[1] = [topping for topping in task_tuple[1] if topping not in found_toppings]
    return new_recipe


# TODO: hi ha un altre Jaccard distance (sauce_distance), ho podriem ajuntar?
def topping_distance_class(source, target):
    # Jaccard distance
    intersection = set(source).intersection(set(target))
    union = set(source).union(set(target))
    return 1 - len(intersection) / len(union)


def revise(case_base, suggested_solution):
    # Calculate distances
    distances = []
    for i, pizza in enumerate(case_base):
        d = pizza_distance(pizza, suggested_solution)
        distances.append(d)

    # Select minimum distance
    min_distance = min(distances)
    return min_distance


def retain(case_base, suggested_solution, distance):
    insertion = {}
    if distance > THRESHOLD_INSERTION:
        case_base.append(suggested_solution)
        insertion = suggested_solution
    deletions_list = []
    while len(case_base) > MAX_CBY:
        case_base, deletions = forget(case_base)
        deletions_list.append(deletions)
    # TODO: write json
    return insertion, deletions_list


def forget(case_base):
    dist_list = []
    max_distance = 1
    for i, case in enumerate(case_base):
        distance_row = []
        for case_ in case_base:
            distance_row.append(pizza_distance_class(case, case_))
        sorted_d = sorted(distance_row)

        if sorted_d[1] < max_distance:
            max_distance = sorted_d[1]
            dist_list = []
            dist_list.append((i, sorted_d))
        elif sorted_d[1] == max_distance:
            dist_list.append((i, sorted_d))

    num_case_base = len(case_base)
    for j in range(2, num_case_base):
        # TODO: in case len(dist_list) > 2
        if dist_list[0][1][j] < dist_list[1][1][j]:
            deletions = case_base[dist_list[0][0]]
            del case_base[dist_list[0][0]]
            break
        elif dist_list[0][1][j] > dist_list[1][1][j]:
            deletions = case_base[dist_list[1][0]]
            del case_base[dist_list[1][0]]
            break

    return case_base, deletions

def get_adapted_pizza(constraints):
    casebase = utils.load_case_base()
    result = retrieve(casebase, constraints, k=5)
    closest_case = result[0]
    if closest_case[1] > 0:
        # ADAPT
        adapted_pizza = adapt(constraints, closest_case[0])
        return adapted_pizza
    else:
        return closest_case[0]



if __name__ == '__main__':
    import json
    from pizza import Pizza

    with open('../data/pizzas.json', 'r', encoding='utf-8') as f:
        pizzas = json.load(f)

    case_base = [Pizza(pizza['dough'], pizza['sauce'], pizza['toppings'], pizza['recipe'], pizza['name']) for pizza in
                 pizzas]

    constraints = {'dough': 'classic', 'sauce': ['tomato'], 'toppings_must': ['mushroom', 'york', 'black olives'],
                   'toppings_must_not': ['onion']}

    # RETRIEVE
    result = retrieve(case_base, constraints, k=5)

    closest_case = result[0]
    if closest_case[1] > 0:
        # ADAPT
        adapted_pizza = adapt(constraints, closest_case[0])
        print("Adapted pizza:", adapted_pizza)
    for r in result:
        print(r)

    # REUSE

    # REVISE
    distance = revise(case_base, constraints)  # TODO: constraints must be changed by REUSE result

    # RETAIN
    insertion, deletions = retain(case_base, constraints, distance)  # TODO: constraints must be changed by REUSE result
