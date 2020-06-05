import json

if __name__ == '__main__':
    data_file = open('../data/pizzas.json', 'r', encoding='utf-8')
    pizza_list = json.load(data_file)
    # TODO passar llista de diccionaris al format que volguem (o deixar aixi)
