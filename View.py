from tkinter import *
import ctypes


class View():

    def __init__(self):
        self.init_UI()

    def init_UI(self):
        top = Tk()
        top.title("DMAS")

        #Get screen dimensions from OS
        user32 = ctypes.windll.user32
        #Center the top window
        w, h = top.winfo_screenwidth() / 2, top.winfo_screenheight() / 1.5
        top.geometry("%dx%d+%d+%d" % (w, h, (user32.GetSystemMetrics(0) - w) / 2, (user32.GetSystemMetrics(1) - h) / 2))

        frame = Frame(top)
        frame.pack(fill=BOTH, expand=True)
        frame.rowconfigure(2, weight=10)

        label = Label(frame, text="Hello World", padx=10, pady=10)
        label.config(font=("Helvetica", 20))
        label.grid(sticky=W)

        area = Text(frame)
        area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)

        help_button = Button(frame, text="Help", width=10)
        help_button.config(font=("Helvetica", 18))
        help_button.grid(sticky=W, row=5, column=0, padx=10, pady=10)

        enter_button = Button(frame, text="Enter", width=10, command= lambda : self.retrieve_input(area))
        enter_button.config(font=("Helvetica", 18))
        enter_button.grid(sticky=E, row=5, column=1, padx=10, pady=10)

        button1 = Button(frame, text="Button 1", width=10)
        button1.config(font=("Helvetica", 18))
        button1.grid(sticky=E+N, row=1, column=2, padx=10, pady=10)

        button2 = Button(frame, text="Button 2", width=10)
        button2.config(font=("Helvetica", 18))
        button2.grid(sticky=E+N, row=2, column=2, padx=10, pady=10)

        top.mainloop()

    def retrieve_input(self, area):
        input = area.get("1.0", END)
        print(input)
        area.delete("1.0", END)