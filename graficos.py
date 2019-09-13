import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.figure import Figure

class GeraGrafico:
    def __init__(self, figure):
        self.x = []
        self.y = []
        self.position = (0,0)
        self.line = []
        self.click = False
        self.baseline = None

        self.fig = figure

        self.ax1 = self.fig.add_subplot(211)
        self.ax1.axis((0, 300, 0, 250))
        self.ax1.grid()
        self.ax1.set_xticks(np.arange(0, 300, 30))
        self.ax1.set_yticks(np.arange(60, 180, 10))


        self.ax2 = self.fig.add_subplot(212)
        self.ax2.axis((0, 300, 0, 100))
        self.ax2.grid()


        self.annotate = None
        self.count = 1
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)



    def gera_valores(self, x, y, amostras=30 ):
        y1 = [n for n in range(y + amostras, y, -1)]
        y2 = [n for n in range(y, y + amostras + 1)]

        self.x = [n for n in range(x - amostras, x + amostras + 1)]
        self.y = y1 + y2

        return (self.x, self.y)



    def onclick(self, event):
        self.click = True
        if event.inaxes == self.ax1:
            for line, text in zip(self.ax1.lines, self.ax1.texts):
                if int(event.xdata) in line.get_xdata() and int(event.ydata) in line.get_ydata():
                    self.line = line
                    self.annotate = text
                    break

            else:
                x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=1)
                self.position = (int(event.xdata), int(event.ydata))
                self.line = self.ax1.add_line(Line2D(x, y))
                self.annotate = self.ax1.annotate(str(self.count), xy=(event.xdata, event.ydata),
                                                  xytext=(event.xdata + 5, event.ydata + 5))
                self.count += 1
                event.canvas.draw()



        elif event.inaxes == self.ax2:
            for line, text in zip(self.ax2.lines, self.ax2.texts):
                if int(event.xdata) in line.get_xdata() and int(event.ydata) in line.get_ydata():
                    self.line = line
                    self.annotate = text
                    break

            else:
                x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=1)
                self.position = (int(event.xdata), int(event.ydata))
                self.line = self.ax2.add_line(Line2D(x, y))
                self.annotate = self.ax2.annotate(str(self.count), xy=(event.xdata, event.ydata),
                                                  xytext=(event.xdata + 5, event.ydata + 5))
                self.count += 1
                event.canvas.draw()





    def onrelease(self, event):
        self.click = False


    def onmotion(self, event):
        if self.click and event.inaxes == self.ax1:
            x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=1)
            self.line.set_data(x, y)
            self.annotate.set_x(event.xdata + 5)
            self.annotate.set_y(event.ydata + 5)
            event.canvas.draw()

        elif self.click and event.inaxes == self.ax2:
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

            for line, text in zip(self.ax1.lines, self.ax1.texts):
                x, y = min(line.get_xdata()), min(line.get_ydata())
                amostras += np.arange(inicio, x, 1).tolist()
                valores += np.random.randint(y - 20, y + 20, x - inicio).tolist()
                inicio = x

            self.ax1.lines.clear()
            self.ax1.texts.clear()
            self.count = 1

            amostras += np.arange(inicio, 300, 1).tolist()
            valores += np.random.randint(110, 150, 300 - x).tolist()

            self.ax1.plot(amostras, valores, color='green')

            inicio = 0
            amostras = np.arange(inicio, 300, 1).tolist()
            valores = np.full(shape=300, fill_value=20, dtype=np.int).tolist()

            for line, text in zip(self.ax2.lines, self.ax2.texts):
                x, y = min(line.get_xdata()), min(line.get_ydata())
                pico_x = [value for value in range(x - 10, x + 11)]
                pico_y1 = [value for value in range(y - 10, y + 1)]
                pico_y2 = [value for value in range(y, y - 10, -1)]

                for valor_x, valor_y in zip(pico_x, pico_y1 + pico_y2):
                    valores[valor_x] = valor_y


            self.ax2.lines.clear()
            self.ax2.texts.clear()
            self.count = 1

            self.ax2.plot(amostras, valores, color='green')

            event.canvas.draw()

        elif event.key == 'delete':
            self.ax1.lines.clear()
            self.ax1.texts.clear()
            self.ax2.lines.clear()
            self.ax2.texts.clear()
            self.count = 1
            event.canvas.draw()

    def gera_baseline(self, value):
        if self.baseline is None:
            self.baseline = self.ax1.add_line(Line2D(np.arange(0, 300, 1), np.full(shape=300, fill_value=value, dtype=np.int)))

        else:
            try:
                self.baseline.remove()
                self.baseline = self.ax1.add_line(Line2D(np.arange(0, 300, 1), np.full(shape=300, fill_value=value, dtype=np.int)))
            except:
                self.baseline = self.ax1.add_line(Line2D(np.arange(0, 300, 1), np.full(shape=300, fill_value=value, dtype=np.int)))


if '__main__' == __name__:
    gg = GeraGrafico(plt.figure())
