from pizza_knowledge_base import get_recipe_from_toppings


class Pizza:
    def __init__(self, dough, sauce, toppings, recipe, name=''):
        self.name = name
        self.dough = dough
        self.sauce = sauce
        self.toppings = toppings
        self.recipe = recipe

    def add_ingredient(self, topping):
        self.toppings.append(topping)

    def set_name(self, name):
        self.name = name

    def set_recipe(self):
        self.recipe = get_recipe_from_toppings(self.dough, self.sauce, self.toppings)

    def is_topping_in_pizza(self, topping):
        return topping in self.toppings
