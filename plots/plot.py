#!/usr/bin/python
import numpy as np
import csv
from itertools import chain, cycle, islice
from collections import defaultdict
from matplotlib.pyplot import *
import sys
import math

labels = {1:"sin(x)", 2:"$\\frac{1}{1+x^2}$", 3:"$\\sqrt{2+x}$", 4:"$\\log(2+x)$"}
names = {1:"sin", 2:"xinv", 3:"sqrt", 4:"log"}
funcs = set()
precs = set()
ks = set()


def parse(input):
	"""returns two dictionaries evaluation_times and cached_coefficients
		evaluation_times:  
			each entry with index f,k,p is a list of of tuples (float, int, int, int) (t, prec, man, exp)
			where t is the avg time it took until the start of iteration i (last entry corresponds to end of program)
			and m is the mantissa and e the exponent of the error
		cached_coefficients:
			each entry with index f,k,p is a list (list (int)) containing the number of saved  
			coefficients for each of the power series after each iteration
		"""
	new_evaluation = True
	f,k,p,m = 0,0,0,0
	evaluation_times = dict()
	cached_coefficients = defaultdict(list)
	for l in input:
		if new_evaluation:
			f,k,p,m = map(int, l.split())
			evaluation_times[(f,k,p)] = []
			new_evaluation = False
			t, prec, man, exp = 0,0,0,0
			count, iteration_count = 0, 0
		else:
			components = l.split()
			if components[1] == "end": #last iteration
				count += 1
				#t = float(components[0].split(":")[1])/m
				#if len(evaluation_times[(f,k,p)]) <= iteration_count:
				#	evaluation_times[(f,k,p)].append((t, prec, man,exp))
				#else:
				#	t_before = evaluation_times[(f,k,p)][iteration_count][0]
				#	evaluation_times[(f,k,p)][iteration_count] = (t+t_before, prec, man, exp)
				t, prec, man, exp = 0,0,0,0
				iteration_count = 0
				if count == m:
					new_evaluation = True
			else:
				# example: time:0.050 Iteration:2 precision:-136 error_mantissa:221887316 error_exponent:-137
				t = float(components[0].split(":")[1])/m
				#i = int(components[1].split(":")[1])
				prec = int(components[2].split(":")[1])
				man = int(components[3].split(":")[1])
				exp = int(components[4].split(":")[1])
				if len(cached_coefficients[(f,k,p)]) <= iteration_count:
					cached_coefficients[(f,k,p)].append([int(c) for c in components[6:]])
				if len(evaluation_times[(f,k,p)]) <= iteration_count:
					evaluation_times[(f,k,p)].append((t, prec, man,exp))
				else:
					t_before = evaluation_times[(f,k,p)][iteration_count][0]
					evaluation_times[(f,k,p)][iteration_count] = (t+t_before, prec, man,exp)
				iteration_count += 1
	return evaluation_times, cached_coefficients






def make_piecewise_constant(X,Y):
	X=list(chain.from_iterable((X[i], X[i+1]-0.00001) for i in range(len(X)-1)))
	X.append(X[-1])
	X.append(X[-1]+(X[-1]-X[-3]))
	Y = list(chain.from_iterable((y, y) for y in Y))
	return X,Y



def autolabel(ax, rects, labels, bottomx):
    # attach some text labels
    for i,rect in enumerate(rects):
        height = rect.get_height()
        b = bottom[i] if bottom else 0
        ax.text(rect.get_x()+rect.get_width()/2., 0.5*height+b, labels[i],ha='center', va='bottom', fontsize='7')
def autolabel_top(ax, rects, labels, bottom, is_log=False):
    # attach some text labels
    for i,rect in enumerate(rects):
        height = rect.get_height()
        b = bottom[i] if bottom else 0
        if bottom: bm = max(bottom)
        if not is_log:
        	b += 0.01*bm
        ax.text(rect.get_x()+rect.get_width()/2., b, labels[i],ha='center', va='bottom', fontsize='9')

def autolabel_log(ax, rects, labels):
    # attach some text labels
    for i,rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height, labels[i],ha='center', va='bottom', fontsize='9')


def barN(data, coeffs, f,k, iteration_infos=False, log=False):
	X = defaultdict(list)
	Y = defaultdict(list)
	width = 25
	my_colors = 'rgbymc'
	barlabels = defaultdict(list)
	toplabels = []
	fig, ax = subplots()
	for n in precs:
		if (f,k,n) in data:
			for i, (t,prec, man,exp) in enumerate(data[(f,k,n)]):
				X[i].append(n)
				real_t = t-data[(f,k,n)][i-1][0] if i>0 else t
				Y[i].append(real_t)
				if iteration_infos:
					barlabels[i].append("prec: "+str(prec)+"\n err:"+str(man)+"x2^"+str(exp)+"\n"+"coeffs: "+str(coeffs[(f,k,n)][i]))
				elif i==len(data[(f,k,n)])-1: # last iteration
					toplabels.append("prec: "+str(prec)+"("+str(i+1)+")")
	max_Y=0
	#if k==0: print X, Y
	p0 = None
	max_bottom = defaultdict(int)
	for i in X:
		if i < len(X):
			bottom = None if i==0 else [Y[i-1][j] for j in range(len(Y[i-1])) if X[i-1][j] in X[i]]
			for ix,x in enumerate(X[i]): 
				max_bottom[x] += Y[i][ix] 
			if i>0 and len(Y[i]) != len(bottom): # data not complete yet
				continue
			#print i, k, bottom, barlabels[i]
			p1 = bar(X[i], Y[i], width,bottom=bottom, color=list(islice(cycle(my_colors),2*i, 2*i+len(my_colors))), log=log)
			if not p0: p0 = p1 # first 
			if iteration_infos:
				autolabel(ax,p1, barlabels[i], bottom)
			max_Y = max(max_Y, max(Y[i]))
	if not iteration_infos:
			bottom = [max_bottom[i] for i in max_bottom]
			autolabel_top(ax,p0, toplabels,bottom, is_log=log)
	title("Time to compute "+labels[f]+" at center of series "+str(k)+" depending on output precision", y=1.02)	
	xticks([x+width/2. for x in X[0]],  map(int,X[0]))
	legend(loc=0)
	#xlabel('precision ($2^{-n}$')
	xlabel('valid decimals')
	ylabel('time (s)')
	#show()
	ylim(ymax=1.2*max_Y)
	log_str = '_log' if log else ''
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/'+names[f]+'_for_series_'+str(k)+'_dep_on_n'+log_str+'.png')
	clf()


def barK(data, coeffs, f, n, iteration_infos=False, log=False):
	X = defaultdict(list)
	Y = defaultdict(list)
	width = 1
	my_colors = 'rgbymc'
	barlabels = defaultdict(list)
	toplabels = []
	fig, ax = subplots()
	for k in ks:
		if (f,k,n) in data:
			for i, (t,prec, man,exp) in enumerate(data[(f,k,n)]):
				X[i].append(k)
				real_t = t-data[(f,k,n)][i-1][0] if i>0 else t
				Y[i].append(real_t)
				if iteration_infos:
					barlabels[i].append("prec: "+str(prec)+"\n err:"+str(man)+"x2^"+str(exp)+"\n"+"coeffs: "+str(coeffs[(f,k,n)][i]))
				elif i==len(data[(f,k,n)])-1: # last iteration
					toplabels.append("prec: "+str(prec)+"("+str(i+1)+")")
	max_Y=0
	p0=None
	max_bottom = defaultdict(int)
	for i in X:
		if i < len(X):
			bottom = None if i==0 else [Y[i-1][j] for j in range(len(Y[i-1])) if X[i-1][j] in X[i]]
			for ix,x in enumerate(X[i]): 
				max_bottom[x] += Y[i][ix] 
			if i>0 and len(Y[i]) != len(bottom): # data not complete yet
				continue
			p1 = bar(X[i], Y[i], width,bottom=bottom, color=list(islice(cycle(my_colors),3*i, 3*i+len(my_colors))), log=log)
			if not p0: p0 = p1 # first 
			if iteration_infos:
				autolabel(ax,p1, barlabels[i], bottom)
			max_Y = max(max_Y, max(Y[i]))

	if not iteration_infos:
			bottom = [max_bottom[i] for i in max_bottom]
			autolabel_top(ax,p0, toplabels,bottom, is_log=log)

	title("Time to compute "+labels[f]+" at center of l-th series for "+str(-n)+" valid decimals", y=1.02)
	xticks([x+width/2. for x in X],  map(int,X))
	legend(loc=0)
	#xlabel('precision ($2^{-n}$')
	xlabel('l')
	ylabel('time (s)')
	#show()
	ylim(ymax=1.2*max_Y)
	log_str = '_log' if log else ''
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/'+names[f]+'_for_n_prec_'+str(n)+'_dep_on_series'+log_str+'.png')
	clf()

def logbarK(data, coeffs, f, n):
	X = []
	Y = []
	width = 1
	my_colors = 'rgbymc'
	toplabels = []
	fig, ax = subplots()
	for k in ks:
		if (f,k,n) in data:
			t,prec,man,exp = data[(f,k,n)][-1]
			X.append(k)
			Y.append(t)
			toplabels.append("prec: "+str(prec)+"("+str(len(data[(f,k,n)]))+")")
	p1 = bar(X, Y, width, color=my_colors, log=True)
	autolabel_log(ax,p1, toplabels)
	title("Time to compute "+labels[f]+" at center of l-th series for "+str(-n)+" valid decimals", y=1.02)
	xticks([x+width/2. for x in X],  map(int,X))
	legend(loc=0)
	#xlabel('precision ($2^{-n}$')
	xlabel('l')
	ylabel('time (s)')
	#show()
	ylim(ymax=1.5*max(Y))
	log_str = '_log'
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/'+names[f]+'_for_n_prec_'+str(n)+'_dep_on_series'+log_str+'.png')
	clf()

def makeTableData(data, coeffs, f,k):
	iterations = set()
	iteration_times = defaultdict(list)
	coeff_data = defaultdict(list)
	error_data = defaultdict(int)
	for n in precs:
		if (f,k,n) in data:
			for i, (t,prec, man,exp) in enumerate(data[(f,k,n)]):
				prec = -prec
				iterations.add(prec)
				real_t = t-data[(f,k,n)][i-1][0] if i>0 else t
				err = int(math.log(man,2)+exp)+1
				iteration_times[prec].append(real_t)
				coeff_data[prec] = coeffs[(f,k,n)][i]
				error_data[prec] = err
	iterationsf = sorted(list(iterations))
	iteration_timesf = []
	coeff_dataf = []
	error_dataf = []
	for i in iterationsf:
		it0 = min(iteration_times[i])
		it1 = max(iteration_times[i])
		if it1-it0>1:
			iteration_timesf.append((it0,it1))
		else:
			iteration_timesf.append(it0)
		coeff_dataf.append(coeff_data[i]) 
		error_dataf.append(error_data[i])
	return iterationsf, iteration_timesf, coeff_dataf, error_dataf




def plotTable(iterations, iteration_times, coeff_data, error_data):
	f=figure()
	fig, ax=subplots()
	ax.xaxis.set_visible(False)
	ax.yaxis.set_visible(False)
	for sp in ax.spines.itervalues():
		sp.set_color('w')
		sp.set_zorder(0)
	rows = []
	columns = []
	cell_text = []
	for it in iterations:
		rows.append(str(it))
	first_col = []
	for t in iteration_times:
		text = str(int(round(t[0])))+" - "+str(int(round(t[1]))) if isinstance(t, tuple) and len(t) > 0 else str(int(round(t))) 
		first_col.append(text)
	second_col = [c[0] for c in coeff_data]
	third_col = [-e for e in error_data]
	columns.append("sec.")
	columns.append("germ 0")
	columns.append("error")
	for i in range(len(rows)):
		cell_text.append([first_col[i], second_col[i], third_col[i]])
	the_table = ax.table(cellText=cell_text,rowLabels=rows,colLabels=columns, loc='center')
	the_table.set_zorder(10)
	table_props = the_table.properties()
	table_cells = table_props['child_artists']
	for cell in table_cells: 
		cell.set_height(0.05)
		cell.set_width(0.1)

def tableN(data, coeffs, f, k):
	iterations, iteration_times, coeff_data, error_data = makeTableData(data, coeffs, f,k)
	plotTable(iterations, iteration_times, coeff_data, error_data)
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/'+names[f]+'_for_series_'+str(k)+'_dep_on_n_table.png')

	clf()

def barCoeffs(coeffs, f, n, ind=0):
	X = []
	Y = []
	width = 1
	my_colors = 'rgbymc'
	for k in ks:
		if (f,k,n) in coeffs:
			X.append(k)
			Y.append(coeffs[(f,k,n)][-1][0])
	title("coeffs of series "+str(ind)+" to compute "+labels[f]+" at center of l-th series for "+str(-n)+" decimals", y=1.02)
	p1 = bar(X, Y, width,color=my_colors)
	xticks([x+width/2. for x in X],  map(int,X))
	legend(loc=0)
	xlabel('l')
	ylabel('number of coefficients')
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/'+names[f]+'_for_coeffs_prec_'+str(n)+'_dep_on_series.png')
	clf()		

def barCoeffsN(coeffs, f, k, ind=0):
	X = []
	Y = []
	width = 25
	my_colors = 'rgbymc'
	for n in precs:
		if (f,k,n) in coeffs:
			X.append(n)
			Y.append(coeffs[(f,k,n)][-1][0])
	title("coeffs of series "+str(ind)+" needed to compute "+labels[f]+" depending on valid decimals", y=1.02)
	p1 = bar(X, Y, width,color=my_colors)
	xticks([x+width/2. for x in X],  map(int,X))
	legend(loc=0)
	xlabel('valid decimals')
	ylabel('number of coefficients')
	savefig('/Volumes/SX 500/Users/TurboHolger/Dropbox/irram/plots/by_holgers_laptop/'+names[f]+'_for_coeffs_series_'+str(k)+'_dep_on_n.png')
	clf()	


def main():
	#data = []
	filename=sys.argv[1]
	with open('../src/'+filename, 'rb') as f:
		table, coeffs = parse(f)
	for (f,k,p) in table:
		funcs.add(f)
		ks.add(k)
		precs.add(p)
	for f in funcs:
		for p in precs:
			barK(table, coeffs, f, p)
			logbarK(table, coeffs, f, p)
			barCoeffs(coeffs, f, p)
		for k in ks:
			barN(table, coeffs, f, k)
			tableN(table, coeffs, f,k)
			barCoeffsN(coeffs, f, k)
			#barN(table, coeffs, f, k, log=True)
	print "done"

if __name__ == "__main__":
	main()




def plotK(data, f):
	colors = ['blue', 'red', 'green', 'yellow', 'cyan', 'orange']
	table = defaultdict(list)
	for row in data:
		if int(row[0]) == f:
			table[int(row[2])].append((int(row[1]), float(row[3])))
	for i in range(0,len(table)/3):
		p = sorted(table.keys())[3*i]
		X = [x[0] for x in table[p]]
		Y = [x[1] for x in table[p]]
		X,Y = make_piecewise_constant(X,Y)
		plot (X, Y, color=colors[i], label='n=$2^{-'+str(p)+'}$')
		legend(loc=0)
		xlabel('k')
		ylabel('time (s)')
		#show() 
		#savefig('dep_on_k_'+names[f]+'_prec_'+str(n)+'.png')