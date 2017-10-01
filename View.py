from tkinter import *
import ctypes

class View(Frame):
    def __init__(self, width, height, prosecutor_name, defendant_name):
        super().__init__()
        self.width = width
        self.height = height
        self.master.title("DRBL")
        # Get screen dimensions from OS
        user32 = ctypes.windll.user32
        self.master.geometry("%dx%d+%d+%d" % (
        self.width, self.height, (user32.GetSystemMetrics(0) - width) / 2, (user32.GetSystemMetrics(1) - height) / 2))
        self.create_frames(prosecutor_name, defendant_name)
        self.create_buttons()

    def create_frames(self, prosecutor_name, defendant_name):
        # dialog frame
        self.dialog_frame = Frame(self, width = self.width, height = self.height / 2, relief=RAISED, borderwidth=3)
        self.dialog_frame.pack_propagate(0)
        self.dialogue_content = StringVar()
        Label(self.dialog_frame, text="Dialog viewer", font = ("Helvetica",14), textvariable=self.dialogue_content).pack()
        self.dialog_frame.pack(side=TOP)

        #button frame
        self.button_frame = Frame(self.dialog_frame, width = self.width, height = self.height / 20, relief=RAISED, borderwidth=1)
        self.button_frame.pack_propagate(0)
        self.button_frame.pack(side = BOTTOM, fill = X)

        #Bottom frame
        self.cs_frame = Frame(self, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        self.cs_frame.pack_propagate(0)
        self.cs_frame.pack(side = BOTTOM)


        #First commitment store
        self.cs1_frame = Frame(self.cs_frame, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        #Label(self.cs1_frame, text = prosecutor_name, font = ("Helvetica",14)).pack()
        self.cs1_frame.pack(side=LEFT, expand=True, fill='both')
        #Second commitment store
        self.cs2_frame = Frame(self.cs_frame, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
       # Label(self.cs2_frame, text=defendant_name, font=("Helvetica",14)).pack()
        self.cs2_frame.pack(side=RIGHT, expand=True, fill='both')

        self.pack(fill=BOTH, expand=True)

    def create_buttons(self):
        #run button
        self.run_button = Button(self.button_frame, width = int(self.width / 60) ,text = "Run")
        self.run_button.pack(side = LEFT, fill=X)


