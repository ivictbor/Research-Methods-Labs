#python3
#modules depended:
#   numpy matplotlib python-dateutil pyparsing six
#
#call format
#  analysis.py data_file
#

import sys, re, math,numpy

prec = 3  # digits after dot for display

# == read data from file
dataFile = open(sys.argv[1])
data = []  #will be populated with data

try:
    for line in dataFile:
        if re.match('^\#', line):
            continue
        match = re.match('^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)$', line)
        if match and re.match('\d+', match.group(1)):  #second cond: if first column is number, not 'sum' or smth else
            data.append( {'N':match.group(1),
                          'Y':float(match.group(2).replace(',','.')), 
                          'X1':float(match.group(3).replace(',','.')),
                          'X2':float(match.group(4).replace(',','.')),
                          'X3':float(match.group(5).replace(',','.'))
                         } )
finally:
    dataFile.close()
   
def average(arr):
    return sum(arr)/len(arr)

fact = ['X1', 'X2', 'X3']
avg = {}
stdisp = {}
n = len(data)
for x in fact:
    avg[x] = average([d[x] for d in data])  
    stdisp[x] = math.sqrt(sum(pow(d[x]-avg[x],2) for d in data)/(n-1))  # std dispersion
    
#normalize 
normarg = []
for d in data:
    normarg.append( {x:(d[x] - avg[x])/stdisp[x] for x in fact})

# matrix of normalized arguments    
X = []        
for a in normarg:
    X.append([a['X1'], a['X2'], a['X3']])

from numpy import matrix
    
X = matrix(X)
XT = X.T #transplanation   
XTxX = XT * X

#find corellation
r = XTxX / (n-1)  
detr = numpy.linalg.det(r)
if detr > 0.7:
    print("multicollinearity impossible: det(r)="+str(detr))
    sys.exit()

# ==========================================
# Check multicollinearity by squared chi - criterion
# ==========================================    
m = len(fact)
sq_chi = - (n-1-(2*m+5)/6) * math.log(detr)
v = m*(m-1)/2  #The number of degrees of freedom  

from constant_tables import sq_chi_tabl 
sq_chi_t = sq_chi_tabl[int(v-1)]
if sq_chi <= sq_chi_t:
    print("multicollinearity impossible: sq_chi <= sq_chi_t")
    sys.exit()

# ==========================================
# Check multicollinearity by F - criterion
# ==========================================
C = r.I  #inverse corel. matrix
F = []
for x in range(0, len(fact)):
   F.append((C.item(x,x)-1)*(n-m)/(m-1))

v1 = n - m
v2 = m - 1   
from constant_tables import F_tabl 
F_t = F_tabl[int(v1 - 1)][int(v2 - 1)]

col_x = ""
for i in range(0,len(F)):
    if F[i] > F_t:
        col_x += 'X_{'+str(i+1)+'}\ '

pairs = []
for i in range(1, m+1) :       
    for j in range(i+1, m+1) :
        pairs.append([i,j])

sep_koef_korr = ""

for p in pairs:
    i = p[0];
    j = p[1];
    r_ij_k = -C.item(i-1, j-1) / math.sqrt(C.item(i-1,i-1)*C.item(j-1,j-1))
    if r_ij_k < 0.1:
        cor_strength = "Отсутствует"
    elif 0.1 <= r_ij_k < 0.3 : 
        cor_strength = "Слабая"
    elif 0.3 <= r_ij_k < 0.5 : 
        cor_strength = "Умеренная"
    elif 0.5 <= r_ij_k < 0.7 : 
        cor_strength = "Заметная"   
    elif 0.7 <= r_ij_k < 0.9 : 
        cor_strength = "Высокая"       
    elif 0.9 <= r_ij_k <= 1 : 
        cor_strength = "Очень\ высокая"           
    sep_koef_korr += '$r_{'+str(i)+'\ '+str(j)+'} = '+ str(round(r_ij_k, prec))+\
        ',\ -\ '+cor_strength+'\ связь\ между\ Х_{'+str(i)+'}\ и\ X_{'+str(j)+'}$\n'  
    
 
avgY = average([d['Y'] for d in data])  
stdispY = math.sqrt(sum(pow(d['Y']-avgY,2) for d in data)/(n-1))  # std dispersion
    
#normalize 
normY = []
for d in data:
    normY.append((d['Y'] - avgY)/stdispY)
    
from numpy import array    
  
normY = array(normY)   

linRegr = numpy.linalg.lstsq(X, normY) # solve the lenear regression

#True estimates of the parameters
b=[0]
avg_weight_sum = 0
koefstr = ''
for i in range(1,m+1):
    x = 'X'+str(i)
    b.append(linRegr[0][i-1] * stdispY / stdisp[x])
    avg_weight_sum += b[i] * avg[x]
    koefstr += (' + ' if b[i] > 0 else ' - ')+str(round(abs(b[i]),prec))+'X_'+str(i)

b[0] = avgY - avg_weight_sum

#estimates
Ytr=[]
for d in data:
    Ytr.append(b[0] + sum(d['X'+str(i)] * b[i] for i in range(1,m+1)))

Y = [d['Y'] for d in data]
#Pirsons coef
rxy = sum( ((Y[i] - average(Y))*(Ytr[i] - average(Ytr))) for i in range(0, n)) / \
    math.sqrt(sum(pow(Y[i] - average(Y),2) for i in range(0, n)) * \
         sum(pow(Ytr[i] - average(Ytr),2) for i in range(0, n))) 
         
sqR = pow(rxy,2)    
 
# ==========================================
# == plotting results
# ==========================================


import matplotlib.pyplot as plt

tex = '$Определитель\ корелляц-й\ матрици:$\n\
$det(r) = '+str(round(detr, prec))+'$\n\
$\\chi_p^2 = '+str(round(sq_chi, prec))+' > \\chi_{табл}^2 = ' +str(round(sq_chi_t,prec))+ '$\n\
$Коллинеарные\ переменные$\n $(F_{x_i}>F_{табл}) :'+col_x+'$\n\n\
$Частичные\ коэф-ы\ корелл:$\n'+sep_koef_korr


texr ='$Модель\ без\ коллинеарности:$\n\
$Y_{tr}='+str(round(b[0], prec))+koefstr+'$\n\n\
$Достоверность\ аппроксимации$\n\
$R^2='+str(round(sqR, prec))+'$'


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
t = ax.text(0.75, 0.75, texr,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=16, 
        color='black')    

import numpy as np       

# plot graphic
miny = min(Y+Ytr)*0.9
maxy = max(Y+Ytr)*1.1    
minx = 0
maxx = n*1.1  
    
t1 = np.arange(miny,maxy, (maxy - miny)/100)
t2 = np.arange(minx,maxx, (maxx - minx)/100) 
ax2 = plt.axes([0.1, 0.1, 0.8, 0.4])
ax2.set_ylim(miny,maxy)
ax2.set_xlim(minx,maxx)
ax2.grid(True)
ax2.plot(range(1,n+1), Y, 'r.-')     
ax2.plot(range(1,n+1), Ytr, 'g.-') 
# det size
ax.figure.canvas.draw()
bbox = t.get_window_extent()

# set size
fig.set_size_inches(bbox.width*2/80,bbox.height/80) # dpi=80

plt.show()

#plt.savefig('test.svg')
#plt.savefig('test.png', dpi=300)




