from tkinter import *
from tkinter import ttk, messagebox

from src import app


def on_closing():
    #TODO: Aqui anira la funcio d'abans de tancar
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()


app = app.App()
app.title("Pizza recipes CBR ")
app.iconbitmap('logo.ico')
app.geometry("600x600")
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

