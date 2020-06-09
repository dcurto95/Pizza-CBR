class KnowledgeBase:
    sauce = ['tomato', 'steak & grill', 'bourbon barbecue', 'tomato and oregano', 'carbonara', 'creme barbecue',
             'barbecue', 'burger', 'extra barbecue']
    meat = ['sausage', 'marinated chicken', 'york', 'beef', 'pepperoni', 'new orleans pork',
            'quarter pounder', 'bacon crispy', 'beef', 'bacon', 'chicken pops', 'bacon',
            'pulled pork', 'york', 'pepperoni', 'mini burger']
    fish = ['tuna', 'prawn', 'anchovy']
    cooked_meat = ['marinated chicken', 'beef', 'new orleans pork', 'quarter pounder', 'bacon crispy',
                   'beef', 'chicken pops', 'bacon', 'pulled pork', 'mini burger']
    cheese = ['extra cheese', 'goat cheese', 'cheddar cheese', 'extra mix 5 cheeses',
              'provolone cheese', '5 gourmet cheeses', 'mix 4 cheeses', 'cured swiss cheese',
              'extra mozzarella topping', 'mozzarella topping',
              'cheddar cheese cream']
    dough = ['thin', 'classic', 'quadroller', '3 floors', 'garlic cheese filled border', 'gluten free']
    after_bake = ['nachos after baking and cut', 'pineapple', 'oregano', 'jamon iberico',
                  'cesar dressing', 'olive oil']
    vegetable = ['fresh tomato', 'caramelized onion', 'rocket', 'extra candied tomatoe', 'onion', 'green pepper',
                 'roasted pepper', 'black olives', 'mushroom', 'bell pepper']


def group_ingredients(ingredients):
    grouped_ingredients = {k: [] for k in
                           ['sauce', 'meat', 'fish', 'vegetable', 'cooked_meat', 'dough', 'after_bake', 'cheese']}

    for ingredient in ingredients:
        if ingredient in KnowledgeBase.sauce:
            grouped_ingredients['sauce'].append(ingredient)
        if ingredient in KnowledgeBase.meat:
            grouped_ingredients['meat'].append(ingredient)
        if ingredient in KnowledgeBase.cooked_meat:
            grouped_ingredients['cooked_meat'].append(ingredient)
        if ingredient in KnowledgeBase.fish:
            grouped_ingredients['fish'].append(ingredient)
        if ingredient in KnowledgeBase.cheese:
            grouped_ingredients['cheese'].append(ingredient)
        if ingredient in KnowledgeBase.vegetable:
            grouped_ingredients['vegetable'].append(ingredient)
        if ingredient in KnowledgeBase.after_bake:
            grouped_ingredients['after_bake'].append(ingredient)
        if ingredient in KnowledgeBase.dough:
            grouped_ingredients['dough'].append(ingredient)

    return grouped_ingredients


def get_recipe_from_ingredients(dough, sauces, ingredients):
    grouped_ingredients = group_ingredients(ingredients)

    chop_ingredients = []
    chop_ingredients.extend(grouped_ingredients['vegetable'])
    chop_ingredients.extend(grouped_ingredients['meat'])

    recipe = [("extend", dough),
              ("precook", grouped_ingredients['cooked_meat']),
              ("chop", chop_ingredients),
              ("spread", sauces),
              ("scatter", grouped_ingredients['cheese']),
              ("add_vegetable", grouped_ingredients['vegetable']),
              ("add_meat", grouped_ingredients['meat']),
              ("add_fish", grouped_ingredients['fish']),
              ("bake", ["pizza"]),
              ("add_after_bake", grouped_ingredients['after_bake'])]

    return recipe
