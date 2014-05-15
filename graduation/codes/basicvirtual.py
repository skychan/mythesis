import sys
sys.path.append(".\\functions")
import generate
import basictabu
import random
from collections import namedtuple
Item = namedtuple("Item", ['process','due','wt','wc'])

def  h(tardiness,completion,wt,wc):			# define the contribution of one item for the obj function
	value = lambda1*wt*tardiness + lambda2*wc*completion
	return value
lambda1 = 0.6
lambda2 = 0.4
def complete_time(S,items):
	c = []
	t = 0
	for j in S:		
		t += items[j].process
		c.append(t)
	return c

def value_generator(S,items):
	completion = complete_time(S,items)
	item = [items[j] for j in S]
	lateness = generate.late(completion,item)
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(len(item)):
		itm = item[j]
		wt,wc = itm.wt,itm.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc)
		item_values.append(value)
	return completion,tardiness,item_values

def same_delta(a,b,items,completion,tardiness):
	delta_c_a = - items[b].process
	delta_c_b = items[a].process
	delta_t_a =  max(completion[a] + delta_c_a - items[a].due ,0) - tardiness[a]
	delta_t_b = max(completion[a] - items[b].due,0) - tardiness[b]
	wt_a,wt_b,wc_a,wc_b = items[a].wt,items[b].wt,items[a].wc,items[b].wc
	delta_a = h(delta_t_a,delta_c_a,wt_a,wc_a)
	delta_b = h(delta_t_b,delta_c_b,wt_b,wc_b)
	return delta_a,delta_b

def diff_delta(S_x,items,line_value):
	c, t, v = value_generator(S_x,items)
	new_value = sum(v)
	delta = new_value - line_value
	return c,t,v,delta

def delta1(S,l_a,l_b,a,b_idx,item_values,items,line_values):
	S_I_1 = S[l_a][:]
	S_I_2 = S[l_b][:]
	S_I_2.insert(b_idx,a)
	S_I_1.remove(a)
	c_I_1,t_I_1,v_I_1,delta_I_1 = diff_delta(S_I_1,items,line_values[l_a])
	c_I_2,t_I_2,v_I_2,delta_I_2 = diff_delta(S_I_2,items,line_values[l_b])
	delta_I = delta_I_1 + delta_I_2
	return S_I_1,S_I_2,c_I_1,c_I_2,t_I_1,t_I_2,v_I_1,v_I_2,c_I_2,delta_I

def delta2(S,l_a,l_b,b,a_idx,item_values,items,line_values):
	S_II_1 = S[l_a][:]
	S_II_2 = S[l_b][:]
	S_II_1.insert(a_idx + 1,b)
	S_II_2.remove(b)
	c_II_1,t_II_1,v_II_1,delta_II_1 = diff_delta(S_II_1,items,line_values[l_a])
	c_II_2,t_II_2,v_II_2,delta_II_2 = diff_delta(S_II_2,items,line_values[l_b])
	delta_II = delta_II_1 + delta_II_2
	return S_II_1,S_II_2,c_II_1,c_II_2,t_II_1,t_II_2,v_II_1,v_II_2,delta_II
	
def delta3(S,l_a,l_b,a,b,a_idx,b_idx,item_values,items,line_values):
	S_III_1 = S[l_a][:]
	S_III_2 = S[l_b][:]
	S_III_1.insert(a_idx,b)
	S_III_1.remove(a)
	S_III_2.insert(b_idx,a)
	S_III_2.remove(b)
	c_III_1,t_III_1,v_III_1,delta_III_1 = diff_delta(S_III_1,items,line_values[l_a])
	c_III_2,t_III_2,v_III_2,delta_III_2 = diff_delta(S_III_2,items,line_values[l_b])
	delta_III = delta_III_1 + delta_III_2
	return S_III_1,S_III_2,c_III_1,c_III_2,t_III_1,t_III_2,v_III_1,v_III_2,delta_III

def tabu(N,NL,S,L,items, completion,tardiness,line_values,item_values):
	TL = [None]*NL
	from_same = []
	from_diff = []
	pairs = generate.pairsets(L)
	completion_temp = completion[:]
	tardiness_temp = tardiness[:]
	line_values_temp = line_values[:]
	item_values_temp = item_values[:]
	delta_star = 0
	Delta = 0
	L_star = L[:]
	m = len(S)
	S_star = [None]*m
	for l in xrange(m):
		S_star[l] = S[l][:]
	# backup all the var
	for k in xrange(N):
		delta = []
		issame = 0
		isdiff = 0
		out = 0
#		random.shuffle(pairs)
		for s in pairs:
			job = list(s)
			a_L_index = max(L.index(job[0]),L.index(job[1]))
			b_L_index = min(L.index(job[0]),L.index(job[1]))
			a = L[a_L_index]
			b = L[b_L_index]
			l_a = generate.find_job(a,S)
			l_b = generate.find_job(b,S)
			a_idx = S[l_a].index(a)
			b_idx = S[l_b].index(b)
			if s not in TL:
				if l_a == l_b:
					delta_a,delta_b = same_delta(a,b,items,completion_temp,tardiness_temp)
					delta_h = delta_a + delta_b
				else:
					# delta_I
					S_I_1,S_I_2,c_I_1,c_I_2,t_I_1,t_I_2,v_I_1,v_I_2,c_I_2,delta_I = delta1(S,l_a,l_b,a,b_idx,item_values,items,line_values_temp)
					# delta_II
					S_II_1,S_II_2,c_II_1,c_II_2,t_II_1,t_II_2,v_II_1,v_II_2,delta_II = delta2(S,l_a,l_b,b,a_idx,item_values,items,line_values_temp)			
					# delta_III
					S_III_1,S_III_2,c_III_1,c_III_2,t_III_1,t_III_2,v_III_1,v_III_2,delta_III = delta3(S,l_a,l_b,a,b,a_idx,b_idx,item_values,items,line_values_temp)

					delta_h = min(delta_I,delta_II,delta_III)
			elif s in from_same:
				break
			else:
				# delta_I
				S_I_1,S_I_2,c_I_1,c_I_2,t_I_1,t_I_2,v_I_1,v_I_2,c_I_2,delta_I = delta1(S,l_a,l_b,a,b_idx,item_values,items,line_values_temp)				
				# delta_II
				S_II_1,S_II_2,c_II_1,c_II_2,t_II_1,t_II_2,v_II_1,v_II_2,delta_II = delta2(S,l_a,l_b,b,a_idx,item_values,items,line_values_temp)
				delta_h = min(delta_I,delta_II)

			if delta == [] or delta_h < delta:
				delta = delta_h
				a_temp,b_temp = a,b
				l_a_temp,l_b_temp = l_a,l_b
				if l_a == l_b:
					S1_temp = S[l_a][:]
					S1_temp = generate.innerswap(S1_temp,a_idx,b_idx)
					c1_temp,t1_temp,v1_temp = value_generator(S1_temp,items)
					S2_temp = []
					c2_temp,t2_temp,v2_temp = [],[],[]
					issame,isdiff = 1,0
				else:
					if delta == delta_I:
						c1_temp,t1_temp,v1_temp = c_I_1,t_I_1,v_I_1
						c2_temp,t2_temp,v2_temp = c_I_2,t_I_2,v_I_2
						S1_temp,S2_temp = S_I_1,S_I_2
						issame,isdiff = 0,0
					elif delta == delta_II:
						c1_temp,t1_temp,v1_temp = c_II_1,t_II_1,v_II_1
						c2_temp,t2_temp,v2_temp = c_II_2,t_II_2,v_II_2
						S1_temp,S2_temp = S_II_1,S_II_2
						issame,isdiff = 0,0
					elif delta == delta_III:
						c1_temp,t1_temp,v1_temp = c_III_1,t_III_1,v_III_1
						c2_temp,t2_temp,v2_temp = c_III_2,t_III_2,v_III_2
						S1_temp,S2_temp = S_III_1,S_III_2
						issame,isdiff = 0,1
		if delta == []:
			break
		L = generate.innerswap(L,L.index(a_temp),L.index(b_temp))
		pairs = generate.pairsets(L)
		change_set = set([a_temp,b_temp])
#		generate.pairsets_update(pairs,change_set)
		if isdiff or issame:
			delete_set = TL.pop(0)
			if delete_set in from_same:
				from_same.remove(delete_set)
			elif delete_set in from_diff:
				from_diff.remove(delete_set)
			TL.append(change_set)
			if isdiff:
				from_diff.append(change_set)
			if issame:
				from_same.append(change_set)
		elif change_set in TL:
			TL[TL.index(change_set)] = None
			from_diff.remove(change_set)
		c_temp = c1_temp + c2_temp
		t_temp = t1_temp + t2_temp
		v_temp = v1_temp + v2_temp
		i = 0
		for j in S1_temp + S2_temp:
			completion_temp[j] = c_temp[i]
			tardiness_temp[j] = t_temp[i]
			item_values_temp[j] = v_temp[i]
			i+=1
		S[l_a_temp] = S1_temp[:]
		line_values_temp[l_a_temp] = sum(v1_temp)
		if l_a_temp != l_b_temp:
			S[l_b_temp] = S2_temp[:]
			line_values_temp[l_b_temp] = sum(v2_temp)
		Delta += delta
		print 'k =  ' +str(k)
		if Delta < delta_star:
			delta_star = Delta
			for l in xrange(m):
				S_star[l] = S[l][:]
			L_star = L[:]
			line_values = line_values_temp[:]
			item_values = item_values_temp[:]
			completion = completion_temp[:]
			tardiness = tardiness_temp[:]
		print Delta, delta_star
	return delta_star,S_star,L_star,line_values,item_values,completion,tardiness

def solve(input_data,N,NL):
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
	m = 5
	S,L,completion = generate.initialization(items,n,m)
	lateness = generate.late(completion,items)
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(len(items)):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc)
		item_values.append(value)
	print 'Initialization done!'

	G = generate.H(item_values,L)
	line_values = []
	for s in S:
		value = generate.H(item_values,s)
		line_values.append(value)

	print 'Initial values done!'
	for l in xrange(m):
		delta,S[l]= basictabu.tabu(144,NL,S[l],items,completion,tardiness)
		G += delta
		line_values[l] += delta
	completion,tardiness,item_values = generate.verify(S,items)
	print 'Initial Tabu Search Done!'
	print sum(item_values)

	delta,S,L,line_values,item_values,completion,tardiness = tabu(N,NL,S,L,items, completion,tardiness,line_values,item_values)
	G += delta
	print G
	print 'Virtual Tabu Search done!'

	completion,tardiness,item_values = generate.verify(S,items)
	print 'while the verify way is:  ' +str(sum(item_values))
	return G

if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
#		output = sys.argv[2].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		N = 2000
		f = open(".\\result\\NL",'w')	
		for NL in range(6,7):
			G = solve(input_data,N,NL)
			f.write('NL = ' +str(NL) + '  G = '+str(G) +'\n')
		f.close()