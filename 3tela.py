import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


import numpy as np

from graficos import GeraGrafico



root = tkinter.Tk()
root.wm_title("Embedding in Tk")

graficos = GeraGrafico(plt.figure())


canvas = FigureCanvasTkAgg(graficos.fig, master=root)  # A tk.DrawingArea.
canvas.draw()


toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)



canvas.mpl_connect('button_press_event', graficos.onclick)
canvas.mpl_connect('button_release_event', graficos.onrelease)
canvas.mpl_connect('motion_notify_event', graficos.onmotion)
canvas.mpl_connect('key_press_event', graficos.key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.