import matplotlib.pyplot as plt

class GeraGrafico:
    def __init__(self, plt):
        self.x = []
        self.y = []
        self.position = (0,0)
        self.line = []
        self.click = False
        self.fig, self.ax = plt.subplots()
        self.ax.axis((-500, 500, 0, 500))
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        plt.show()


    def gera_valores(self, x, y, amostras=30 ):
        y1 = [n for n in range(y + amostras, y, -1)]
        y2 = [n for n in range(y, y + amostras + 1)]

        self.x = [n for n in range(x - amostras, x + amostras + 1)]
        self.y = y1 + y2

        return (self.x, self.y)



    def onclick(self, event):
        self.click = True
        for line in self.ax.lines:
            if int(event.xdata) in line.get_xdata() and int(event.ydata) in line.get_ydata():
                self.line = line
                break

        else:
            x, y = self.gera_valores(int(event.xdata), int(event.ydata))
            self.position = (int(event.xdata), int(event.ydata))
            self.ax.plot(x, y)
            event.canvas.draw()



    def onrelease(self, event):
        self.click = False

    def onmotion(self, event):
        if self.click:
            x, y = self.gera_valores(int(event.xdata), int(event.ydata))
            self.line.set_data(x, y)
            event.canvas.draw()


        '''
        if self.click:
            for line in self.ax.lines:
                print(self.position)
                for x, y in zip(line.get_xdata(), line.get_ydata()):
                    if self.position[0] == x and self.position[1] == y:
                        x, y = self.gera_valores(int(event.xdata), int(event.ydata))
                        line.set_xdata(x)
                        line.set_ydata(y)
                        event.canvas.draw()


                        self.click = False

            else:
                x, y = self.gera_valores(int(event.xdata), int(event.ydata))
                self.position = (int(event.xdata), int(event.ydata))
                self.ax.plot(x, y)

                self.click = False

            '''

if '__main__' == __name__:
    gg = GeraGrafico(plt)
