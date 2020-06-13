from collections import defaultdict


class KnowledgeBase:
    sauce = ('tomato', 'steak & grill', 'bourbon barbecue', 'tomato and oregano', 'carbonara', 'creme barbecue',
             'barbecue', 'burger')
    meat = ('sausage', 'marinated chicken', 'york', 'beef', 'pepperoni', 'new orleans pork',
            'quarter pounder', 'bacon crispy', 'bacon', 'chicken pops', 'pulled pork', 'pepperoni', 'mini burger')
    fish = ('tuna', 'prawn', 'anchovy')
    cheese = (
        'goat cheese', 'cheddar cheese', 'provolone cheese', '5 gourmet cheeses', 'mix 4 cheeses', 'cured swiss cheese',
        'mozzarella topping', 'cheddar cheese cream')
    dough = ('thin', 'classic', 'quadroller', '3 floors', 'garlic cheese filled border', 'gluten free')
    after_bake = ('nachos after baking and cut', 'pineapple', 'oregano', 'jamon iberico',
                  'cesar dressing', 'olive oil', 'fresh parmesan cheese')
    vegetable = ('fresh tomato', 'caramelized onion', 'rocket', 'extra candied tomatoe', 'onion', 'green pepper',
                 'roasted pepper', 'black olives', 'mushroom', 'bell pepper')
    # All ingredients in precook must already be in another set
    precook = (
        'caramelized onion', 'roasted pepper', 'marinated chicken', 'beef', 'new orleans pork', 'quarter pounder',
        'bacon crispy', 'chicken pops', 'pulled pork', 'mini burger')

    # cooking_groups = {'sauce': sauce, 'meat': meat, 'fish': fish, 'vegetable': vegetable, 'precook': precook, 'dough': dough, 'after_bake': after_bake, 'cheese': cheese}
    default_recipe_task_order = (
        'extend', 'precook', 'chop', 'spread', 'scatter', 'add_vegetable', 'add_meat', 'add_fish', 'bake',
        'add_after_bake')


# def group_ingredients(ingredients):
#     grouped_ingredients = {k: [] for k in
#                            ['sauce', 'meat', 'fish', 'vegetable', 'precook', 'dough', 'after_bake', 'cheese']}
#
#     for ingredient in ingredients:
#         if ingredient in KnowledgeBase.sauce:
#             grouped_ingredients['sauce'].append(ingredient)
#         if ingredient in KnowledgeBase.meat:
#             grouped_ingredients['meat'].append(ingredient)
#         if ingredient in KnowledgeBase.precook:
#             grouped_ingredients['precook'].append(ingredient)
#         if ingredient in KnowledgeBase.fish:
#             grouped_ingredients['fish'].append(ingredient)
#         if ingredient in KnowledgeBase.cheese:
#             grouped_ingredients['cheese'].append(ingredient)
#         if ingredient in KnowledgeBase.vegetable:
#             grouped_ingredients['vegetable'].append(ingredient)
#         if ingredient in KnowledgeBase.after_bake:
#             grouped_ingredients['after_bake'].append(ingredient)
#         if ingredient in KnowledgeBase.dough:
#             grouped_ingredients['dough'].append(ingredient)
#
#     return grouped_ingredients
#
#
# def get_recipe_from_ingredients(dough, sauces, ingredients):
#     grouped_ingredients = group_ingredients(ingredients)
#
#     chop_ingredients = []
#     chop_ingredients.extend(grouped_ingredients['vegetable'])
#     chop_ingredients.extend(grouped_ingredients['meat'])
#
#     recipe = [("extend", dough),
#               ("precook", grouped_ingredients['cooked_meat']),
#               ("chop", chop_ingredients),
#               ("spread", sauces),
#               ("scatter", grouped_ingredients['cheese']),
#               ("add_vegetable", grouped_ingredients['vegetable']),
#               ("add_meat", grouped_ingredients['meat']),
#               ("add_fish", grouped_ingredients['fish']),
#               ("bake", ["pizza"]),
#               ("add_after_bake", grouped_ingredients['after_bake'])]
#
#     return recipe


def group_toppings(toppings):
    grouped_toppings = defaultdict(list)

    for topping in toppings:
        if topping in KnowledgeBase.meat:
            grouped_toppings['meat'].append(topping)
        if topping in KnowledgeBase.precook:
            grouped_toppings['precook'].append(topping)
        if topping in KnowledgeBase.fish:
            grouped_toppings['fish'].append(topping)
        if topping in KnowledgeBase.cheese:
            grouped_toppings['cheese'].append(topping)
        if topping in KnowledgeBase.vegetable:
            grouped_toppings['vegetable'].append(topping)
        if topping in KnowledgeBase.after_bake:
            grouped_toppings['after_bake'].append(topping)

    return dict(grouped_toppings)


def get_recipe_from_toppings(dough, sauces, toppings):
    grouped_toppings = group_toppings(toppings)

    chop_ingredients = []
    for ing in ['vegetable', 'meat']:
        if ing in grouped_toppings:
            chop_ingredients.extend(grouped_toppings[ing])

    recipe = [('extend', dough)]
    if 'precook' in grouped_toppings:
        recipe.append(('precook', grouped_toppings['precook']))
    if len(chop_ingredients) != 0:
        recipe.append(('chop', chop_ingredients))
    if sauces:
        recipe.append(('spread', sauces))
    if 'cheese' in grouped_toppings:
        recipe.append(('scatter', grouped_toppings['cheese']))
    if 'vegetable' in grouped_toppings:
        recipe.append(('add_vegetable', grouped_toppings['vegetable']))
    if 'meat' in grouped_toppings:
        recipe.append(('add_meat', grouped_toppings['meat']))
    if 'fish' in grouped_toppings:
        recipe.append(('add_fish', grouped_toppings['fish']))
    recipe.append(('bake', ['pizza']))
    if 'after_bake' in grouped_toppings:
        recipe.append(('add_after_bake', grouped_toppings['after_bake']))

    return recipe


def get_toppings_in_same_group(first_group, second_group, must_have_toppings):
    different_groups = []
    matching_groups = []

    for key, value in first_group.items():
        if key not in second_group or set(second_group[key]).issubset(must_have_toppings):
            different_groups.extend(value)
        else:
            matching_groups.extend(value)
    return different_groups, matching_groups


def get_pretty_print(recipe):
    text = []
    for i, task in enumerate(recipe):
        if task[1]:
            if isinstance(task[1], list):
                if len(task[1]) > 1:
                    ingredients_string = ', '.join(task[1][:-1])
                    ingredients_string += ' and ' + task[1][-1]
                elif task[1]:
                    ingredients_string = task[1][0]
            else:
                ingredients_string = task[1]

            if task[0] == 'extend':
                text.append(f'{i+1}. Extend the {ingredients_string} dough on a wide surface.')
            if task[0] == 'precook':
                text.append(f'{i+1}. Precook the {ingredients_string}.')
            if task[0] == 'chop':
                text.append(f'{i+1}. Chop the {ingredients_string}.')
            if task[0] == 'spread':
                text.append(f'{i+1}. Spread the {ingredients_string} on the dough.')
            if task[0] == 'scatter':
                text.append(f'{i+1}. Scatter the {ingredients_string} on the pizza.')
            if task[0] == 'add_vegetable':
                text.append(f'{i+1}. Add the {ingredients_string} over pizza.')
            if task[0] == 'add_meat':
                text.append(f'{i+1}. Add the {ingredients_string} over pizza.')
            if task[0] == 'add_fish':
                text.append(f'{i+1}. Add the {ingredients_string} over pizza.')
            if task[0] == 'bake':
                text.append(f'{i+1}. Bake the pizza at 180ºC for approximately 15 minutes (with the oven preheated).')
            if task[0] == 'add_after_bake':
                text.append(f'{i+1}. Once cooked, add the {ingredients_string}')

    text.append('Enjoy!')
    return '\n'.join(text)
