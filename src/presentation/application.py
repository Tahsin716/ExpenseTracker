import tkinter as tk

class Application:

    def __init__(self):
        self.__title = "hello"
        self.__display()

    @staticmethod
    def __display():
        root = tk.Tk()
        root.title("Tkinter Test Window")
        label = tk.Label(root, text="Tkinter is installed!")
        label.pack()
        root.mainloop()



