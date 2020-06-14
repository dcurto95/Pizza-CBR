from random import shuffle

import numpy as np

from pizza import Pizza
from pizza_knowledge_base import get_recipe_from_toppings, KnowledgeBase, group_toppings, get_toppings_in_same_group


# ##### S Y S T E M   P A R A M E T E R S #####
DOUGH_WEIGHT = 0.15
SAUCE_WEIGHT = 0.15
TOPPING_WEIGHT = 0.7

INSERTION_WEIGHT = 0.67
DELETION_WEIGHT = 0.33

THRESHOLD_INSERTION = 0.4
MAX_CBY = 50  # MAX ELEMENTS CASE BASE LIBRARY
MAX_INGREDIENTS = 7


# ##### D I S T A N C E S #####

# Distance for retrieval (between a pizza and user constraints)
def pizza_distance_constraints(pizza, constraints):
    d_dough = dough_distance(pizza.dough, constraints['dough'])
    d_sauce = sauce_distance(pizza.sauce, constraints['sauce'])
    d_toppings = topping_distance_constraints(pizza.toppings, constraints['toppings_must'], constraints['toppings_must_not'])

    return DOUGH_WEIGHT * d_dough + SAUCE_WEIGHT * d_sauce + TOPPING_WEIGHT * d_toppings


# Distance for learning (between two already-created pizzas)
def pizza_distance(pizza_1, pizza_2):
    d_dough = dough_distance(pizza_1.dough, pizza_2.dough)
    d_sauce = sauce_distance(pizza_1.sauce, pizza_2.sauce)
    d_toppings = topping_distance(pizza_1.toppings, pizza_2.toppings)

    return DOUGH_WEIGHT * d_dough + SAUCE_WEIGHT * d_sauce + TOPPING_WEIGHT * d_toppings


# Hamming or discrete Manhattan distance for dough comparison
def dough_distance(source, target):
    return int(source != target)


# Jaccard distance for sauce comparison
def sauce_distance(source, target):
    return jaccard_distance(source, target)


# Modified edit distance with insertion and deletion counts for topping comparison in retrieval (using must and must_not lists)
def topping_distance_constraints(source, target_must, target_must_not):
    insertions = len(set(target_must) - set(source))
    normalized_insertions = insertions / len(set(target_must))  # Forced to have len > 0 in GUI
    deletions = len(set(target_must_not).intersection(set(source)))
    normalized_deletions = deletions / (len(set(target_must_not)) + 1e-10)
    return INSERTION_WEIGHT * normalized_insertions + DELETION_WEIGHT * normalized_deletions


# Jaccard distance for topping comparison between two already-created pizzaes
def topping_distance(toppings_1, toppings_2):
    return jaccard_distance(toppings_1, toppings_2)


# Jaccard distance implementation
def jaccard_distance(set_1, set_2):
    intersection = set(set_1).intersection(set(set_2))
    union = set(set_1).union(set(set_2))
    if len(union) == 0:  # Special case where both are empty sets
        return 0
    return 1 - len(intersection) / len(union)


# ##### R E T R I E V E #####

# Main retrieve function, returns k pairs of (pizza, distance) for closest pizzas to user constraints
def retrieve(case_base, constraints, k=3):
    k = min(k, len(case_base))

    # Calculate distances
    distances = {}
    for i, pizza in enumerate(case_base):
        d = pizza_distance_constraints(pizza, constraints)
        distances[i] = d

    # Rank by distance
    distances_list = list(distances.items())
    shuffle(distances_list)  # Shuffle to randomly breack ties between pizzas with same distance
    sorted_pizzas = sorted(distances_list, key=lambda x: x[1])  # Sort by distance, low to high
    sorted_pizzas = np.asarray(sorted_pizzas, dtype=np.int32)[:, 0]  # Take the idx
    most_similar = [(case_base[sorted_pizzas[i]], distances[sorted_pizzas[i]]) for i in range(k)]
    return most_similar


# ##### A D A P T #####

# Aux functions

def update_recipe_from_baseline(actions, add_tasks, constraints, insert_tasks, new_ingredients, baseline_recipe,
                                substitute_tasks, topping_deletions):
    # Dough and sauce always changed
    baseline_recipe[0][1] = constraints['dough']
    sauce_index = actions == 'spread'
    sauce_index = np.argmax(sauce_index)
    baseline_recipe[sauce_index][1] = constraints['sauce']

    # Add new tasks
    if add_tasks.size > 0:
        baseline_recipe = np.append(baseline_recipe, add_tasks, axis=0)

    # Substitute and insert new toppings in the existing recipe
    for task_tuple in baseline_recipe:
        new_ingredients = substitute_topping(constraints, new_ingredients, substitute_tasks, task_tuple)
        insert_topping(insert_tasks, task_tuple)

    # Delete toppings
    if topping_deletions:
        baseline_recipe = delete_topping(baseline_recipe, topping_deletions)
        new_ingredients = [topping for topping in new_ingredients if topping not in topping_deletions]
    # Sort the recipe based on knowledge base template
    baseline_recipe = [tuple.tolist() for x in KnowledgeBase.default_recipe_task_order for tuple in baseline_recipe if
                       tuple[0] == x]
    return baseline_recipe, new_ingredients


def get_delete_insert_substitute_toppings(closest_pizza, constraints):
    # Obtain the toppings which are not in the closest pizza
    new_toppings = set(constraints['toppings_must']) - set(closest_pizza.toppings)

    # Group the toppings using the knowledge base
    new_toppings_group = group_toppings(list(new_toppings))
    closest_toppings_group = group_toppings(closest_pizza.toppings)

    # Split the toppings in three lists based on how they affect the final recipe
    topping_deletions = list(set(constraints['toppings_must_not']).intersection(set(closest_pizza.toppings)))
    topping_insertions, topping_substitutions = get_toppings_in_same_group(new_toppings_group,
                                                                           closest_toppings_group,
                                                                           constraints['toppings_must'])
    return topping_deletions, topping_insertions, topping_substitutions


def substitute_topping(constraints, new_ingredients, substitute_tasks, task_tuple):
    # Substitute toppings
    # Find the tasks to edit
    substitution_index = task_tuple[0] == substitute_tasks[:, 0]
    if any(substitution_index):
        # Find which toppings are replaceable
        topping_replacements = substitute_tasks[substitution_index][0][1]
        topping_index = [topping not in constraints['toppings_must'] for topping in task_tuple[1]]
        topping_index = np.where(topping_index)[0]
        # Replace them
        for index, replacement in zip(topping_index, topping_replacements):
            new_ingredients[new_ingredients == task_tuple[1][index]] = replacement
            task_tuple[1][index] = replacement
        # If there are toppings left but none can be changed add them to the list
        if len(topping_replacements) > len(topping_index):
            for replacement in topping_replacements[len(topping_index):]:
                task_tuple[1].append(replacement)
                new_ingredients = np.append(new_ingredients, replacement)
    return new_ingredients


def insert_topping(insert_tasks, task_tuple):
    # Append toppings to the exising steps of the recipe
    if insert_tasks.size > 0:
        # Find the tasks to edit
        insert_index = task_tuple[0] == insert_tasks[:, 0]
        if any(insert_index):
            task_tuple[1].extend(insert_tasks[insert_index][0][1])


def delete_topping(new_recipe, topping_deletions):
    topping_deletions = set(topping_deletions)
    deleted = 0
    for i, task_tuple in enumerate(new_recipe):
        # Find toppings to delete
        found_toppings = topping_deletions.intersection(set(task_tuple[1]))
        if found_toppings:
            if len(task_tuple[1]) == len(found_toppings):
                # If all toppings from task are deleted delete the task
                new_recipe = np.delete(new_recipe, i - deleted, 0)
                deleted += 1
            else:
                # Delete specific toppings
                task_tuple[1] = [topping for topping in task_tuple[1] if topping not in found_toppings]
    return new_recipe


# Main adapt function. Takes the retrieved pizza and the set of constraints by the user. Returns an adapted pizza and recipe.
def adapt(constraints, closest_pizza):
    new_recipe = np.array(closest_pizza.recipe, copy=True)
    actions = new_recipe[:, 0]

    closest_pizza.set_recipe()  # To create new references
    new_ingredients = closest_pizza.toppings.copy()

    # Obtain the topping differences separated by task
    topping_deletions, topping_insertions, topping_substitutions = get_delete_insert_substitute_toppings(closest_pizza,
                                                                                                         constraints)
    # Update the ingredients list of the adapted pizza
    new_ingredients.extend(topping_insertions)
    new_ingredients = np.asarray(new_ingredients)

    # Obtain the steps for each list of toppings
    insert_tasks = np.asarray(get_recipe_from_toppings('', [], topping_insertions))
    insert_tasks = insert_tasks[(insert_tasks[:, 0] != 'bake') & (insert_tasks[:, 0] != 'extend')]
    substitute_tasks = np.asarray(get_recipe_from_toppings('', [], topping_substitutions))
    substitute_tasks = substitute_tasks[(substitute_tasks[:, 0] != 'bake') & (substitute_tasks[:, 0] != 'extend')]

    # Split the topping insertions by new steps in the recipes and appending toppings in existing steps
    add_tasks_index = [task_tuple[0] not in actions for task_tuple in insert_tasks]
    add_tasks = insert_tasks[add_tasks_index] if add_tasks_index else np.array([])
    insert_tasks = insert_tasks[~np.asarray(add_tasks_index)] if add_tasks_index else np.array([])

    # Create the recipe
    new_recipe, new_ingredients = update_recipe_from_baseline(actions, add_tasks, constraints, insert_tasks,
                                                              new_ingredients, new_recipe,
                                                              substitute_tasks, topping_deletions)
    if not isinstance(new_ingredients, list):
        new_ingredients = new_ingredients.tolist()
    new_ingredients = list(set(new_ingredients))
    return Pizza(constraints['dough'], constraints['sauce'], new_ingredients, new_recipe)


# ##### L E A R N #####

# Add suggested pizza to the case base under certain circumstances
def learn(case_base, suggested_solution, closest_case):
    insertion = None
    # Calculate distances
    distance = pizza_distance(closest_case, suggested_solution)
    if distance > THRESHOLD_INSERTION and len(suggested_solution.toppings) <= MAX_INGREDIENTS:
        case_base.append(suggested_solution)
        insertion = suggested_solution
    deletions_list = []
    while len(case_base) > MAX_CBY:
        case_base, deletion = forget(case_base)
        deletions_list.append(deletion)
    return insertion, deletions_list


# Removes the least useful case in the case library
def forget(case_base):
    deletion = None

    # Store at each row the distance of a case to all the others, sorted (first column will have the minimums)
    matrix_distance = np.zeros([len(case_base), len(case_base)])
    for i, case in enumerate(case_base):
        distance_row = []
        for case_ in case_base:
            distance_row.append(pizza_distance(case, case_))
        matrix_distance[i, :] = sorted(distance_row)

    # Navigate through columns to break ties
    indices = np.arange(matrix_distance.shape[0])
    for j in range(1, len(case_base)):  # Start at 1 to avoid 0-distances between itself
        where_min_dist = np.where(matrix_distance[:, j] == np.min(matrix_distance[indices, j]))[0]
        indices = np.setdiff1d(indices, where_min_dist)

        # indices = np.array(list(
        #     set(np.where(matrix_distance[:, j] == min(matrix_distance[indices, j]))[0]).intersection(set(indices))))

        if len(indices) == 1:
            deletion = case_base[indices[0]]
            del case_base[indices[0]]
            break

    # If all had the same distances, remove a random one
    if deletion is None:
        rnd_idx = np.random.randint(len(indices))
        deletion = case_base[indices[rnd_idx]]
        del case_base[indices[rnd_idx]]

    return case_base, deletion


# ##### M A I N   C B R   C Y C L E #####

def cbr_cycle(constraints, case_base, verbose=False):
    # Retrieve
    result = retrieve(case_base, constraints, k=1)
    closest_case, closest_dist = result[0]

    if verbose:
        print('*** R E T R I E V E ***')
        print('Case that best matches constraints: {}, with distance = {:.3f}'.format(closest_case, closest_dist))

    # Adapt if needed
    if closest_dist > 0:
        adapted_case = adapt(constraints, closest_case)

        if verbose:
            print('*** A D A P T ***')
            print('Adapted pizza: {}'.format(adapted_case))
    else:
        adapted_case = closest_case

    # Evaluate
    pass

    # Learn
    insertion, deletions_list = learn(case_base, adapted_case, closest_case)
    if verbose:
        print('*** L E A R N ***')
        if insertion is None:
            print('The adapted pizza was NOT learned in the case library')
        else:
            print('The adapted pizza was learned to the case library. {} cases have been removed'.format(len(deletions_list)))
        print('\n\n')

    return adapted_case
