import sys
import math
sys.path.append(".\\functions")
import generate
from collections import namedtuple
Item = namedtuple("Item", ['process','release','setup','due','wt','wc'])

def  h(S,completion,items,lambda1,lambda2):			# redefine the contribution of one item for the obj function
	n = len(items)
	lateness = generate.late(completion,items)
	value = [None]*n
	Rb,c_max = generate.balance_rate(completion,S)
	Ru = generate.idle_rate(items,completion,c_max,S)
	for s in S:
		l = S.index(s)
		for j in s:
			value[j] = lambda1*(math.fabs(items[j].wt*lateness[j]))/Ru[l] + lambda2*items[j].wc*completion[j]*math.exp(-Rb)
	return value

def complete_time(S,items,lambda1,lambda2):
	n = len(items)
	c = [None]*n
	f = [None]*n
	for s in S:
		t = 0
		for j in s:
			item = items[j]
			if s.index(j) == 0:
				f[j] = max(item.release - item.setup,0)
			else:
				f[j] = max(item.release - item.setup - c[s[s.index(j)-1]],0)
			t += item.process + item.setup + f[j]
			c[j] = t
	item_values = h(S,c,items,lambda1,lambda2)
	line_values = []
	for s in S:
		v = [item_values[j] for j in s]
		line_values.append(sum(v))
	return c,line_values

def ATCS(items,S,m):					# use the ATCS rule
	J = S[:]
	S = []
	t = 0
	c = []
	n = len(items)
	f = []
	k_1,k_2 = generate.estimate(m,items)
	while J:
		p = [items[j].process for j in J]
		r = [items[j].release for j in J]
		d = [items[j].due for j in J]
		s = [items[j].setup for j in J]
		wt = [items[j].wt for j in J]
		orderidx = generate.Idx_c(t,p,s,d,wt,k_1,k_2)
		j_star = J[orderidx.index(max(orderidx))]
		S.append(j_star)
		J.remove(j_star)
		if len(S) == 1:
			f.append(max(items[j_star].release - items[j_star].setup,0))
		else:
			f.append(max(items[j_star].release - items[j_star].setup - c[ -1],0))
		t = t + items[j_star].process + items[j_star].setup + f[-1]
		c.append(t)
	return S,c

def solve(input_data,m,lambda1):
	lambda2 = 1 - lambda1
	Data = input_data.split('\n')					# load data
	n = len(Data) -1						# get the amount of items
	items = []	
	for j in xrange(n):
		data = Data[j]
		parts = data.split()
		p = int(parts[0])					# get the process time
		r = int(parts[1])						# get the release time
		s = int(parts[2])						# get the setup time
		d = int(parts[3])					# get the due date
		wt = int(parts[4])					# get the tardiness weights
		wc = int(parts[5])					# get the completion weights
		items.append(Item(p,r,s,d,wt,wc))			# combine those item data
	print 'Data loaded!'	
	S,L,completion,item_free = generate.initialization_c(items,n,m)
	print 'Initialization done!'
	line_values,G = generate.Goal(completion,items,S,lambda1,lambda2)
	print 'Initialization values done!'
	print G

	NR = 19
	item_values = h(S,completion,items,lambda1,lambda2)
	for k in xrange(NR):
		l_p,l_m = generate.reorder(items,S,line_values,item_values)
		S[l_p],c_p = ATCS(items,S[l_p],m)
		S[l_m],c_m = ATCS(items,S[l_m],m)
		completion,line_values = complete_time(S,items,lambda1,lambda2)
		item_values = h(S,completion,items,lambda1,lambda2)
		G = sum(line_values)
	Rb,c= generate.balance_rate(completion,S)
	return G,Rb
	
if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		m = int(sys.argv[2])
		lambda1 = float(raw_input('lambda1 = '))
		f = open(".\\result\\catcs_"  +str(int(file_location[7:]))+ "_" + str(m) + "_" + str(lambda1),'w')
		G,Rb = solve(input_data,m,lambda1)
		f.write(str(G) +' ' +str(Rb)+ '\n')
		f.close()