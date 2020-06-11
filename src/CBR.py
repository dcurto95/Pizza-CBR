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


if __name__ == '__main__':
    import json
    from pizza import Pizza
    with open('../data/pizzas.json', 'r', encoding='utf-8') as f:
        pizzas = json.load(f)

    case_base = [Pizza(pizza['dough'], pizza['sauce'], pizza['toppings'], pizza['recipe'], pizza['name']) for pizza in pizzas]

    constraints = {'dough': 'classic', 'sauce': ['tomato'], 'toppings_must': ['mushroom', 'york', 'black olives'], 'toppings_must_not': ['onion']}

    result = retrieve(case_base, constraints, k=5)
    for r in result:
        print(r)
