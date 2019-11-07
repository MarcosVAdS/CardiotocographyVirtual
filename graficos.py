import math
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.figure import Figure

class GeraGrafico:
    def __init__(self, figure):
        self.line = None
        self.click = False
        self.baseline = None

        self.duration = 600
        self.variability = 10

        self.fig = figure

        self.ax1 = self.fig.add_subplot(211, adjustable='box')
        self.ax1.axis((0, self.duration, 40, 200))
        self.ax1.grid()
        self.ax1.set_xticks(np.arange(0, self.duration, 30))
        self.ax1.get_xaxis().set_ticklabels([num for num in range(0, 22)])
        self.ax1.set_yticks(np.arange(60, 200, 10))
        self.ax1.set_title('Frequência cardíaca fetal')
        self.ax1.set_ylabel('bpm')


        self.ax2 = self.fig.add_subplot(212, adjustable='box')
        self.ax2.axis((0, self.duration, 0, 100))
        self.ax2.grid()
        self.ax2.set_xticks(np.arange(0, self.duration, 30))
        self.ax2.get_xaxis().set_ticklabels([num for num in range(0, 22)])
        self.ax2.set_yticks(np.arange(0, 100, 10))
        self.ax2.set_title('Contrações uterinas')
        self.ax2.set_xlabel('Tempo [min]')
        self.ax2.set_ylabel('a.u.')

        self.annotate = None
        self.count = 1
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)

        self.rad = 10

    def gera_valores(self, x, y, amostras=30 ):
        y1 = [n for n in range(y + amostras, y, -1)]
        y2 = [n for n in range(y, y + amostras + 1)]
        x = [n for n in range(x - amostras, x + amostras + 1)]

        return (x, y1 + y2)

    def onclick(self, event):
        self.click = True
        if event.inaxes == self.ax1:
            for line, text in zip(self.ax1.lines, self.ax1.texts):
                contem, art = line.contains(event)
                if contem:
                    line.set_picker(self.rad)
                    line.set_pickradius(self.rad)
                    self.line = line
                    self.annotate = text
                    break

            else:
                x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=0)
                self.line = self.ax1.add_line(Line2D(x, y, marker="o"))

                self.line.set_picker(self.rad)
                self.line.set_pickradius(self.rad)
                self.annotate = self.ax1.annotate(str(self.count), xy=(event.xdata, event.ydata),
                                                          xytext=(event.xdata + 5, event.ydata + 5))
                self.count += 1
                event.canvas.draw()

        elif event.inaxes == self.ax2:
            for line, text in zip(self.ax2.lines, self.ax2.texts):
                contem, art = line.contains(event)
                if contem:
                    line.set_picker(self.rad)
                    line.set_pickradius(self.rad)
                    self.line = line
                    self.annotate = text
                    break

            else:
                x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=0)
                self.line = self.ax2.add_line(Line2D(x, y, marker="o"))
                self.line.set_picker(self.rad)
                self.line.set_pickradius(self.rad)
                self.annotate = self.ax2.annotate(str(self.count), xy=(event.xdata, event.ydata),
                                                  xytext=(event.xdata + 5, event.ydata + 5))
                self.count += 1
                event.canvas.draw()

    def onrelease(self, event):
        self.click = False

    def onmotion(self, event):
        if self.click and event.inaxes == self.ax1 and self.line is not None:
            for line, text in zip(self.ax1.lines, self.ax1.texts):
                contem, art = line.contains(event)
                if contem:
                    x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=0)
                    line.set_data(x, y)
                    text.set_x(event.xdata + 5)
                    text.set_y(event.ydata + 5)
                    event.canvas.draw()
                    return

        elif self.click and event.inaxes == self.ax2 and self.line is not None:
            for line, text in zip(self.ax2.lines, self.ax2.texts):
                contem, art = line.contains(event)
                if contem:
                    x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=0)
                    line.set_data(x, y)
                    text.set_x(event.xdata + 5)
                    text.set_y(event.ydata + 5)
                    event.canvas.draw()
                    return

    def key_press(self, event):
        if event.key == 'enter':
            # gera para o grafico de batimemntos
            inicio_x = 0
            inicio_y = 120
            amostras = []
            valores = []

            for line, text in zip(self.ax1.lines, self.ax1.texts):
                x, y = min(line.get_xdata()), min(line.get_ydata())
                amostras += np.arange(inicio_x, x, 1).tolist()
                valores += [v + r for v, r in zip(np.linspace(inicio_y, y, x - inicio_x).tolist(),
                                                  np.random.randint(-self.variability, self.variability,
                                                                    x - inicio_x).tolist())]

                inicio_x = x
                inicio_y = y

            self.ax1.lines.clear()
            self.ax1.texts.clear()
            self.count = 1

            amostras += np.arange(inicio_x, self.duration, 1).tolist()
            valores += [v + r for v, r in zip(np.linspace(inicio_y, 120, self.duration - inicio_x).tolist(),
                                              np.random.randint(-self.variability, self.variability,
                                                                self.duration - inicio_x).tolist())]

            print(len(amostras))
            print(len(valores))

            self.ax1.plot(amostras, valores, color='green')

            #gera para o grafico de contração
            inicio = 0
            amostras = []
            valores = []

            scale = 20            #curvatura da parte superior
            factor = 2.5 * scale  #regulação da amplitude


            for line, text in zip(self.ax2.lines, self.ax2.texts):
                x, y = min(line.get_xdata()), min(line.get_ydata())
                plot_x = np.linspace(x - 80, x + 80, 1000)
                plot_y = stats.norm.pdf(plot_x, x, scale) * y * factor

                amostras.append(plot_x)
                valores.append(plot_y)


            self.ax2.lines.clear()
            self.ax2.texts.clear()
            self.count = 1

            for amostra, valor in zip(amostras, valores):
                self.ax2.plot(amostra, valor, color='green')


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
            self.baseline = self.ax1.add_line(Line2D(np.arange(0, self.duration, 1), np.full(shape=self.duration, fill_value=value, dtype=np.int)))

        else:
            try:
                self.baseline.remove()
                self.baseline = self.ax1.add_line(Line2D(np.arange(0, self.duration, 1), np.full(shape=self.duration, fill_value=value, dtype=np.int)))
            except:
                self.baseline = self.ax1.add_line(Line2D(np.arange(0, self.duration, 1), np.full(shape=self.duration, fill_value=value, dtype=np.int)))


if '__main__' == __name__:
    gg = GeraGrafico(plt.figure())
