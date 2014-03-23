#!/usr/bin/python

import tkinter as tk
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from numpy import arange, sin, pi


class Plotter:
    
    __fig = 1
    __splot = 1
    __canvas = 1
    __toolbar = 1

    def __init__(self,tk_root,x,y):
        self.__fig = Figure(figsize=(5,5), dpi=100);
        self.__splot = self.__fig.add_subplot(111)
        self.__splot.grid()
        #self.__splot.plot(x,y)

        self.__canvas = FigureCanvasTkAgg(self.__fig, master=tk_root)
        self.__canvas.show()
        self.__canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
        self.__toolbar = NavigationToolbar2TkAgg(self.__canvas, tk_root)
        self.__toolbar.update()
        self.__canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    def destroy(self):
        pass

    def plot(self,x,y):
        self.__splot.clear();
        self.__splot.grid()
        self.__splot.plot(x,y)

        self.__canvas.draw()
#        print('plot2')

class Window:

    root = 1
    left_frame =1
    right_frame = 1
    plotter = 1

    def __init__(self):
        self.root = tk.Tk()
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.resizable(True, True)
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open",command=self.opencsv)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        self.left_frame = tk.Frame(self.root)
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0,column=1,sticky='nsew')
        self.left_frame.grid(row=0,column=0,sticky='nsew')
#        button1=tk.Button(self.left_frame,text='ok',bg='black',fg='red',font='arial 14')
#        button1.pack()

    def plot(self):
        x = arange(0.0,3.0,0.01)
        y = sin(2*pi*x)
        self.plotter.plot(x,y)
#        print('plot1')

    def opencsv(self):
        fname = tk.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                print("""here it comes: self.settings["template"].set(fname)""")
                print(fname)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

def main():
        
    x = arange(0.0,3.0,0.01)
    y = sin(2*pi*x)

    window = Window()    
    window.plotter = Plotter(tk_root = window.right_frame, x=x,y=y)

#    window.plot(x=x,y=y)

    window.root.mainloop()





# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
