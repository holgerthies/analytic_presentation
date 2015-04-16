import numpy as np
from matplotlib.pyplot import *
import csv
from itertools import chain
data = []

with open('bana0.csv', 'rb') as csvfile:
	table = csv.reader(csvfile, delimiter=' ')
	for row in table:
		data.append(row)
with open('bana1.csv', 'rb') as csvfile:
	table = csv.reader(csvfile, delimiter=' ')
	for row in table:
		data.append(row)
with open('bana2.csv', 'rb') as csvfile:
	table = csv.reader(csvfile, delimiter=' ')
	for row in table:
		data.append(row)
with open('bana3.csv', 'rb') as csvfile:
	table = csv.reader(csvfile, delimiter=' ')
	for row in table:
		data.append(row)
def make_piecewise_constant(X,Y):
	X=list(chain.from_iterable((X[i], X[i+1]-0.00001) for i in range(len(X)-1)))
	X.append(X[-1])
	X.append(X[-1]+(X[-1]-X[-3]))
	Y = list(chain.from_iterable((y, y) for y in Y))
	return X,Y
def plotN():
	X1 = [float(row[1]) for row in data if row[0]=='0']
	Y1 = [float(row[2]) for row in data if row[0] == '0']
	X2 = [float(row[1]) for row in data if row[0]=='1']
	Y2 = [float(row[2]) for row in data if row[0] == '1']
	X1,Y1 = make_piecewise_constant(X1,Y1)
	X2, Y2 = make_piecewise_constant(X2,Y2)
	plot(X1, Y1, color='blue', label="sin(0.8)")
	plot(X2, Y2, color='green', label="1/(1+x^2/2)(0.8)")
	legend(loc=1)
	xlabel('n')
	ylabel('time (s)')
	show()

def plotDx1():
	X1 = [float(row[1]) for row in data if row[0]=='2' and row[2]=='5']
	Y1 = [float(row[3]) for row in data if row[0] == '2' and row[2]=='5']
	X1,Y1 = make_piecewise_constant(X1,Y1)
	X2 = [float(row[1]) for row in data if row[0]=='2' and row[2]=='505']
	Y2 = [float(row[3]) for row in data if row[0] == '2' and row[2]=='505']
	X2,Y2 = make_piecewise_constant(X2,Y2)
	X3 = [float(row[1]) for row in data if row[0]=='2' and row[2]=='1005']
	Y3 = [float(row[3]) for row in data if row[0] == '2' and row[2]=='1005']
	X3,Y3 = make_piecewise_constant(X3,Y3)
	X4 = [float(row[1]) for row in data if row[0]=='2' and row[2]=='1505']
	Y4 = [float(row[3]) for row in data if row[0] == '2' and row[2]=='1505']
	X4,Y4 = make_piecewise_constant(X4,Y4)
	X5 = [float(row[1]) for row in data if row[0]=='2' and row[2]=='2005']
	Y5 = [float(row[3]) for row in data if row[0] == '2' and row[2]=='2005']
	X5,Y5 = make_piecewise_constant(X5,Y5)	
	plot(X1, Y1, color='black', label="n=5")
	#plot(X2, Y2, color='blue', label="n=505")
	plot(X3, Y3, color='green', label="n=1005")
	plot(X4, Y4, color='blue', label="n=1505")
	plot(X5, Y5, color='red', label="n=2005")
	xlim(25, max(X1))
	legend(loc=0)
	xlabel('i')
	ylabel('time (s)')
	show()
def plotDx2():
	X1 = [float(row[2]) for row in data if row[0]=='2' and row[1]=='1']
	Y1 = [float(row[3]) for row in data if row[0] == '2' and row[1]=='1']
	X1,Y1 = make_piecewise_constant(X1,Y1)
	X2 = [float(row[2]) for row in data if row[0]=='2' and row[1]=='41']
	Y2 = [float(row[3]) for row in data if row[0] == '2' and row[1]=='41']
	X2,Y2 = make_piecewise_constant(X2,Y2)
	X3 = [float(row[2]) for row in data if row[0]=='2' and row[1]=='441']
	Y3 = [float(row[3]) for row in data if row[0] == '2' and row[1]=='441']
	xlim(min(X1), max(X1))
	X3,Y3 = make_piecewise_constant(X3,Y3)
	plot(X1, Y1, color='black', label="i=5")
	plot(X2, Y2, color='blue', label="i=41")
	plot(X3, Y3, color='red', label="i=441")
	legend(loc=0)
	xlabel('n')
	ylabel('time (s)')
	show()