from shutil import copyfile

if __name__ == '__main__':
    copyfile('../data/pizzas_backup.json', '../data/pizzas.json')
