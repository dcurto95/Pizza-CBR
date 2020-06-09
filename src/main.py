from tkinter import *
from tkinter import ttk

from pizza_knowledge_base import KnowledgeBase

def select_ingredient():
    result = ""
    for ingredient in ingredient_listbox.curselection():
        result = result + str(ingredient_listbox.get(ingredient))
    print(result)


root = Tk()
root.title("Pizza recipes CBR ")
root.iconbitmap('logo.ico')
root.geometry("600x600")

#Label Select ingredients
ingredient_label = Label(root, text="Select the ingredients you want")
ingredient_label.pack()

#Create frame and scrollbar
ingredient_frame = Frame(root)
ingredient_scrollbar = Scrollbar(ingredient_frame, orient=VERTICAL)


ingredient_listbox = Listbox(ingredient_frame, width=50, yscrollcommand=ingredient_scrollbar.set, selectmode=MULTIPLE)

#Configure scrollbar
ingredient_scrollbar.config(command=ingredient_listbox.yview)
ingredient_scrollbar.pack(side=RIGHT, fill=Y)
ingredient_frame.pack()
ingredient_listbox.pack(pady=5)

#Insert ingredients
ingredients= ['chicken', 'bacon', 'egg', 'tomato', 'cheese','sausage', 'chile','olives','tuna','sausage','pineapple','onion','cucumber']

for ingredient in ingredients:
    ingredient_listbox.insert(END, ingredient)

#Button add ingredient
add_btn = Button(root, text="Add ingredient", command=select_ingredient)
add_btn.pack(pady=5)


#Label select sauces
sauces_label = Label(root, text="Select the sauce")
sauces_label.pack()


#Dropdown sauces
sauces = KnowledgeBase.sauce

for sauce in sauces:
    check_btn = Checkbutton(root, text=sauce)
    check_btn.pack()

#Label Select Dough
dough_label = Label(root, text="Select the dough")
dough_label.pack()

#Dropdown dough
dough_types = KnowledgeBase.dough

dough_dropdown = ttk.Combobox(root,value=dough_types, state="readonly")
dough_dropdown.current(1)
dough_dropdown.pack()

root.mainloop()