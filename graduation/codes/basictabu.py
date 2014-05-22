import sys
sys.path.append(".\\functions")
import generate
from collections import namedtuple
Item = namedtuple("Item", ['process','due','wt','wc'])

def  h(tardiness,completion,wt,wc,lambda1,lambda2):			# define the contribution of one item for the obj function
	value = lambda1*wt*tardiness + lambda2*wc*completion
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

def value_generator(S,items,lambda1,lambda2):
	completion = complete_time(S,items)
	lateness = generate.late(completion,items)
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(len(items)):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc,lambda1,lambda2)
		item_values.append(value)
	return completion,tardiness,item_values
	

def tabu(N,NL,S,items, completion,tardiness,lambda1,lambda2):
	TL = [None]*NL
#	value = generate.H(item_values,S)
	pairs = generate.pairsets(S)
	completion_temp = completion[:]
	tardiness_temp = tardiness[:]
	delta_star = 0
	Delta = 0
	S_star = S[:]
	for k in xrange(N):
		delta = []
		for s in pairs:
			if s not in TL:
				job = list(s)
				a = S[max(S.index(job[0]),S.index(job[1]))]
				b = S[min(S.index(job[0]),S.index(job[1]))]
				delta_c_a = - items[b].process
				delta_c_b = items[a].process
				delta_t_a = - min(items[b].process,tardiness_temp[a])
				delta_t_b = max(completion_temp[a] - items[b].due,0) - tardiness_temp[b]
				wt_a,wt_b,wc_a,wc_b = items[a].wt,items[b].wt,items[a].wc,items[b].wc
				delta_a = h(delta_t_a,delta_c_a,wt_a,wc_a,lambda1,lambda2)
				delta_b = h(delta_t_b,delta_c_b,wt_b,wc_b,lambda1,lambda2)
				delta_h = delta_a + delta_b
				if delta == []:
					delta = delta_h
					delta_a_star = delta_a
					delta_b_star = delta_b 
					a_star,b_star = a,b
				elif delta_h < delta:
					delta = delta_h
					delta_a_star = delta_a
					delta_b_star = delta_b 
					a_star,b_star = a,b
		if delta == []:
			break
		a = S.index(a_star)
		b = S.index(b_star)
		S = generate.innerswap(S,a,b)
		change_set = set([a_star,b_star])
		generate.pairsets_update(pairs,change_set)
		TL.pop(0)
		TL.append(change_set)
		completion_temp[a_star] -= items[b_star].process
		completion_temp[b_star] += items[a_star].process
		tardiness_temp[a_star] = max(completion_temp[a_star] - items[a_star].due,0)
		tardiness_temp[b_star] = max(completion_temp[b_star] - items[b_star].due,0)
		Delta += delta
		if Delta < delta_star:
			delta_star = Delta
			S_star = S[:]
	return delta_star,S_star

def solve(input_data,m,lambda1):
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

	completion,tardiness,item_values = value_generator(S,items,lambda1,lambda2)
	G = generate.H(item_values,L)
	line_values = []
	for s in S:
		value = generate.H(item_values,s)
		line_values.append(value)

	print 'Initial values done!'

	N = 1500
	NL = 2
	for l in xrange(m):
		delta,S[l]= tabu(N,NL,S[l],items,completion,tardiness,lambda1,lambda2)
		G += delta
		line_values[l] += delta
	completion,tardiness,item_values = value_generator(S,items,lambda1,lambda2)
	print G
	print 'Initial Tabu Search done!'
	n = len(items)
	co = [None]*n
	for s in S:
		t = 0
		for j in s:
			t += items[j].process
			co[j] = t
	la = generate.late(co,items)
	ta = generate.tard(la)
	v = []
	for j in xrange(len(items)):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = ta[j],co[j]
		value = h(t,c,wt,wc,lambda1,lambda2)
		v.append(value)
	print sum(v)

	NR = 3
	value = G
	S_temp = [None]*m
	for l in xrange(m):
		S_temp[l] = S[l][:]
	line_values_temp = line_values[:]
	item_values_temp = item_values[:]
	print line_values_temp
	for k in xrange(NR):		
		l_p,l_m = generate.reorder(items,S_temp,line_values_temp,item_values_temp)
		completion_temp,tardiness_temp,item_values_temp = value_generator(S_temp,items,lambda1,lambda2)
		line_values_temp[l_p] = generate.H(item_values_temp,S_temp[l_p])
		line_values_temp[l_m] = generate.H(item_values_temp,S_temp[l_m])
		delta_p,S_temp[l_p] = tabu(N,NL,S_temp[l_p],items,completion_temp,tardiness_temp,lambda1,lambda2)
		delta_m,S_temp[l_m] = tabu(N,NL,S_temp[l_m],items,completion_temp,tardiness_temp,lambda1,lambda2)
		line_values_temp[l_p] += delta_p
		line_values_temp[l_m] += delta_m
		value = generate.H(item_values_temp,L)
		value = value + delta_m + delta_p
		print value,G
		if value < G:
			G = value
			line_values = line_values_temp[:]
			completion,tardiness,item_values = value_generator(S_temp,items,lambda1,lambda2)
			for l in xrange(m):
				S[l] = S_temp[l][:]
		print 'hello:' + str(k)
	GG = generate.H(item_values,L)
	print GG
	n = len(items)
	co = [None]*n
	for s in S:
		t = 0
		for j in s:
			t += items[j].process
			co[j] = t
	la = generate.late(co,items)
	ta = generate.tard(la)
	v = []
	for j in xrange(len(items)):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = ta[j],co[j]
		value = h(t,c,wt,wc,lambda1,lambda2)
		v.append(value)
	print sum(v)
	g = open(".\\result\\draw_tabu" ,'w')
	for s in S:
		cc = [completion[j] for j in s]
		tt = [tardiness[j] for j in s]
		g.write(str(s) + '\n' + str(cc) + '\n' + str(tt) + '\n')
		g.write('\n')
	g.close()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
#		output = sys.argv[2].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		m = 5
		lambda1 = 0.6
		solve(input_data,m,lambda1)
