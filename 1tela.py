from tkinter import *
import matplotlib.pyplot as plt
from graficos import GeraGrafico

class Aplicacao:
    def __init__(self, master=None):
        self.title = Label(root, text="CTGvirtual")
        self.title["font"] = ("Arial", "100", "bold")
        self.title["bg"] = ("#5271FF")
        self.title.pack(side="top", expand=1)
        self.initButton = Button(root, text="INICIAR")
        self.initButton["font"] = ("Arial", "30")
        self.initButton["width"] = 20
        self.initButton["bg"] = ("white")
        self.initButton["command"] = self.plot
        self.initButton.pack()
        self.tutorialButton = Button(root, text="TUTORIAL")
        self.tutorialButton["font"] = ("Arial", "30")
        self.tutorialButton["width"] = 20
        self.tutorialButton["bg"] = ("white")
        self.tutorialButton.pack(side="bottom", expand=1)

    def plot(self):
        '''
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']
        valores = [105235, 107697, 110256, 109236, 108859, 109986]


        plt.plot(meses,valores)
        plt.show()
        '''





        GeraGrafico(plt)

root = Tk()
root.title("CTGvirtual")
root.geometry("1280x720")
root["bg"] = ("#5271FF")
Aplicacao(root)
root.mainloop()
