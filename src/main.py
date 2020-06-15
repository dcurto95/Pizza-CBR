from tkinter import messagebox
import app
from utils import save_case_base

# Saves the case base when the close window button is clicked
def on_closing():

    # Save the case base in the file
    save_case_base(app.case_base)

    # Confirmation message to quit the application
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # Terminates the application
        app.destroy()

# Centers the app in the middle of the screen
def center_app_in_screen(app, frame_width=550, frame_height=600):
    # get screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # calculate position x, y
    x = (screen_width / 2) - (frame_width / 2)
    y = (screen_height / 2.2) - (frame_height / 2)

    # Set the frame dimensions and its position
    app.geometry('%dx%d+%d+%d' % (frame_width, frame_height, x, y))


if __name__ == '__main__':

    # Initialize the application
    app = app.App()
    # Fix the size of the window
    app.resizable(False, False)
    # Center the frame in the middle of the screen
    center_app_in_screen(app)
    # Add the title
    app.title("Pizza recipes CBR ")
    # Add the icon
    app.iconbitmap('logo.ico')
    # Add event listener for window close
    app.protocol("WM_DELETE_WINDOW", on_closing)
    # Execute the main loop
    app.mainloop()
