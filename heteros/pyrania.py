#!/usr/bin/python

#scikit-learn, pandas


import tkinter as tk
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from numpy import arange, sin, pi, linalg
from math import sqrt
import numpy
from pandas import read_csv
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def rank(array):
    tmp_array = numpy.array(array)
    temp = tmp_array.argsort()
    ranks = numpy.empty(len(tmp_array), int)
    ranks[temp] = numpy.arange(len(tmp_array))
    return ranks

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

    def add_to_plot(self,x,y):
        self.__splot.plot(x,y)
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

class Window:

    root = {}
    left_frame = {}
    right_frame = {}
    label_R2 = {}
    plotter = {}
    depend_var = {}
    independ_var = {}
    t_criteria = {}

    def __init__(self):
        self.root = tk.Tk()
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.resizable(True, True)
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open",command=self.opencsv)
        filemenu.add_command(label="Process data",command=self.calc_model)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        self.left_frame = tk.Frame(self.root)
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0,column=1,sticky='nsew')
        self.left_frame.grid(row=0,column=0,sticky='nsew')
# вторая привязка
        self.listbox=tk.Listbox(self.left_frame,width=70,heigh=40,selectmode=tk.EXTENDED)
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH)
#        self.listbox.grid(sticky='nsew',row=1,column=0)
        scrollbar = tk.Scrollbar(self.left_frame,orient=tk.HORIZONTAL)
        scrollbar.pack(side = tk.TOP, fill=tk.X);
#        scrollbar.grid(row=0,column=0)
        self.listbox.config(xscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.xview)

        self.plotter = Plotter(tk_root = self.right_frame)

        self.t_criteria = read_csv("t-crit.csv")['T']
#        print(self.t_criteria)


    def plot(self):
        x = arange(0.0,3.0,0.01)
        y = sin(2*pi*x)
        self.plotter.plot(x,y)

    def opencsv(self):
        fname = tk.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                dataset = read_csv(fname)
                print(fname)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        else:
            return
        
        dataset.head()
        self.depend_var = dataset['y']
        self.independ_var = dataset.drop('y',axis=1)
        self.calc_model()

    def calc_model(self):
        i = 0
        for var in self.independ_var:
#            xx = self.independ_var[var].reshape((self.independ_var[var].shape[0],-1))
#            yy = self.depend_var.reshape((self.depend_var.shape[0],-1))
#            model = LinearRegression().fit(xx,self.depend_var)
#            predicted = model.predict(xx)
            xx = numpy.vstack([self.independ_var[var],numpy.ones(len(self.depend_var))]).T
            b = linalg.lstsq(xx,self.depend_var)[0]
            predicted = self.independ_var[var]*b[0] + b[1]

            errors = self.depend_var-predicted
            self.plotter.add_to_plot(arange(0,len(self.depend_var)),errors)
#            r2 = r2_score(self.depend_var,predicted)
            #self.plotter.plot_hist(errors,arange(0,4,0.25))
#            self.label_R2['text'] = "R2 value: " + str(r2)

            err_rank = rank(errors)
            n = len(self.independ_var[var])
            sqrank_sum = sum((err_rank - rank(self.independ_var[var]))**2)
            Rox = 1-6*(sqrank_sum/(n*((n**2)-1)))
            t = (abs(Rox)*sqrt(n-2))/(sqrt(1-Rox**2))
            self.listbox.insert(tk.END,"Расчетное значение t-критерия для независимой переменной "+str(i+1) + "равно: " + str(t))
            if t > numpy.float64(self.t_criteria[n-2]):
                self.listbox.insert(tk.END,"Расчетное значения критерия t = " + str(t) + ", что больше табличного для v=18 " + str(self.t_criteria[n-2]) + " Критерий вносит гетероскедастичных ошибок")
            else:
                self.listbox.insert(tk.END,"Расчетное значения критерия t = " + str(t) + ", что меньше табличного для v=18 " + str(self.t_criteria[n-2]) + " Критерий не вносит гетероскедастические ошибки")
            i += 1



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    Window().root.mainloop()
