import numpy
import tkinter as tk
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import plotter
import scipy.optimize
from plotter import *
from pandas import read_csv


def function(x,a0,a1,a2,a3,a4,a5):
    #print(x,a0,a1,a2,a3,a4,a5)
    return a0+a1*x[0]+a2*x[1]+a3*(x[0]**2)+a4*(x[1]**4)+a5*x[0]*x[1]

def splitter(xdata,ydata):
    return((xdata[::2], ydata[::2]), (xdata[1::2], ydata[1::2]))



class Mguator:

    depend_var = {}
    independ_var = {}
    function = None
    selector = None

    def __init__(self,independ_var,depend_var,func ):
        self.depend_var = depend_var
        self.independ_var = independ_var
        self.function = func

    def combine(self,args_count):
        pairs = []
        for i in range(1, args_count+1):
            for j in range(i + 1, args_count+1):
                pairs.append((i,j))
                pairs.append((j,i))
        return pairs

    def otmguashit(self):

        (train_xdata,train_ydata),(ctrl_xdata,ctrl_ydata) = splitter(self.independ_var,self.depend_var)
        #print(train_xdata,train_ydata,ctrl_xdata,ctrl_ydata)
        x_cnt = self.independ_var.columns.values.size
        combinations = self.combine(x_cnt)

        self.model = []
        step_values = (train_xdata.values,train_ydata.values)

        while True:
            step_model = []
            for indx in combinations:
                step_model.append((indx,scipy.optimize.curve_fit(self.function, [step_values[0][:,indx[0]:indx[0]+1].T,
                                                    step_values[0][:,indx[1]:indx[1]+1].T], step_values[1])[0]))
            #Возвращает список кортежей ((индексы),[коэфициенты],[Расчетные значения функции])
            #Принимает базовую функцию список кортежей ((индексы),[коэфициенты])
            step_model = self.selector(self.function,step_model)
            #-----------обрабатываем данные после селекции
            self.model.append(step_model)
            if step_model.size == 1:
                break
            combinations = step_model.size
            new_step_values = numpy.array([])
            for values in step_model:
                new_step_values.vstack
            step_values = (new_step_values,step_values[1])

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
        pass
        # self.root = tk.Tk()
        # self.root.grid_columnconfigure(1, weight=1)
        # self.root.grid_columnconfigure(1, weight=1)
        # self.root.grid_rowconfigure(0, weight=1)
        # self.root.resizable(True, True)
        # menubar = tk.Menu(self.root)
        # filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Open",command=self.opencsv)
        # filemenu.add_command(label="Process data",command=self.calc_model)
        # menubar.add_cascade(label="File", menu=filemenu)
        # self.root.config(menu=menubar)
        # self.left_frame = tk.Frame(self.root)
        # self.right_frame = tk.Frame(self.root)
        # self.right_frame.grid(row=0,column=1,sticky='nsew')
        # self.left_frame.grid(row=0,column=0,sticky='nsew')
        #
        # self.plotter = Plotter(tk_root = self.right_frame)


    def opencsv(self):
        #fname = tk.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
        #                                   ("All files", "*.*") ))
        fname= "/home/lordgal/Univers/СМНД/Research-Methods-Labs/MGUA/data.csv"
        if fname:
            try:
                self.dataset = read_csv(fname)
                print(fname)
            except:                     # <- naked except is a bad idea
                print("Open Source File", "Failed to read file\n'%s'" % fname)
        else:
            return

        self.dataset.head()
        self.depend_var = self.dataset['y']
        self.independ_var = self.dataset.drop('y',axis=1)
#        print("Независимые переменные \n",self.independ_var.values[:,:2])
#        print("Зависимые переменные \n",self.depend_var.values)
        self.calc_model()

    def calc_model(self):
        mg = Mguator(self.independ_var,self.depend_var,function)
        mg.otmguashit()

        pass


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    # 1/5 лвололдош
    Window().opencsv()#root.mainloop()
