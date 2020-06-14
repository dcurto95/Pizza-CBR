from utils import load_case_base, save_case_base

if __name__ == '__main__':
    pizzas = load_case_base(filename='../data/pizzas_backup.json')

    for pizza in pizzas:
        # Apply modifications
        pizza.set_recipe()

    save_case_base(pizzas)
