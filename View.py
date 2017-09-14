from tkinter import *

class View(Frame):
    def __init__(self, width, height):
        super().__init__()
        self.master.title("Simulation")
        self.master.geometry("%dx%d+300+300" % (width, height))
        self.create_frames()

    def create_frames(self):
        # Right frame
        self.dialog_frame = Frame(self, width = 200, height = 100, relief=RAISED, borderwidth=3)
        self.dialog_frame.pack_propagate(0)
        Label(self.dialog_frame, text="Dialog viewer").pack()
        self.dialog_frame.pack(side=RIGHT, fill=Y)
        # Bottom frame
        self.network_viewer = Frame(self, height = 200, relief = RAISED, borderwidth = 3)
        self.network_viewer.pack_propagate(0)
        Label( self.network_viewer, text = "Bayesian Network viewer").pack()
        self.network_viewer.pack(side = BOTTOM, fill = X)
        #Left
        self.canvas = Canvas(self)
        self.canvas.configure(background = "black")
        self.canvas.create_text(180, 40, fill = "white", font = 'Helvetica',text = "Hello world!")
        #self.canvas.update()
        self.canvas.pack(fill= BOTH)
        #Bottom-right frame
        self.evidence_frame = Frame(self.dialog_frame, height = 200, width = 200, relief = RAISED, borderwidth = 3)
        self.evidence_frame.pack_propagate(0)
        Label(self.evidence_frame, text = "Evidence and Case viewer").pack()
        self.evidence_frame.pack(side = BOTTOM)

        self.pack(expand = 1)


