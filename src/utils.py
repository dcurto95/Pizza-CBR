import json
from pizza import Pizza
from pizza_knowledge_base import KnowledgeBase

def load_case_base():
    with open('../data/pizzas.json', 'r', encoding='utf-8') as f:
        pizzas = json.load(f)
    case_base = [Pizza(pizza['dough'], pizza['sauce'], pizza['toppings'], pizza['recipe'], pizza['name']) for pizza in pizzas]
    return case_base


def get_toppings():
    topping_family = ["meat", "fish", "cheese", "after_bake", "vegetable"]
    toppings = []
    for topping in topping_family:
        value = getattr(KnowledgeBase, topping)
        toppings.extend(value)
    return toppings

def get_steps(pizza):
    steps = []

