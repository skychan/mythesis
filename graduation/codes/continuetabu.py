import sys
import math
sys.path.append(".\\functions")
import generate
from collections import namedtuple
Item = namedtuple("Item", ['process','release','setup','due','wt','wc'])

lambda1 = 0.6
lambda2 = 0.4
sigma = 0.5
def  h(S,completion,items,lambda1,lambda2):			# define the contribution of one item for the obj function
	n = len(items)
	lateness = generate.late(completion,items)
	value = [None]*n
	for s in S:
		for j in s:
#			value[j] = lambda1*(math.sqrt(items[j].wt*lateness[j]**2)) + lambda2*items[j].wc*completion[j]**8
			value[j] = completion[j] + 4*lateness[j]
	return value

def complete_time(S,items):
	n = len(items)
	c = [None]*n
	for s in S:
		t = 0
		for j in s:
			t += items[j].process
			c[j] = t
	return c

def value_generator(S,items):
	completion = complete_time(S,items)
	lateness = generate.late(completion,items)
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(len(items)):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc)
		item_values.append(value)
	return completion,tardiness,item_values
	

def tabu(N,NL,S,items,G,completion,lambda1,lambda2,sigma):
	TL = [None]*NL
	pairs = generate.pairsets(S)
	completion_temp = completion[:]
	G_star = G
	S_star = S[:]
	for k in xrange(N):
		test_G = []
		test_S = []
		test_values= []
		for s in pairs:
			if s not in TL:
				job = list(s)
				a = job[0]
				b = job[1]
				a_idx = S.index(a)
				b_idex = S.index(b)
				S_temp = generate.innerswap(S,a_idx,b_idex)
				line_values_temp,G_temp = generate.Goal(completion,items,S,lambda1,lambda2,sigma)
				if test_G == [] or G_temp < test_G:
					test_G = G_temp
					test_S = S_temp[:]
					test_values = line_values_temp[:]
					a_star = a
					b_star = b
		if test_G == []:
			break
		change_set = set([a_star,b_star])
		generate.pairsets_update(pairs,change_set)
		TL.pop(0)
		TL.append(change_set)
		if test_G < G_star:
			G_star = test_G
			S_star = test_S[:]
			line_values = line_values_temp[:]
	return G_star,S_star,line_values

def solve(input_data):
	Data = input_data.split('\n')					# load data
	n = len(Data) -1							# get the amount of items
	m = 5
	items = []	
	for j in xrange(n):
		data = Data[j]
		parts = data.split()
		p = int(parts[0])						# get the process time
		r = int(parts[1])						# get the release time
		s = int(parts[2])						# get the setup time
		d = int(parts[3])						# get the due date
		wt = int(parts[4])						# get the tardiness weights
		wc = int(parts[5])						# get the completion weights
		items.append(Item(p,r,s,d,wt,wc))			# combine those item data
	print 'Data loaded!'	
	S,L,completion,item_free = generate.initialization_c(items,n,m)
	print 'Initialization done!'
	line_values,G = generate.Goal(completion,items,S,lambda1,lambda2,sigma)
	print 'Initialization values done!'
	print G

	NR = 1
	N = 10
	NL = 2
	item_values = h(S,completion,items,lambda1,lambda2)
	for k in xrange(NR):
		l_p,l_m = generate.reorder(items,S,line_values,item_values)
		print l_p,l_m
		G_star,S_star,line_values = tabu(N,NL,S[l_p],items,G,completion,lambda1,lambda2,sigma)
		G_star,S_star,line_values = tabu(N,NL,S[l_m],items,G_star,completion,lambda1,lambda2,sigma)

	print G

if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		solve(input_data)