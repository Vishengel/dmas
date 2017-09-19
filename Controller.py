from tkinter import *
from View import View
from Model import Model

class Controller():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.resizable(False, False)
        self.view = View(width, height)
        self.model = Model()
        self.initButtons()

    def initButtons(self):
        self.start_button = Button(self.view.button_frame, text = "Start simulation", command = self.start_sim)
        self.start_button.pack(side = LEFT, padx = 2)
        #self.next_button = Button(self.view.button_frame, text="Next step")
        #self.next_button.pack(side=LEFT, padx = 2)
        self.entry_field = Entry(self.view.button_frame, width = 7, state = DISABLED)
        self.entry_field.pack(side=LEFT, padx = 2)
        self.confirm_button = Button(self.view.button_frame, state = DISABLED, text = "Steps", command = self.run_sim)
        self.confirm_button.pack(side = LEFT, padx = 2)
        #self.pauze_button = Button(self.view.button_frame, state = DISABLED, text="Pauze")
        #self.pauze_button.pack(side=LEFT, padx = 2)
        self.reset_button = Button(self.view.button_frame, state = DISABLED,  text="Reset")
        self.reset_button.pack(side=LEFT, padx = 2)

    def start_sim(self):
        self.start_button['state'] = 'disabled'
        #Enable all the buttons and start the simulation
        self.entry_field['state'] = 'normal'
        self.entry_field.insert(END, "1")
        self.confirm_button['state'] = 'normal'
        #self.pauze_button['state'] = 'normal'
        self.reset_button['state'] = 'normal'
        self.model.start_simulation()

    def run_sim(self):
        try:
            iterations = int(self.entry_field.get())
            self.model.play(iterations)

        except:
            print("Only integers allowed!")

    def run(self):
        self.root.mainloop()
