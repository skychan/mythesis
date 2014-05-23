import sys
import math
sys.path.append(".\\functions")
import generate
import continueatcs
import random
from collections import namedtuple
Item = namedtuple("Item", ['process','release','setup','due','wt','wc'])

def tabu(N,NL,S,l,items,G,completion,line_values,lambda1,lambda2):
	TL = [None]*NL
	pairs = generate.pairsets(S[l])
	completion_temp = completion[:]
	line_values_temp = line_values[:]
	G_star = G
	S_star = []
	test_G = []
	for s in S:
		S_star.append(s[:])
	for k in xrange(N):
#		print k
		test_S = []
		s = random.choice(pairs)
		move = 0
		if s not in TL:
			job = list(s)
			a = job[0]
			b = job[1]
			a_idx = S_star[l].index(a)
			b_idex = S_star[l].index(b)
			S_temp = generate.innerswap(S_star[l],a_idx,b_idex)
			c,v = continueatcs.complete_time(S_star[:l]+[S_temp]+S_star[l+1:],items,lambda1,lambda2)
			G_temp = sum(v)
			if test_G == [] or G_temp < test_G:
				test_G = G_temp
				test_S = S_temp[:]
				completion_temp = c[:]
				line_values_temp = v[:]
				a_star = a
				b_star = b
				move = 1
		else:
			continue
		if move == 0:
			continue
		change_set = set([a_star,b_star])
		generate.pairsets_update(pairs,change_set)
		S_star[l] = test_S[:]
#		completion_temp,line_values_temp = continueatcs.complete_time(S_star,items,lambda1,lambda2)
#		sky,g = generate.Goal()
		TL.pop(0)
		TL.append(change_set)
		if test_G < G_star:
			G_star = test_G
			S[l] = test_S[:]
			line_values = line_values_temp[:]
			completion = completion_temp[:]
#			line_values = line_values_temp[:]
	return G_star,S,line_values,completion

def solve(input_data,lambda1,N,NL,m):
	lambda2  = 1 - lambda1
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
#	print 'Data loaded!'	
	S,L,completion,item_free = generate.initialization_c(items,n,m)
#	print 'Initialization done!'
	line_values,G = generate.Goal(completion,items,S,lambda1,lambda2)
	print 'Initialization values done!'
	print G

	NR = 10
	item_values = continueatcs.h(S,completion,items,lambda1,lambda2)
	G_star = G
	S_star =[]
	for s in S:
		S_star.append(s[:])
#	print item_values
	for k in xrange(NR):
		l_p,l_m = generate.reorder(items,S_star,line_values,item_values)
		completion,line_values = continueatcs.complete_time(S_star,items,lambda1,lambda2)
		G_star = sum(line_values)
		G_star,S_star,line_values,completion = tabu(N,NL,S_star,l_p,items,G_star,completion,line_values,lambda1,lambda2)
#		print S_star,line_values
		G_star,S_star,line_values,completion = tabu(N,NL,S_star,l_m,items,G_star,completion,line_values,lambda1,lambda2)
		item_values = continueatcs.h(S_star,completion,items,lambda1,lambda2)
#		print S_star,line_values
	Rb,_ = generate.balance_rate(completion,S)
	completion,line_values = continueatcs.complete_time(S_star,items,lambda1,lambda2)
	print G_star,sum(item_values),sum(line_values)
	return G_star,Rb


if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		lambda1 = 0.6
		m = int(sys.argv[2])
		NL = 2
		N = 50
		f = open(".\\result\\ctabu_"  +str(int(file_location[7:]))+ "_" + str(m),'w')
		a = [0.4,0.5,0.6]
		for lambda1 in a:
			G,Rb = solve(input_data,lambda1,N,NL,m)
			f.write(str(lambda1) + ' ' + str(G) + ' ' + str(Rb)+'\n')
		f.close()