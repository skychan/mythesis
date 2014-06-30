from __future__ import division
import sys
sys.path.append(".\\functions")
import generate
from collections import namedtuple
Item = namedtuple("Item", ['process','due','wt','wc'])

def  h(tardiness,completion,wt,wc,lambda1,lambda2):			# define the contribution of one item for the obj function
	if tardiness:
		c = 1
	else:
		c = 0
	value = lambda1*(wt*tardiness + wc*completion)+ lambda2*200*c
	return value

def ATC(items,S):							# use ATC rule
	J = S[:]
	S = []
	t = 0
	c = []
	while J:
		p = [items[j].process for j in J]
		d = [items[j].due for j in J]
		wt = [items[j].wt for j in J]
		orderidx = generate.Idx(t,p,d,wt)
		j_star = J[orderidx.index(max(orderidx))]
		S.append(j_star)
		J.remove(j_star)
		t = t + items[j_star].process
		c.append(t)
	return S,c

def solve(input_data,m,lambda1,NR):
	lambda2 = 1- lambda1
	Data = input_data.split('\n')					# load data
	n = len(Data) -1						# get the amount of items
	items = []	
	for j in xrange(n):
		data = Data[j]
		parts = data.split()
		p = int(parts[0])					# get the process time
		s = int(parts[2])						# get the setup time
		d = int(parts[3])					# get the due date
		wt = int(parts[4])					# get the tardiness weights
		wc = int(parts[5])					# get the completion weights
		items.append(Item(p+s,d,wt,wc))			# combine those item data
	print 'Data loaded!'	
	S,L,completion = generate.initialization(items,n,m)
	print 'Initialization done!'

	lateness = generate.late(completion,items)			# begin the value initialization
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(n):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc,lambda1,lambda2)
		item_values.append(value)
	G = generate.H(item_values,L)
	line_values = []
	for s in S:
		value = generate.H(item_values,s)
		line_values.append(value)
	print 'Initial values done!'

	for k in xrange(NR):
		l_p,l_m = generate.reorder(items,S,line_values,item_values)
		S[l_p],c_p = ATC(items,S[l_p])
		S[l_m],c_m = ATC(items,S[l_m])
		for j in S[l_p]:
			completion[j] = c_p.pop(0)
			c = completion[j]
			item = items[j]
			wt,wc = item.wt,item.wc
			late = completion[j] - item.due
			t = generate.tard(late)
			item_values[j] = h(t[0],c,wt,wc,lambda1,lambda2)
		for j in S[l_m]:
			completion[j] = c_m.pop(0)
			c = completion[j]
			item = items[j]
			wt,wc = item.wt,item.wc
			late = completion[j] - item.due
			t = generate.tard(late)
			item_values[j] = h(t[0],c,wt,wc,lambda1,lambda2)
		delta_p = generate.H(item_values,S[l_p]) - line_values[l_p]
		delta_m = generate.H(item_values,S[l_m]) - line_values[l_m]
		line_values[l_p] += delta_p
		line_values[l_m] += delta_m
		G = G + delta_m + delta_p
	lateness = generate.late(completion,items)
	tardiness = generate.tard(lateness)
	u = tardiness.count(0)
	cv = u/len(tardiness)
	return G,cv,S

if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()		
		input_data_file = open(file_location,'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		m = int(sys.argv[2])
		NR = int(raw_input('iterate time: '))
		lambda1 = float(raw_input('lambda1 = '))
		f = open(".\\result\\batc_"  +str(int(file_location[7:]))+ "_" + str(m) + "_" + str(lambda1),'w')
		G,cv,S= solve(input_data,m,lambda1,NR)
		f.write(str(G) +' ' +str(cv) +'\n' 
			 +str(S))
		f.close()