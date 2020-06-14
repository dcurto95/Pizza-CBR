from tkinter import messagebox

from src import app
from utils import save_case_base


def on_closing():
    save_case_base(app.case_base)

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()


def center_app_in_screen(app, frame_width=550, frame_height=600):
    # get screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    # calculate position x, y
    x = (screen_width / 2) - (frame_width / 2)
    y = (screen_height / 2.2) - (frame_height / 2)
    app.geometry('%dx%d+%d+%d' % (frame_width, frame_height, x, y))


app = app.App()
app.resizable(False, False)
center_app_in_screen(app)
app.title("Pizza recipes CBR ")
app.iconbitmap('logo.ico')
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
