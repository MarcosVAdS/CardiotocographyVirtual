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
        self.baseline_value = 120

        self.duration = 600
        self.variability = 2
        self.bpm = 120

        self.fig = figure

        self.ax1 = self.fig.add_subplot(211, adjustable='box')
        self.ax1.axis((0, self.duration, 40, 201))
        self.ax1.grid(color='red')
        self.ax1.set_xticks(np.arange(0, self.duration, 30))
        self.ax1.get_xaxis().set_ticklabels([num for num in range(0, 22)])
        self.ax1.set_yticks(np.arange(60, 200, 10))
        self.ax1.set_title('Frequência cardíaca fetal')
        self.ax1.set_ylabel('bpm')


        self.ax2 = self.fig.add_subplot(212, adjustable='box')
        self.ax2.axis((0, self.duration, 0, 100))
        self.ax2.grid(color='red')
        self.ax2.set_xticks(np.arange(0, self.duration, 30))
        self.ax2.get_xaxis().set_ticklabels([num for num in range(0, 22)])
        self.ax2.set_yticks(np.arange(0, 100, 10))
        self.ax2.set_title('Contrações uterinas')
        self.ax2.set_xlabel('Milímetros [mm]')
        self.ax2.set_ylabel('a.u.')

        self.annotate = None
        self.count = 1
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)

        self.rad = 3

        self.remove_points = []
        self.remove_texts = []

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
                self.line = self.ax1.add_line(Line2D(x, y, marker="."))

                self.line.set_picker(self.rad)
                self.line.set_pickradius(self.rad)
                self.annotate = self.ax1.annotate(str(self.count), xy=(event.xdata, event.ydata),
                                                          xytext=(event.xdata + 5, event.ydata + 5), alpha=0)
                self.count += 1

                self.remove_points.append(self.line)
                self.remove_texts.append(self.annotate)

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
                                                  xytext=(event.xdata + 3, event.ydata + 3), alpha=0)
                self.count += 1

                self.remove_points.append(self.line)
                self.remove_texts.append(self.annotate)

                event.canvas.draw()

    def onrelease(self, event):
        self.click = False

    def onmotion(self, event):
        if hasattr(event, 'inaxes') and event.inaxes == self.ax1:
            minutes = int((event.xdata / 30))
            seconds = ((event.xdata / 30) % 1) * 60 / 100
            self.position = self.ax1.annotate(f'({minutes + seconds:.2f},{int(event.ydata)})', xy=(event.xdata, event.ydata),
                              xytext=(event.xdata, event.ydata))
            event.canvas.draw()
            self.position.remove()

        if hasattr(event, 'inaxes') and event.inaxes == self.ax2:
            minutes = int((event.xdata / 30))
            seconds = ((event.xdata / 30) % 1) * 60 / 100
            self.position = self.ax2.annotate(f'({minutes + seconds:.2f},{int(event.ydata)})', xy=(event.xdata, event.ydata),
                              xytext=(event.xdata, event.ydata))
            event.canvas.draw()
            self.position.remove()



        if self.click and event.inaxes == self.ax1 and self.line is not None:
            for line, text in zip(self.ax1.lines, self.ax1.texts):
                contem, art = line.contains(event)
                if contem:
                    x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=0)
                    line.set_data(x, y)
                    text.set_x(event.xdata + 5)
                    text.set_y(event.ydata + 5)
                    event.canvas.draw()
                    self.position.remove()


        elif self.click and event.inaxes == self.ax2 and self.line is not None:
            for line, text in zip(self.ax2.lines, self.ax2.texts):
                contem, art = line.contains(event)
                if contem:
                    x, y = self.gera_valores(int(event.xdata), int(event.ydata), amostras=0)
                    line.set_data(x, y)
                    text.set_x(event.xdata + 5)
                    text.set_y(event.ydata + 5)
                    event.canvas.draw()




    def key_press(self, event):

        if event.key == 'enter':
            # gera para o grafico de batimemntos
            if not self.baseline:
                pass

            else:
                inicio_x = 0
                inicio_y = self.baseline_value

                valores = []

                for line, text in zip(self.ax1.lines, self.ax1.texts):
                    x, y = min(line.get_xdata()), min(line.get_ydata())
                    valores += np.linspace(inicio_y, y, int(self.bpm * (x - inicio_x) / 30)).tolist()


                    inicio_x = x
                    inicio_y = y
                    print(len(valores))

                self.ax1.lines.clear()
                self.ax1.texts.clear()
                self.count = 1

                valores += np.linspace(inicio_y, self.baseline_value, int(self.bpm * (self.duration - inicio_x) / 30)).tolist()
                amostras = np.linspace(0, self.duration, len(valores)).tolist()
                variabilidades = np.random.randint(-self.variability, self.variability, len(valores)).tolist()

                valores = [v + r for v, r in zip(valores, variabilidades)]

                print(len(amostras))
                print(len(valores))
                print(len(variabilidades))

                self.ax1.plot(amostras, valores, color='green', linewidth=0.5)
                self.ax1.add_line(self.baseline)


                #gera para o grafico de contração
                inicio = 0
                amostras = []
                valores = []

                scale = 20            #curvatura da parte superior
                factor = 2.5 * scale  #regulação da amplitude


                for line, text in zip(self.ax2.lines, self.ax2.texts):
                    x, y = min(line.get_xdata()), min(line.get_ydata())
                    plot_x = np.linspace(x - 65, x + 65, 300)
                    plot_y = stats.norm.pdf(plot_x, x, scale) * y * factor

                    amostras.append(plot_x)
                    valores.append(plot_y)


                self.ax2.lines.clear()
                self.ax2.texts.clear()
                self.count = 1

                # for pos in range(len(amostras) - 1):
                #     atual = amostras[pos]
                #     proxima = amostras[pos + 1]
                #     menor = min(proxima)
                #     maior = max(atual)
                #     media = int((maior+menor)/2)
                #     atual_index = 0
                #     proxima_index = 0
                #
                #
                #     for x in range(len(atual)):
                #         if atual[x] > media:
                #             atual_index = x
                #             break
                #
                #     for x in range(len(proxima)):
                #         if proxima[x] > media:
                #             proxima_index = x
                #             break
                #
                #
                #     amostras[pos] = np.delete(amostras[pos], [valor for valor in range(atual_index, len(amostras[pos]))])
                #     valores[pos] = np.delete(valores[pos], [valor for valor in range(atual_index, len(valores[pos]))])
                #     self.ax2.plot(amostras[pos], valores[pos], color='green')
                #
                #     amostras[pos + 1] = np.delete(amostras[pos + 1], [valor for valor in range(proxima_index)])
                #     valores[pos + 1] = np.delete(valores[pos + 1], [valor for valor in range(proxima_index)])
                #     self.ax2.plot(amostras[pos + 1], valores[pos + 1], color='green')
                #
                # self.ax2.plot(amostras[len(amostras) - 1], valores[len(valores) - 1], color='green')


                for amostra, valor in zip(amostras, valores):
                    self.ax2.plot(amostra, valor, color='green')

                event.canvas.draw()

        elif event.key == 'delete':
            self.ax1.lines.clear()
            self.ax1.texts.clear()
            self.ax2.lines.clear()
            self.ax2.texts.clear()
            self.remove_points.clear()
            self.remove_texts.clear()
            self.count = 1
            self.baseline = None
            self.baseline_value = 120

            event.canvas.draw()

        elif event.key == 'backspace':
            if len(self.ax1.lines) == 0 and len(self.ax2.lines) == 0:
                pass

            elif self.line in self.ax1.lines:
                self.ax1.lines.remove(self.line)
                self.ax1.texts.remove(self.annotate)

                del self.remove_points[-1]
                del self.remove_texts[-1]

                if len(self.remove_points):
                    self.line = self.remove_points[-1]
                    self.annotate = self.remove_texts[-1]
                else:
                    self.line = None
                    self.annotate = None


            elif self.line in self.ax2.lines:
                self.ax2.lines.remove(self.line)
                self.ax2.texts.remove(self.annotate)

                del self.remove_points[-1]
                del self.remove_texts[-1]

                if len(self.remove_points):
                    self.line = self.remove_points[-1]
                    self.annotate = self.remove_texts[-1]
                else:
                    self.line = None
                    self.annotate = None

            event.canvas.draw()

    def gera_baseline(self, value):
        self.baseline_value = value

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
