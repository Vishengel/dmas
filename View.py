from tkinter import *
import ctypes

class View(Frame):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.master.title("Simulation")
        # Get screen dimensions from OS
        user32 = ctypes.windll.user32
        self.master.geometry("%dx%d+%d+%d" % (
        self.width, self.height, (user32.GetSystemMetrics(0) - width) / 2, (user32.GetSystemMetrics(1) - height) / 2))
        self.create_frames()

    def create_frames(self):
        #Top frame
        self.dialog_frame = Frame(self, width = self.width, height = self.height / 2, relief=RAISED, borderwidth=3)
        self.dialog_frame.pack_propagate(0)
        self.dialogue_view = StringVar()
        Label(self.dialog_frame, font = ("Helvetica",14), textvariable=self.dialogue_view).pack()
        self.dialog_frame.pack(side=TOP)

        #Bottom frame
        self.cs_frame = Frame(self, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        self.cs_frame.pack_propagate(0)
        self.cs_frame.pack(side = BOTTOM)

        #First commitment store
        self.cs1_frame = Frame(self.cs_frame, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        Label(self.cs1_frame, text = "Prosecutor", font = ("Helvetica",14)).pack()
        self.cs1_frame.pack(side=LEFT, expand=True, fill='both')
        #Second commitment store
        self.cs2_frame = Frame(self.cs_frame, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        Label(self.cs2_frame, text="Defendant", font=("Helvetica",14)).pack()
        self.cs2_frame.pack(side=RIGHT, expand=True, fill='both')

        self.pack(fill=BOTH, expand=True)


