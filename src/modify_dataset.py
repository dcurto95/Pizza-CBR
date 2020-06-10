import json

from pizza import Pizza

if __name__ == '__main__':
    with open('../data/old_pizzas.json', 'r', encoding='utf-8') as f:
        pizzas = json.load(f)

    pizzas = [Pizza(pizza['dough'], pizza['sauce'], pizza['toppings'], pizza['recipe'], pizza['name']) for pizza in pizzas]

    for pizza in pizzas:
        pizza.set_recipe()
    
    with open('../data/pizzas23.json', 'w', encoding='utf-8') as f:
        json.dump(pizzas, f, default=lambda obj: obj.__dict__, indent=4)
