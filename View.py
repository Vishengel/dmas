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
        # Right frame
        self.dialog_frame = Frame(self, width = self.width, height = self.height / 2, relief=RAISED, borderwidth=3)
        self.dialog_frame.pack_propagate(0)
        Label(self.dialog_frame, text="Dialog viewer", font = ("Helvetica",14)).pack()
        self.dialog_frame.pack(side=TOP)

        #Bottom-right frame
        self.cs_frame = Frame(self, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        self.cs_frame.pack_propagate(0)
        self.cs_frame.pack(side = BOTTOM)

        #First commitment store
        self.cs1_frame = Frame(self.cs_frame, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        Label(self.cs1_frame, text = "p", font = ("Helvetica",14)).pack()
        self.cs1_frame.pack(side=LEFT, expand=True, fill='both')
        #Second commitment store
        self.cs2_frame = Frame(self.cs_frame, width = self.width, height = self.height / 2, relief = RAISED, borderwidth = 3)
        Label(self.cs2_frame, text="d", font=("Helvetica",14)).pack()
        self.cs2_frame.pack(side=RIGHT, expand=True, fill='both')

        self.pack(fill=BOTH, expand=True)

    def draw_agents(self, agents):
        #Draw agents on screen, each with their own identifying tag
        for i in range(len(agents)):
            self.canvas.create_oval(agents[i].x, agents[i].y, agents[i].x + self.width / 20, agents[i].y + self.width / 20, tag = i, fill = "red")
        self.canvas.itemconfigure(len(agents), fill = "blue")
        #self.canvas.create_rectangle(agents[i-1].x, agents[-1].y, agents[-1].x + 30, agents[-1].y + 30, tag = len(agents) - 1, fill = "blue")

    def move_agent(self, agent_tag, dx, dy):
        self.canvas.move(agent_tag,dx,dy)


