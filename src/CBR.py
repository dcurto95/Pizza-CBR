# I expect constraints to be a dict
# {'dough': dough,
# 'sauce': [s1, s2, ...],
# 'toppings_must': [t1, t2, ...],
# 'toppings_must_not': [t1, t2, ...]}

DOUGH_WEIGHT = 0.15
SAUCE_WEIGHT = 0.15
TOPPING_WEIGHT = 0.7

INSERTION_WEIGHT = 0.67
DELETION_WEIGHT = 0.33

THRESHOLD_INSERTION = 0.4
MAX_CBY = 39 #MAX ELEMENTS CASE BASE LIBRARY


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

    return DOUGH_WEIGHT*d_dough + SAUCE_WEIGHT*d_sauce + TOPPING_WEIGHT*d_toppings


def pizza_distance_class(pizza, constraints):
    d_dough = dough_distance(pizza.dough, constraints.dough)
    if len(pizza.sauce) > 0 and len(constraints.sauce) > 0:
        d_sauce = sauce_distance(pizza.sauce, constraints.sauce)
    else:
        d_sauce = 1
    d_toppings = topping_distance_class(pizza.toppings, constraints.toppings)

    return DOUGH_WEIGHT*d_dough + SAUCE_WEIGHT*d_sauce + TOPPING_WEIGHT*d_toppings


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
    return INSERTION_WEIGHT*normalized_insertions + DELETION_WEIGHT*normalized_deletions


#TODO: hi ha un altre Jaccard distance (sauce_distance), ho podriem ajuntar?
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
    #TODO: write json
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
        #TODO: in case len(dist_list) > 2
        if dist_list[0][1][j] < dist_list[1][1][j]:
            deletions = case_base[dist_list[0][0]]
            del case_base[dist_list[0][0]]
            break
        elif dist_list[0][1][j] > dist_list[1][1][j]:
            deletions = case_base[dist_list[1][0]]
            del case_base[dist_list[1][0]]
            break

    return case_base, deletions



if __name__ == '__main__':
    import json
    from pizza import Pizza
    with open('../data/pizzas.json', 'r', encoding='utf-8') as f:
        pizzas = json.load(f)

    case_base = [Pizza(pizza['dough'], pizza['sauce'], pizza['toppings'], pizza['recipe'], pizza['name']) for pizza in pizzas]

    constraints = {'dough': 'classic', 'sauce': ['tomato'], 'toppings_must': ['mushroom', 'york', 'black olives'], 'toppings_must_not': ['onion']}

    # RETRIEVE
    result = retrieve(case_base, constraints, k=5)
    for r in result:
        print(r)

    # REUSE

    # REVISE
    distance = revise(case_base, constraints)    #TODO: constraints must be changed by REUSE result

    # RETAIN
    retain(case_base, constraints, distance)    #TODO: constraints must be changed by REUSE result
    #insertion, deletions = retain(case_base, constraints, distance)    #TODO: constraints must be changed by REUSE result

