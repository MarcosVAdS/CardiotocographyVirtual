import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

class GeraGrafico:
    def __init__(self, plt):
        self.x = []
        self.y = []
        self.position = (0,0)
        self.line = []
        self.click = False

        self.fig, self.ax = plt.subplots()
        self.ax.axis((0, 300, 0, 250))
        self.ax.grid()
        self.annotate = None
        self.count = 1
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)

        plt.yticks(np.arange(60, 180, 10))
        plt.xticks(np.arange(0, 300, 30))
        plt.show()


    def gera_valores(self, x, y, amostras=30 ):
        y1 = [n for n in range(y + amostras, y, -1)]
        y2 = [n for n in range(y, y + amostras + 1)]

        self.x = [n for n in range(x - amostras, x + amostras + 1)]
        self.y = y1 + y2

        return (self.x, self.y)



    def onclick(self, event):
        self.click = True

        for line, text in zip(self.ax.lines, self.ax.texts):
            if int(event.xdata) in line.get_xdata() and int(event.ydata) in line.get_ydata():
                self.line = line
                self.annotate = text
                break

        else:
            x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=1)
            self.position = (int(event.xdata), int(event.ydata))
            self.line = self.ax.add_line(Line2D(x, y))
            self.annotate = self.ax.annotate(str(self.count), xy=(event.xdata, event.ydata), xytext=(event.xdata + 5, event.ydata + 5))
            self.count += 1
            event.canvas.draw()



    def onrelease(self, event):
        self.click = False


    def onmotion(self, event):
        if self.click:
            x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=1)
            self.line.set_data(x, y)
            self.annotate.set_x(event.xdata + 5)
            self.annotate.set_y(event.ydata + 5)
            event.canvas.draw()


    def key_press(self, event):
        if event.key == 'enter':
            inicio = 0
            amostras = []
            valores = []


            for line, text in zip(self.ax.lines, self.ax.texts):
                print(line.get_label(), line.get_color(), text.get_text())
                x, y = min(line.get_xdata()), min(line.get_ydata())
                print(len(amostras))
                print(len(valores))
                amostras += np.arange(inicio, x, 1).tolist()
                valores += np.random.randint(y - 20, y + 20, x - inicio).tolist()
                inicio = x

            self.ax.lines.clear()
            self.ax.texts.clear()
            self.count = 1

            amostras += np.arange(inicio, 300, 1).tolist()
            valores += np.random.randint(110, 150, 300 - x).tolist()

            print(len(amostras))
            print(len(valores))
            self.ax.plot(amostras, valores, color='green')

            event.canvas.draw()

        elif event.key == 'delete':
            self.ax.lines.clear()
            self.ax.texts.clear()
            self.count = 1
            event.canvas.draw()


if '__main__' == __name__:
    gg = GeraGrafico(plt)
