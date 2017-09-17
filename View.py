from tkinter import *

class View(Frame):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.master.title("Simulation")
        self.master.geometry("%dx%d+300+300" % (self.width, self.height))
        self.create_frames()

    def create_frames(self):
        # Right frame
        self.dialog_frame = Frame(self, width = self.width / 2, height = self.height / 2, relief=RAISED, borderwidth=3)
        self.dialog_frame.pack_propagate(0)
        Label(self.dialog_frame, text="Dialog viewer", font = ("Helvetica",10)).pack()
        self.dialog_frame.pack(side=RIGHT, fill=Y)
        # Bottom frame
        self.network_viewer = Frame(self, height = self.height / 2, relief = RAISED, borderwidth = 3)
        self.network_viewer.pack_propagate(0)
        Label( self.network_viewer, text = "Bayesian Network viewer", font = ("Helvetica",10)).pack()
        self.network_viewer.pack(side = BOTTOM, fill = X)
        #Left
        self.canvas = Canvas(self)
        self.canvas.configure(background = "black")
        #self.canvas.create_text(180, 40, fill = "white", font = 'Helvetica',text = "Hello world!")
        #self.canvas.update()
        self.canvas.pack(fill= BOTH, expand = 1)
        #Button frame
        self.button_frame = Frame(self.canvas, relief = RAISED, borderwidth = 3)
        self.button_frame.pack(side = BOTTOM, fill = X)
        #Bottom-right frame
        self.evidence_frame = Frame(self.dialog_frame, width = self.width / 2, height = self.height / 2, relief = RAISED, borderwidth = 3)
        self.evidence_frame.pack_propagate(0)
        Label(self.evidence_frame, text = "Evidence and Case viewer", font = ("Helvetica",10)).pack()
        self.evidence_frame.pack(side = BOTTOM)

        self.pack(fill = BOTH, expand = 1)


