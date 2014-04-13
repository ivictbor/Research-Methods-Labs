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
    return ranks+1

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

class Window:

    root = {}
    left_frame = {}
    right_frame = {}
    label_R2 = {}
    plotter = {}
    depend_var = {}
    independ_var = {}
    DW_criteria = {}
    dataset = {}
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

        self.plotter = Plotter(tk_root = self.right_frame)



    def plot(self):
        x = arange(0.0,3.0,0.01)
        y = sin(2*pi*x)
        self.plotter.plot(x,y)

    def opencsv(self):
        fname = tk.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                self.dataset = read_csv(fname)
                print(fname)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        else:
            return
        
        self.dataset.head()
        self.depend_var = self.dataset['y']
        self.independ_var = self.dataset.drop('y',axis=1)
        print("Независимые переменные \n",self.independ_var)
        print("Зависимые переменные \n",self.depend_var)
        self.calc_model()

    def calc_model(self):
        model = LinearRegression().fit(self.independ_var,self.depend_var)
        predicted = model.predict(self.independ_var)
        errors = numpy.array(self.depend_var-predicted)
        a = numpy.array(errors[1:])
        b = numpy.array(errors[:-1])
        print("Ошибки модели:\n",errors)
        errors_sub = a-b
        errors_mul = a*b
#        print(errors_mul)
        DW = sum(errors_sub**2)/sum(errors**2)
        print("Расчетное значение критерия Дарбина-Уотсона равно: " ,DW)
        
        n=len(errors);   
        DW1 = 1.10;
        DW2 = 1.54;

        if DW < DW1:
            print("Расчетное значение меньше табличного для нижней границы. Присутствует положительная автокореляция")
        elif DW1 < DW and DW <DW2:
            print("Расчетное значение между границ. Присутствие автокореляции не пределено")
        elif DW2 < DW and DW <(4-DW2):
            print("Автокореляция отсутствует")
        elif (4-DW2) < DW and DW <(4-DW1):
            print("Присутствие автокореляции не пределено")
        elif DW > DW1:
            print("Присутствует отрицательная автокореляция")
        
        Qt= 1.37         
        Q=(n*DW/(n-1))
        print("Критерий фон Неймана",Q)
        if Q < Qt:
            print("Присутствует положительная автокореляция")
        
        r0 = sum(errors_mul)/sum(errors**2)
        if abs(r0) < 0.3:
            print("r0=",r0," Автокореляцией нельзя пренебречь")
        corr = []
        values = self.dataset.values
#        print(self.dataset)
        corr.extend([self.dataset.corr()])
        cp=self.dataset.copy()
        for i in range(0,n-3):
            d=numpy.vstack((self.dataset.values.T[0,i+1:],self.dataset.values.T[1:,i:-1])).T
            cp=cp.from_records(d)
            corr.extend([cp.corr()])
#            print(cp)
        corrk= {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
        for a in corr:
            i=0
            for c in a.values[0,1:]:
#                print(c)
                corrk[i].extend([c])
                i+=1
#        print(corrk)
        for a in corrk:
            if len(corrk[a]) > 0:
                self.plotter.add_to_plot(numpy.arange(len(corrk[a])),corrk[a],"Faktor "+str(a))
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    Window().root.mainloop()
