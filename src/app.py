import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

import CBR
import utils
from pizza_knowledge_base import KnowledgeBase, get_pretty_print


# ##### MAIN APPLICATION #####
class App(Tk):
    def __init__(self, *args, **kwargs):

        # Initialize the Tk
        Tk.__init__(self, *args, **kwargs)

        # Setup and configure the frame
        container = Frame(self, bg="yellow")
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.header_font = 'Helvetica 12 bold'
        self.frames = {}
        self.recommended_pizza = {}
        self.case_base = utils.load_case_base()

        # Add existing frames
        for F in (StartPage, RecipePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.grid_rowconfigure(0, weight=1)  # this needed to be added
            # frame.grid_columnconfigure(0, weight=1)


        # Show the StartPage
        self.show_frame(StartPage)

    # Display the frame given by the context
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    # Validates the user constraints, retrieves the recommended pizza and switches the frame to RecipePage
    def generate_recipe(self, ingredient_listbox, ingredient_discarded_listbox, dough_dropdown, vars, toppings):
        # Retrieve the topping that the user wants
        ingredients_selected = list(ingredient_listbox.curselection())

        # If none selected raise an error message
        if len(ingredients_selected) == 0:
            messagebox.showerror(title="No toppings selected",
                                 message="No toppings selected. You must select at least one")
        else:
            #Retrieve the unwanted toppings
            unwanted_ingredients_selected = list(ingredient_discarded_listbox.curselection())
            S1 = set(ingredients_selected)
            S2 = set(unwanted_ingredients_selected)

            # Check if same topping is in both list, if true raise an error message
            intersection = S1.intersection(S2)
            if len(intersection) > 0:
                messagebox.showerror(title="Same topping in both lists",
                                     message="You have selected the same topping in both lists. "
                                             "Please remove it from one of the lists in order to proceed.")
            else:
                # Retrieve the dough
                dough_selected = dough_dropdown.get()
                toppings_selected = [toppings[i] for i in ingredients_selected]
                toppings_discarded = [toppings[i] for i in unwanted_ingredients_selected]

                #Retrieve the sauces
                sauces_selected = []
                for value, sauce in zip(vars, KnowledgeBase.sauce):
                    if value.get():
                        sauces_selected.append(sauce)

                # Create the constraints dictionary
                constraints = {'dough': dough_selected, 'sauce': sauces_selected, 'toppings_must': toppings_selected,
                               'toppings_must_not': toppings_discarded}

                # Execute the CBR cycle
                self.recommended_pizza = CBR.cbr_cycle(constraints, self.case_base, verbose=True)

                # Navigate to the RecipePage
                self.show_frame(RecipePage)

                # Update the RecipePage with the information of the recommended pizza
                self.frames[RecipePage].update_view(self.recommended_pizza)


# ##### START PAGE (GENERATE RECIPE) #####
class StartPage(Frame):
    def __init__(self, parent, controller):
        # Initialize the frame
        Frame.__init__(self, parent)

        # Get toppings and sort them alphabetically
        toppings = utils.get_toppings()
        toppings.sort()

        # Label Recipe generator
        recipe_creator = Label(self, text="RECIPE GENERATOR", font="Helvetica 14 bold underline")
        recipe_creator.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

        # Label Select ingredients
        ingredients_frame = Frame(self)
        ingredient_label = Label(ingredients_frame, text="Select the must-contain toppings",
                                 font=controller.header_font)
        ingredient_label.grid(row=0, column=0, ipadx=10, ipady=10, sticky="nsew")

        # #Create frame and scrollbar
        ingredients_scroll_frame = Frame(ingredients_frame)
        ingredient_scrollbar = Scrollbar(ingredients_scroll_frame, orient=VERTICAL)
        ingredient_listbox = Listbox(ingredients_scroll_frame, width=30, yscrollcommand=ingredient_scrollbar.set,
                                     selectmode=MULTIPLE, exportselection=False)

        # Configure scrollbar
        ingredient_scrollbar.config(command=ingredient_listbox.yview)
        ingredient_scrollbar.pack(side=RIGHT, fill=Y)
        ingredients_scroll_frame.grid(column=0)
        ingredient_listbox.pack()

        # Insert toppings to the listbox
        for ingredient in toppings:
            ingredient_listbox.insert(END, ingredient)

        ingredients_frame.grid(row=1, column=0, pady=(10, 5))

        # Frame for the dislike toppings
        ingredients_discarded_frame = Frame(self)
        ingredient_discarded_label = Label(ingredients_discarded_frame, text="Select the toppings you dislike",
                                           font=controller.header_font)
        ingredient_discarded_label.grid(row=1, column=0, ipadx=10, ipady=10)

        # #Create frame and scrollbar
        ingredients_discarded_scroll_frame = Frame(ingredients_discarded_frame)
        ingredient_discarded_scrollbar = Scrollbar(ingredients_discarded_scroll_frame, orient=VERTICAL)

        ingredient_discarded_listbox = Listbox(ingredients_discarded_scroll_frame, width=30,
                                               yscrollcommand=ingredient_discarded_scrollbar.set,
                                               selectmode=MULTIPLE, exportselection=False)

        # Configure scrollbar
        ingredient_discarded_scrollbar.config(command=ingredient_discarded_listbox.yview)
        ingredient_discarded_scrollbar.pack(side=RIGHT, fill=Y)
        ingredients_discarded_scroll_frame.grid(column=0)
        ingredient_discarded_listbox.pack()

        # Insert toppings to the listbox
        for ingredient in toppings:
            ingredient_discarded_listbox.insert(END, ingredient)

        ingredients_discarded_frame.grid(row=1, column=1, pady=(10, 5))

        # SAUCES
        sauces_frame = Frame(self)

        # Label select sauces
        sauces_label = Label(sauces_frame, text="Select the sauces you want", font=controller.header_font)
        sauces_label.grid(column=0, row=0, columnspan=2, ipadx=5, ipady=5, pady=(10, 0), sticky="NSEW")

        # Dropdown sauces
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

        sauces_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # Label Select Dough
        dough_label = Label(self, text="Select the dough", font=controller.header_font)
        dough_label.grid(row=3, columnspan=2, pady=(10, 0))

        # Dropdown dough
        dough_types = KnowledgeBase.dough

        dough_dropdown = ttk.Combobox(self, value=dough_types, state="readonly")
        dough_dropdown.current(1)
        dough_dropdown.grid(row=4, columnspan=2, pady=(5, 0))

        # Button generate recipe
        add_btn = Button(self, text="Generate recipe",
                         command=lambda: controller.generate_recipe(ingredient_listbox, ingredient_discarded_listbox,
                                                                    dough_dropdown, vars, toppings))
        add_btn.grid(row=5, columnspan=2, ipadx=5, ipady=5, pady=20)




# ##### RECIPE PAGE (DISPLAYS THE PIZZA RECIPE) #####
class RecipePage(Frame):
    def __init__(self, parent, controller):

        # Initialize the frame
        Frame.__init__(self, parent)
        #Configure the weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize and configure a new frame
        frame = Frame(self)
        frame.pack(side=LEFT, fill=BOTH, expand=True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Initialize the canvas
        self.canvas = Canvas(frame)
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        # Create the recipe frame and add it to the canvas
        recipe_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=recipe_frame, anchor=NW)

        # Create the scrollbar and configure it
        scrollbar = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.config(yscrollcommand=scrollbar.set)
        recipe_frame.bind("<Configure>", self.configure_frame)

        # # Definition of string variable (dynamically updated)
        self.text_dough = StringVar()
        self.text_sauces = StringVar()
        self.text_toppings = StringVar()
        self.steps = StringVar()

        header_font = 'Helvetica 10 bold'

        # Create the recipe label
        recipe_label = Label(recipe_frame, text="RECIPE", font="Helvetica 14 bold underline")
        recipe_label.grid(row=0, column=0, pady=(20, 10))

        # Dough label
        dough_label = Label(recipe_frame, text="Dough", font=header_font)
        dough_label.grid(row=1, column=0)

        # Dough content
        pizza_dough = Label(recipe_frame, textvariable=self.text_dough)
        pizza_dough.grid(row=2, column=0)

        # Sauce label
        sauce_label = Label(recipe_frame, text="Sauces", font=header_font)
        sauce_label.grid(row=3, column=0)

        # Sauce content
        pizza_sauce = Label(recipe_frame, textvariable=self.text_sauces)
        pizza_sauce.grid(row=4, column=0)

        # Toppings label
        toppings_label = Label(recipe_frame, text="Toppings", font=header_font)
        toppings_label.grid(row=5, column=0)

        # Toppings content
        pizza_toppings = Label(recipe_frame, textvariable=self.text_toppings)
        pizza_toppings.grid(row=6, column=0, pady=(0, 20))

        # Preparation label
        steps_label = Label(recipe_frame, text="Preparation", font=controller.header_font)
        steps_label.grid(row=7, column=0)

        # Preparation content
        pizza_steps = Label(recipe_frame, textvariable=self.steps, wraplength=450)
        pizza_steps.grid(row=8, column=0, padx=5, pady=(0,10))

        back_btn = Button(frame, text="Go Back", command=lambda: controller.show_frame(StartPage))
        back_btn.pack(anchor="w")

    def configure_frame(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Updates the RecipePage view given a recommended pizza
    def update_view(self, pizza):

        # Sort sauce and toppings alphabetically
        pizza.sauce.sort()
        pizza.toppings.sort()

        # Modify variables with the content
        self.text_dough.set(pizza.dough)
        self.text_sauces.set('\n'.join(pizza.sauce))
        self.text_toppings.set('\n'.join(pizza.toppings))
        self.steps.set(get_pretty_print(pizza.recipe))
