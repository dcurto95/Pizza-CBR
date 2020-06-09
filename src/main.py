import json

import numpy as np

from pizza import Pizza

if __name__ == '__main__':
    data_file = open('../data/pizzas.json', 'r', encoding='utf-8')
    pizza_list = json.load(data_file)
    data_file.close()

    pizza_list = [Pizza(name=pizza['name'], dough=pizza['dough'], sauce=pizza['sauce'],
                        ingredients=pizza['ingredients'], recipe=pizza['recipe']) for pizza in pizza_list]

    print("Hi welcome to MAI-pizza!")
    ingredients = input("What ingredients do you like? (splitted by , )\n")
    ingredients_list = ingredients.lower().split(',')

    pizza_votes = np.zeros(len(pizza_list))
    for ingredient in ingredients_list:
        for i, pizza in enumerate(pizza_list):
            pizza_votes[i] += 1 if pizza.is_ingredient_in_pizza(ingredient) else 0
    print("Best pizza:")
    print(pizza_list[np.argmax(pizza_votes)])
