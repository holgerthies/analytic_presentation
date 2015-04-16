#!/usr/bin/python
import numpy as np
from itertools import chain, cycle, islice
from collections import defaultdict
from matplotlib.pyplot import *
import sys
import math

labels = {1:"sin(x)", 2:"$\\frac{1}{1+x^2}$", 3:"$\\sqrt{2+x}$", 4:"$\\log(2+x)$"}
names = {1:"sin", 2:"xinv", 3:"sqrt", 4:"log"}
funcs = set()
precs = set()
ds = set()

def make_piecewise_constant(X,Y):
	X=list(chain.from_iterable((X[i], X[i+1]-0.00001) for i in range(len(X)-1)))
	X.append(X[-1])
	X.append(X[-1]+(X[-1]-X[-3]))
	Y = list(chain.from_iterable((y, y) for y in Y))
	return X,Y

def parse(input):
	repetitions = int(input[0].split()[-1])
	eval_times = dict()
	for i in range(0,len(input), repetitions+1):
		f, p, d, r = map(int, input[i].split())
		time = 0.0
		for j in range(1,repetitions+1):
			if i+j >= len(input): break
			t = input[i+j].split()[0].split(":")[1]
			time += float(t)/float(repetitions)
		eval_times[(f,p,d)] = time
	return eval_times



def plotN(data):
	colors = ['blue', 'red', 'green', 'yellow', 'cyan', 'orange']
	Y=[dict(),dict()]
	for i, func in enumerate([1,2]): 
		for f,p,d in data:
			if d== 0 and f==func:
				Y[i][p] = data[(f,p,d)]
	for i in range(2):
		x = sorted(Y[i].keys())
		y = []
		for k in x:
			y.append(Y[i][k])
		x,y = make_piecewise_constant(x,y)
		plot (x, y, color=colors[i], label=labels[i+1])
	legend(loc=0)
	xlabel('valid decimals')
	ylabel('time (s)')
	title("Time to evaluate BA_ANA depending on the number of valid decimals", y=1.02)
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/ba_ana_dep_on_n.png')
	clf()

def plotDiff(data, ns, func):
	colors = ['blue', 'red', 'green', 'orange', 'cyan', 'yellow']
	Y=[dict() for _ in ns]
	for i, n in enumerate(ns):
		for f,p,d in data:
			if f==func and p==n:
				Y[i][d] = data[(f,p,d)]
	for i,n in enumerate(ns):
		x = sorted(Y[i].keys())
		y = []
		for k in x:
			y.append(Y[i][k])
		x,y = make_piecewise_constant(x,y)
		plot (x, y, color=colors[i], label="n = "+str(n))
	legend(loc=0)
	xlabel('Number of Differentiations')
	ylabel('time (s)')
	title("Eval differentiated BA_ANA ("+labels[func]+") depending the number of differentiations", y=1.02)
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/ba_ana_dep_on_diff_'+names[func]+'.png')
	clf()
def main():
	#data = []
	filename=sys.argv[1]
	with open('../src/'+filename, 'rb') as f:
		eval_times = parse(list(f))
	plotN(eval_times)
	for i in range(1,3):
		plotDiff(eval_times, [500,1000,2000,4000], i)
	print "done"

if __name__ == "__main__":
	main()



