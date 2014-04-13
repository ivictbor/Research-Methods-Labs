__author__ = 'lordgal'
import tkinter as tk
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class Plotter:

    __fig = 1
    __splot = 1
    __canvas = 1
    __toolbar = 1

    def __init__(self,tk_root):
        self.__fig = Figure(figsize=(5,5), dpi=100);
        self.__splot = self.__fig.add_subplot(111)
        self.__splot.grid()

        self.__canvas = FigureCanvasTkAgg(self.__fig, master=tk_root)
        self.__canvas.show()
        self.__canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.__toolbar = NavigationToolbar2TkAgg(self.__canvas, tk_root)
        self.__toolbar.update()
        self.__canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def add_to_plot(self,x,y,legend):
        self.__splot.plot(x,y,'.-',label=legend)
        self.__splot.legend()
        self.__canvas.draw()

    def plot_hist(self,data,bins):
        self.__splot.hist(data,bins)
        self.__canvas.draw()
    def plot(self,x,y):
        self.__splot.clear();
        self.__splot.grid()
        self.__splot.plot(x,y)
        self.__canvas.draw()
#        print('plot2')