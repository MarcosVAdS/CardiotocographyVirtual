from tkinter import *
import matplotlib.pyplot as plt
from graficos import GeraGrafico

class Aplicacao:
    def __init__(self):
        self.root = Tk()
        self.root.title("CTGvirtual")
        self.root.geometry("1280x720")
        self.root["bg"] = ("#5271FF")

        self.home_frame = HomeFrame(master=self.root, controller=self)
        self.config_frame = None
        self.plot_frame = None

        self.actual_frame = self.home_frame
        self.actual_frame.pack()

        self.root.mainloop()


class HomeFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.root = master
        self["bg"] = ("#5271FF")

        self.controller = controller

        self.title = Label(self, text="CTGvirtual")
        self.title["font"] = ("Arial", "100", "bold")
        self.title["bg"] = ("#5271FF")
        self.title.pack(pady=90)

        self.initButton = Button(self, text="INICIAR", width=20)
        self.initButton["font"] = ("Arial", "30")
        self.initButton["width"] = 20
        self.initButton["bg"] = ("white")
        self.initButton["command"] = self.show_config_frame
        self.initButton.pack(pady=40)

        self.tutorialButton = Button(self, text="TUTORIAL")
        self.tutorialButton["font"] = ("Arial", "30")
        self.tutorialButton["width"] = 20
        self.tutorialButton["bg"] = ("white")
        self.tutorialButton.pack(pady=20)

    def show_config_frame(self):
        self.controller.actual_frame.destroy()
        self.controller.actual_frame = ConfigFrame(self.root, self.controller)
        self.controller.actual_frame.pack()

class ConfigFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self["bg"] = ("#5271FF")








if __name__ == '__main__':
    Aplicacao()