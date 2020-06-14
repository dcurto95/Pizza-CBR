import json

from pizza import Pizza
from pizza_knowledge_base import KnowledgeBase


def load_case_base(filename='../data/pizzas.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        pizzas = json.load(f)
    case_base = [Pizza(pizza['dough'], pizza['sauce'], pizza['toppings'], pizza['recipe'], pizza['name']) for pizza in
                 pizzas]
    return case_base


def save_case_base(case_base, filename='../data/pizzas.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(case_base, f, default=lambda obj: obj.__dict__, indent=4)


def get_toppings():
    topping_family = ["meat", "fish", "cheese", "after_bake", "vegetable"]
    toppings = []
    for topping in topping_family:
        value = getattr(KnowledgeBase, topping)
        toppings.extend(value)
    return toppings
