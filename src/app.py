from tkinter import *
from tkinter import ttk, messagebox

from CBR import retrieve
from pizza_knowledge_base import KnowledgeBase
from src import utils, CBR

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.header_font = 'Helvetica 12 bold'
        self.frames = {}

        for F in (StartPage, RecipePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def generate_recipe(self, ingredient_listbox, ingredient_discarded_listbox, dough_dropdown, vars, toppings):

        ingredients_selected = list(ingredient_listbox.curselection())
        unwanted_ingredients_selected = list(ingredient_discarded_listbox.curselection())
        dough_selected = dough_dropdown.get()
        toppings_selected = [toppings[i] for i in ingredients_selected]
        toppings_discarded =[toppings[i] for i in unwanted_ingredients_selected]

        sauces_selected = []
        for value, sauce in zip(vars, KnowledgeBase.sauce):
            if value.get():
                sauces_selected.append(sauce)

        constraints = {'dough': dough_selected, 'sauce': sauces_selected, 'toppings_must': toppings_selected,
                       'toppings_must_not': toppings_discarded}

        pizza = CBR.get_adapted_pizza(constraints)

        self.show_frame(RecipePage)





class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        toppings = utils.get_toppings()

        #Label Select ingredients
        ingredients_frame = Frame(self)
        ingredient_label = Label(ingredients_frame, text="Select the ingredients you want", font=controller.header_font)
        ingredient_label.grid(row=0, column=0, ipadx=10, ipady=10)


        # #Create frame and scrollbar
        ingredients_scroll_frame = Frame(ingredients_frame)
        ingredient_scrollbar = Scrollbar(ingredients_scroll_frame, orient=VERTICAL)
        ingredient_listbox = Listbox(ingredients_scroll_frame, width=30, yscrollcommand=ingredient_scrollbar.set, selectmode=MULTIPLE, exportselection=False)

        #Configure scrollbar
        ingredient_scrollbar.config(command=ingredient_listbox.yview)
        ingredient_scrollbar.pack(side=RIGHT, fill=Y)
        ingredients_scroll_frame.grid(column=0)
        ingredient_listbox.pack()

        for ingredient in toppings:
            ingredient_listbox.insert(END, ingredient)

        ingredients_frame.grid(row=0, column=0)

        ingredients_discarded_frame = Frame(self)
        ingredient_discarded_label = Label(ingredients_discarded_frame, text="Select the ingredients you do not want", font=controller.header_font)
        ingredient_discarded_label.grid(row=0, column=0, ipadx=10, ipady=10)


        # #Create frame and scrollbar
        ingredients_discarded_scroll_frame = Frame(ingredients_discarded_frame)
        ingredient_discarded_scrollbar = Scrollbar(ingredients_discarded_scroll_frame, orient=VERTICAL)


        ingredient_discarded_listbox = Listbox(ingredients_discarded_scroll_frame, width=30, yscrollcommand=ingredient_discarded_scrollbar.set, selectmode=MULTIPLE, exportselection=False)


        #Configure scrollbar
        ingredient_discarded_scrollbar.config(command=ingredient_discarded_listbox.yview)
        ingredient_discarded_scrollbar.pack(side=RIGHT, fill=Y)
        ingredients_discarded_scroll_frame.grid(column=0)
        ingredient_discarded_listbox.pack()

        for ingredient in toppings:
            ingredient_discarded_listbox.insert(END, ingredient)

        ingredients_discarded_frame.grid(row=0, column=1)

        #SAUCES
        sauces_frame = Frame(self)

        #Label select sauces
        sauces_label = Label(sauces_frame, text="Select the sauces you want", font=controller.header_font)
        sauces_label.grid(column=0, row=0, columnspan=2, ipadx=5, ipady=5, sticky="NSEW")


        #Dropdown sauces
        sauces = KnowledgeBase.sauce
        counter = 1
        vars = []
        for i, sauce in enumerate(sauces):
            var = IntVar()
            check_btn = Checkbutton(sauces_frame, text=sauce, variable=var)
            vars.append(var)
            if i == 0:
                check_btn.grid(row=counter, column=0, sticky=W)
            elif i % 2:
                check_btn.grid(row=counter, column=0, sticky=W)
            else:
                check_btn.grid(row=counter, column=1, sticky=W)
                counter = counter + 1

        sauces_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        #Label Select Dough
        dough_label = Label(self, text="Select the dough", font=controller.header_font)
        dough_label.grid(row=2, columnspan=2)

        #Dropdown dough
        dough_types = KnowledgeBase.dough

        dough_dropdown = ttk.Combobox(self,value=dough_types, state="readonly")
        dough_dropdown.current(1)
        dough_dropdown.grid(row=3, columnspan=2, pady=10)


        #Button generate recipte
        add_btn = Button(self, text="Generate recipe", command=lambda: controller.generate_recipe(ingredient_listbox, ingredient_discarded_listbox, dough_dropdown, vars, toppings))
        add_btn.grid(row=4, columnspan=2, ipadx=5, ipady=5, pady=20)

        #
        # page_one = Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        # page_one.grid()



class RecipePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        back_btn = Button(self, text="Go Back", command=lambda: controller.show_frame(StartPage))
        back_btn.pack(anchor="w")

        recipe_frame = Frame(self)
        ingredient_label = Label(recipe_frame, text="Ingredients", font=controller.header_font)
        ingredient_label.grid(row=0, column=0, ipadx=10, ipady=10)

        ingredient_label = Label(recipe_frame, text="Step by step", font=controller.header_font)
        ingredient_label.grid(row=2, column=0, ipadx=10, ipady=10)

        recipe_frame.pack()


def on_closing():
    #TODO: Aqui anira la funcio d'abans de tancar
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()
