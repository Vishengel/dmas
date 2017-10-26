from tkinter import *
import ctypes


class View(Frame):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.master.title("DRBL")
        # Get screen dimensions from OS
        user32 = ctypes.windll.user32
        self.master.geometry("%dx%d+%d+%d" % (
            self.width, self.height, (user32.GetSystemMetrics(0) - width) / 2,
            (user32.GetSystemMetrics(1) - height) / 2))
        #self.width = 1500
        #self.height = 780
        self.create_frames()
        self.create_buttons()



    def create_frames(self):
        #top screen, contains both dialog frames
        self.main_frame = Frame(self, width=self.width / 2, height=self.height / 2, relief=RAISED, borderwidth=3)
        self.main_frame.pack_propagate(0)
        self.main_frame.pack(side=TOP, fill=BOTH)
        self.main_frame.grid_propagate(False)

        # dialog frame
        self.dialog_frame = Frame(self.main_frame, width=self.width/2, height=self.height / 2, relief=RAISED, borderwidth=3)
        self.dialog_frame.pack_propagate(0)
        self.dialog_frame.pack(fill = BOTH)
        self.dialog_frame.grid_propagate(False)

        # natural language frame
        self.language_frame = Frame(self.main_frame, width=self.width/2, height=self.height / 2, relief=RAISED, borderwidth=3)
        self.language_frame.pack_propagate(0)
        #self.language_frame.pack(side=RIGHT)
        self.language_frame.grid_propagate(False)

        # implement stretchability
        self.dialog_frame.grid_rowconfigure(0, weight=1)
        self.dialog_frame.grid_columnconfigure(0, weight=1)

        self.language_frame.grid_rowconfigure(0, weight=1)
        self.language_frame.grid_columnconfigure(0, weight=1)


         # button frame
        self.button_frame = Frame(self, width=self.width, height=self.height / 10, relief=RAISED,
                                  borderwidth=13)
        self.button_frame.pack_propagate(0)
        self.button_frame.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.button_frame.grid_rowconfigure(1, weight=1)


        # Bottom frame
        self.cs_frame = Frame(self, width=self.width, height=self.height / 2.5, relief=RAISED, borderwidth=3)
        self.cs_frame.pack_propagate(0)
        self.cs_frame.pack(side=BOTTOM)
        self.cs_frame.grid_rowconfigure(2, weight=1)

        # Create entry field
        self.entry = Entry(self.button_frame)
        self.entry.pack(side=LEFT)
        self.entry.insert(0, 1)

        # First commitment store
        self.cs1_frame = Frame(self.cs_frame, width=self.width, height=self.height / 2, relief=RAISED, borderwidth=3)

        # Second commitment store
        self.cs2_frame = Frame(self.cs_frame, width=self.width, height=self.height / 2, relief=RAISED, borderwidth=3)

        # create the dialogue text widget
        self.dialogue_text = Text(self.dialog_frame, borderwidth=3, relief="sunken")
        self.dialogue_text.config(font=("Helvetica", 12), undo=True, wrap='word')
        self.dialogue_text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.natural_text = Text(self.language_frame, borderwidth=3, relief="sunken")
        self.natural_text.config(font=("consolas", 12), undo=True, wrap='word')
        self.natural_text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        dialogue_sb = Scrollbar(self.dialog_frame, command=self.dialogue_text.yview)
        dialogue_sb.grid(row=0, column=1, sticky='nsew')
        self.dialogue_text['yscrollcommand'] = dialogue_sb.set

        self.natural_text['yscrollcommand'] = dialogue_sb.set



        p_name = Label(self.cs1_frame, text="Prosecutor", font=("Helvetica", 14))
        p_name.grid(row=0, column=0, columnspan=2)

        d_name = Label(self.cs2_frame, text="Defendant", font=("Helvetica", 14))
        d_name.grid(row=0, column=0)

        # create commitment store text widgets
        self.cs1_text = Text(self.cs1_frame, borderwidth=3, relief="sunken")
        self.cs1_text.config(font=("Helvetica", 12), undo=True, wrap='word')
        self.cs1_text.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        self.cs1_text.grid_columnconfigure(1, weight=1)

        # create a Scrollbar and associate it with txt
        cs1_sb = Scrollbar(self.cs1_frame, command=self.cs1_text.yview, highlightbackground="red", highlightcolor="red", highlightthickness=3)
        cs1_sb.grid(row=1, column=1, sticky='nsew')
        self.cs1_text['yscrollcommand'] = cs1_sb.set

        # create commitment store text widgets
        self.cs2_text = Text(self.cs2_frame, borderwidth=3, relief="sunken")
        self.cs2_text.config(font=("Helvetica", 12), undo=True, wrap='word')
        self.cs2_text.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)


        # create a Scrollbar and associate it with txt
        cs2_sb = Scrollbar(self.cs2_frame, command=self.cs2_text.yview)
        cs2_sb.grid(row=1, column=1, sticky='nsew')
        self.cs2_text['yscrollcommand'] = cs2_sb.set

        # self.dialog_frame.configure(background='black')

        """background_image = PhotoImage(file="courtroom.gif")
        label = Label(self.dialog_frame, image=background_image)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.image = background_image"""

        self.cs1_frame.pack(side=LEFT, expand=True, fill='both')
        self.cs2_frame.pack(side=RIGHT, expand=True, fill='both')
        self.pack(fill=BOTH, expand=True)


    def create_buttons(self):
        # run button
        self.run_button = Button(self.button_frame, width=int(self.width / 60), text="Next move", padx=5)
        self.run_button.pack(side=LEFT, fill=X)

        # reset button
        self.reset_button = Button(self.button_frame, width=int(self.width / 60), text="Reset", padx=5)
        self.reset_button.pack(side=LEFT, fill=X)
