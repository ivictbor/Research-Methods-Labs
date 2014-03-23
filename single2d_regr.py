#python3
#modules depended:
#   numpy matplotlib python-dateutil pyparsing six
#
#call format
#  analysis.py data_file
#

import sys, re, math 

# == read data from file
dataFile = open(sys.argv[1])
data = []  #will be populated with data

try:
    for line in dataFile:
        if re.match('^\#', line):
            continue
        match = re.match('^(\S+)\s+(\S+)\s+(\S+)$', line)
        if match and re.match('\d+', match.group(1)):  #second cond: if first column is number, not 'sum' or smth else
            data.append( {'N':match.group(1),
                          'Y':float(match.group(2).replace(',','.')), 
                          'X':float(match.group(3).replace(',','.'))
                         } )
finally:
    dataFile.close()
   
sums = {'Y':0, 'X':0, 'sqX':0, 'XY':0}    #dict for accumulate sums of params 
for i in range(len(data)):
    data[i]['sqX'] = pow(data[i]['X'], 2)  # calc squared Xi
    data[i]['XY'] = data[i]['X'] * data[i]['Y']  # calc Xi*Yi
    sums['X'] +=  data[i]['X']
    sums['Y'] +=  data[i]['Y']
    sums['sqX'] +=  data[i]['sqX']
    sums['XY'] +=  data[i]['XY']

# calculate the coefficients of the normal equations system
n = len(data)
b1 =  (sums['XY'] - sums['Y']*sums['X']/n) / (sums['sqX'] - pow(sums['X'], 2)/n)
b0 = (sums['Y'] - b1*sums['X'])/n

prec = 3  # digits after dot for display
#regression model      
print('Regression model:\n\tY_ti = {} + {} X_i'.format(round(b0,prec),
                                                     round(b1,prec)))

# variance of Y
sqVar = sum(pow((d['Y']) - sums['Y']/n, 2) for d in data) / (n-1)

# variance of error
sqVarE = sum(pow((d['Y']) - (b0+b1*d['X']), 2) for d in data) / (n-2)

print ('Variance of Y(6_Y^2): {}'.format(round(sqVar,prec)))
print ('Variance of error(6_E^2): {}'.format(round(sqVarE,prec)))

# coefficient of determination
sqR = (sqVar - sqVarE)/sqVar;

# coefficient of correlation 
if sqR<0:
    rXY = 0;
else:   
    rXY = math.sqrt(sqR);

print ('Coefficient of determination(R^2): {}'.format(round(sqR,prec)))
print ('Coefficient of correlation(r_XY): {}'.format(round(rXY,prec)))

# the degree of bias

from numpy import matrix

#from numpy import linalg
A_NES = matrix(
            [ [n,         sums['X']   ],
            [sums['X'], sums['sqX'] ] ] )        
          
A_NESm1 = A_NES.I  #inverse matrix         

#standard errors
Sb0 = math.sqrt(sqVarE*A_NESm1[0,0])
Sb1 = math.sqrt(sqVarE*A_NESm1[1,1])
print ('Standard error (Sb0): {}'.format(round(Sb0,prec)))
print ('Standard error (Sb1): {}'.format(round(Sb1,prec)))

print ('Standard error compare (Sb0/b0): {}%'.format(round(Sb0*100/b0,prec)))
print ('Standard error compare (Sb1/b1): {}%'.format(round(Sb1*100/b1,prec)))

# Elasticity
print ('Elasticity of X: {}'.format(round(b1,prec)))
Elxy= b1 / sum(d['Y'] for d in data) * sum(d['X'] for d in data) # avg replaced by sum, becouse n/n=1
print ('Elasticity of Y depend on X: {}'.format(round(Elxy,prec)))


# == plotting results

import matplotlib.pyplot as plt

tex = '$Регрисионная\ модель:$\n\
$Y_{ti} = '+str(round(b0,prec))+(' + ' if b1 > 0 else ' - ')+str(round(abs(b1),prec))+' X_i$\n\n\
$Дисперсия\ зависимой\ переменной\ Y:$\n\
$\\sigma_Y^2='+str(round(sqVar,prec))+'$\n\n\
$Дисперсия\ ошибок\ e:$\n\
$\\sigma_e^2='+str(round(sqVarE,prec))+'$\n\n'

texr = '$Коэфициент\ детерминации:$\n\
$R^2='+str(round(sqR,prec))+'$\n\n\
$Коэфициент\ корелляции:$\n\
$r_{XY}='+str(round(rXY,prec))+'$\n\n\
$Стандартные\ погрешности\ оценок$\n\
$(с\ учетом\ дисперсии\ остатков)$\n\
$S_{b_0}='+str(round(Sb0,prec))+'$\n\
$S_{b_1}='+str(round(Sb1,prec))+'$\n\n\
$Сравнение\ с\ величинами\ ошибок$\n\
$\\frac{S_{b_0}}{b0}='+str(round(Sb0*100/b0,prec))+'\%$\n\
$\\frac{S_{b_1}}{b1}='+str(round(Sb1*100/b1,prec))+'\%$\n\n\
$Граничная\ эластичность\ фактора X$\n\
$Є_X='+str(round(b1,prec))+'$\n\n\
$Эластичность\ Y\ в\ зависимости\ от\ X$\n\
$Є_{Y/X}='+str(round(Elxy,prec))+'$\n\n'

# draw area
fig = plt.figure(1)
ax = fig.add_axes([0,0,1,1])
ax.set_axis_on()

# Set a possibility to draw cyrrilic fonts
plt.rcParams["text.usetex"] = False

# draw left side
t = ax.text(0.25, 0.75, tex,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=16, 
        color='black')
        
# draw right side        
t = ax.text(0.75, 0.5, texr,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=16, 
        color='black')    

import numpy as np       

# plot graphic
miny = min(d['Y'] for d in data)*0.9
maxy = max(d['Y'] for d in data)*1.1    
minx = min(d['X'] for d in data)*0.9
maxx = max(d['X'] for d in data)*1.1  
    
t1 = np.arange(miny,maxy, (maxy - miny)/100)
t2 = np.arange(minx,maxx, (maxx - minx)/100) 
ax2 = plt.axes([0.12, 0.12, 0.28, 0.45])
ax2.set_ylim(miny,maxy)
ax2.set_xlim(minx,maxx)
ax2.grid(True)
ax2.plot(t2, b0 + b1*t2, 'r')     

# arrays with points
xarr = [d['X'] for d in data]  
yarr = [d['Y'] for d in data]  

plt.plot(xarr, yarr, 'bo')   # plot points from table
        
# det size
ax.figure.canvas.draw()
bbox = t.get_window_extent()

# set size
fig.set_size_inches(bbox.width*2/80,bbox.height/80) # dpi=80

plt.show()

#plt.savefig('test.svg')
#plt.savefig('test.png', dpi=300)