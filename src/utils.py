import json
from pizza import Pizza
from pizza_knowledge_base import KnowledgeBase


# Loads the case base given a JSON filename
def load_case_base(filename='../data/pizzas.json'):
    # Open the filename in read mode
    with open(filename, 'r', encoding='utf-8') as f:
        # Load the content
        pizzas = json.load(f)

    # Convert the JSON into list of Pizza objects
    case_base = [Pizza(pizza['dough'], pizza['sauce'], pizza['toppings'], pizza['recipe'], pizza['name']) for pizza in
                 pizzas]
    return case_base


# Saves the case base into a file
def save_case_base(case_base, filename='../data/pizzas.json'):
    # Open the file in write mode
    with open(filename, 'w', encoding='utf-8') as f:
        # Write the content
        json.dump(case_base, f, default=lambda obj: obj.__dict__, indent=4)


# Get list of toppings
def get_toppings():
    topping_family = ["meat", "fish", "cheese", "after_bake", "vegetable"]
    toppings = []
    # Retrieve all toppings
    for topping in topping_family:
        value = getattr(KnowledgeBase, topping)
        toppings.extend(value)
    return toppings
