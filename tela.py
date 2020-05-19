from tkinter import Tk, Frame, Label, Button, BOTH, StringVar, TOP, Canvas, RIGHT, LEFT, Entry
import matplotlib.pyplot as plt
from graficos import GeraGrafico
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from PIL import ImageTk, Image

class Aplicacao:
    def __init__(self):
        self.root = Tk()
        self.root.title("CTGvirtual")
        self.root.geometry("1280x720")
        self.root["bg"] = ("#5271FF")
        self.root.protocol('WM_DELETE_WINDOW', self.root.quit)

        self.home_frame = HomeFrame(master=self.root, controller=self)
        self.config_frame = ConfigFrame(master=self.root, controller=self)
        self.plot_frame = PlotFrame(master=self.root, controller=self)
        self.tutorial_frame = TutorialFrame(master=self.root, controller=self)

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
        self.tutorialButton["command"] = self.show_tutorial_frame
        self.tutorialButton.pack(pady=20)


    def show_config_frame(self):
        self.controller.actual_frame.pack_forget()
        self.controller.actual_frame = self.controller.config_frame
        self.controller.actual_frame.show_plot_frame()

    def show_tutorial_frame(self):
        self.controller.actual_frame.pack_forget()
        self.controller.actual_frame = self.controller.tutorial_frame
        self.controller.actual_frame.pack(fill=BOTH, expand=1)


class ConfigFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.root = master
        self.controller = controller
        self["bg"] = ("#5271FF")


        self.text = Label(self, text='Configurações')
        self.text.pack()

        self.avancar = Button(self, text='Avançar')
        self.avancar["command"] = self.show_plot_frame
        self.avancar["width"] = 20
        self.avancar.pack(side=LEFT, padx=100, pady=300)

        self.voltar = Button(self, text='Voltar')
        self.voltar["command"] = self.show_home_frame
        self.voltar["width"] = 20
        self.voltar.pack(side=LEFT, padx=10, pady=300)

    def show_home_frame(self):
        self.controller.actual_frame.pack_forget()
        self.controller.actual_frame = self.controller.home_frame
        self.controller.actual_frame.pack(fill=BOTH, expand=1)

    def show_plot_frame(self):
        self.controller.actual_frame.pack_forget()
        self.controller.actual_frame = self.controller.plot_frame
        self.controller.actual_frame.pack(fill=BOTH, expand=1)

class PlotFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.root = master
        self.controller = controller

        self["bg"] = ("#5271FF")

        self.graficos = GeraGrafico(plt.figure())
        self.canvas = FigureCanvasTkAgg(self.graficos.fig, master=self)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.canvas.mpl_connect('button_press_event', self.graficos.onclick)
        self.bind("<Button-1>", self.graficos.onclick)

        self.canvas.mpl_connect('button_release_event', self.graficos.onrelease)
        self.bind("<ButtonRelease-1>", self.graficos.onrelease)

        self.canvas.mpl_connect('motion_notify_event', self.graficos.onmotion)
        self.bind("<Motion>", self.graficos.onmotion)

        self.canvas.mpl_connect('key_press_event', self.graficos.key_press)
        self.bind("<Key>", self.graficos.key_press)

        b = StringVar(self, value='120')
        self.baseline = Entry(self, textvariable=b)

        self.baseline_button = Button(self, text="Plotar Linha de Base", width=20)
        self.baseline_button["command"] = self.calc_baseline


        v = StringVar(self, value='2')
        self.entry_variability = Entry(self, textvariable=v)

        self.variability_button = Button(self, text="Variância", width=20)
        self.variability_button["command"] = self.give_variability

        self.voltar_button = Button(self, text="Voltar", width=20)
        self.voltar_button["command"] = self.show_home_frame

        self.canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        self.baseline_button.pack(side=RIGHT, padx=10, pady=10)
        self.baseline.pack(side=RIGHT, padx=10, pady=10)        
        self.variability_button.pack(side=RIGHT, padx=10, pady=10)
        self.entry_variability.pack(side=RIGHT, padx=10, pady=10)
        self.voltar_button.pack(side=LEFT, padx=10, pady=10)

    def give_variability(self):
        value_variability = int(self.entry_variability.get())
        self.graficos.variability = value_variability
        

    def calc_baseline(self):
        value = int(self.baseline.get())
        self.graficos.gera_baseline(value)
        self.canvas.get_tk_widget().focus_force()
        self.canvas.draw()

    def show_home_frame(self):
        self.controller.actual_frame.pack_forget()
        self.controller.actual_frame = self.controller.home_frame
        self.controller.actual_frame.pack(fill=BOTH, expand=1)

class TutorialFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.root = master
        self.controller = controller
        self["bg"] = ("#5271FF")

        #image = Image.open("../images/tela_de_plot.JPG")
        #photo = ImageTk.PhotoImage(image)

        #self.canvas = Canvas(self, width=image.width, height=image.height)
        #self.canvas.create_image(0, 0, image=photo)
        #self.canvas.pack()





