import json


class JsonSerializable(object):
    def to_json(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.to_json()


sauce = {'tomato', 'steak & grill', 'bourbon barbecue', 'tomato and oregano', 'carbonara', 'creme barbecue',
         'barbecue', 'burguer', 'extra barbecue'}
meat = {'sausage', 'marinated chicken', 'double york', 'double beef', 'pepperoni', 'new orleans pork',
        'quarter pounder', 'bacon crispy', 'beef', 'bacon', 'chicken pops', 'double bacon',
        'pulled pork', 'york', 'double pepperoni', 'mini burger'}
fish = {'tuna', 'prawn', 'anchovy'}
cooked_meat = {'marinated chicken', 'double beef', 'new orleans pork', 'quarter pounder', 'bacon crispy',
               'beef', 'chicken pops', 'double bacon', 'pulled pork', 'mini burger'}
cheese = {'extra cheese', 'goat cheese', 'cheddar cheese', 'extra mix 5 cheeses',
          'provolone cheese', '5 gourmet cheeses', 'mix 4 cheeses', 'cured swiss cheese',
          'extra mozzarella topping', 'mozzarella topping',
          'cheddar cheese cream'}
dough = {'thin', 'classic', 'quadroller', '3 floors', 'garlic cheese filled border', 'gluten free'}
after_bake = {'nachos after baking and cut', 'pineapple', 'oregano', 'jamon iberico',
              'cesar dressing', 'olive oil'}
vegetable = {'fresh tomato', 'caramelized onion', 'rocket', 'extra candied tomatoe', 'onion', 'green pepper',
             'roasted pepper', 'black olives', 'mushroom', 'bell pepper'}


class Pizza(JsonSerializable):
    def __init__(self, name='', ingredients=None):
        if ingredients is None:
            ingredients = {k: [] for k in
                           ['sauce', 'meat', 'fish', 'vegetable', 'cooked_meat', 'dough', 'after_bake', 'cheese']}

        self.name = name
        self.ingredients = ingredients
        self.recipe = []

    def add_ingredient(self, ingredient):
        if ingredient in sauce:
            self.ingredients['sauce'].append(ingredient)
        if ingredient in meat:
            self.ingredients['meat'].append(ingredient)
        if ingredient in cooked_meat:
            self.ingredients['cooked_meat'].append(ingredient)
        if ingredient in fish:
            self.ingredients['fish'].append(ingredient)
        if ingredient in cheese:
            self.ingredients['cheese'].append(ingredient)
        if ingredient in vegetable:
            self.ingredients['vegetable'].append(ingredient)
        if ingredient in after_bake:
            self.ingredients['after_bake'].append(ingredient)
        if ingredient in dough:
            self.ingredients['dough'].append(ingredient)

    def set_name(self, name):
        self.name = name

    def set_recipe(self):
        self.recipe = [("extend", self.ingredients['dough']),
                       ("precook", self.ingredients['cooked_meat']),
                       ("chop", self.ingredients['vegetable'].extend(self.ingredients['meat'])),
                       ("spread", self.ingredients['sauce']),
                       ("scatter", self.ingredients['cheese']),
                       ("add_vegetable", self.ingredients['vegetable']),
                       ("add_meat", self.ingredients['meat']),
                       ("add_fish", self.ingredients['fish']),
                       ("bake", ["pizza"]),
                       ("add_after_bake", self.ingredients['after_bake'])]
