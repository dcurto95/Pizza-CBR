import json

from pizza_knowledge_base import get_recipe_from_ingredients


class JsonSerializable(object):
    def to_json(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.to_json()


class Pizza(JsonSerializable):
    def __init__(self, name='', dough=[], sauce=[], ingredients=[], recipe=[]):
        self.name = name
        self.dough = dough
        self.sauce = sauce
        self.ingredients = ingredients
        self.recipe = recipe

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def set_name(self, name):
        self.name = name

    def set_recipe(self):
        self.recipe = get_recipe_from_ingredients(self.dough, self.sauce, self.ingredients)

    def is_ingredient_in_pizza(self, ingredient):
        return ingredient in ' '.join(self.ingredients)
