from __future__ import division
import sys
sys.path.append(".\\functions")
import generate
import basictabu
import random
from collections import namedtuple
Item = namedtuple("Item", ['process','due','wt','wc'])

def  h(tardiness,completion,wt,wc,lambda1,lambda2):			# define the contribution of one item for the obj function
	value = lambda1*wt*tardiness + lambda2*wc*completion
	return value
def complete_time(S,items):
	c = []
	t = 0
	for j in S:		
		t += items[j].process
		c.append(t)
	return c

def value_generator(S,items,lambda1,lambda2):
	completion = complete_time(S,items)
	item = [items[j] for j in S]
	lateness = generate.late(completion,item)
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(len(item)):
		itm = item[j]
		wt,wc = itm.wt,itm.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc,lambda1,lambda2)
		item_values.append(value)
	return completion,tardiness,item_values

def same_delta(a,b,S,items,line_value,lambda1,lambda2):
	K = generate.innerswap(S,S.index(a),S.index(b))
	c, t, v = value_generator(K,items,lambda1,lambda2)
	new_value = sum(v)
	delta = new_value - line_value
	return K,c,t,v,delta

def diff_delta(S_x,items,line_value,lambda1,lambda2):
	c, t, v = value_generator(S_x,items,lambda1,lambda2)
	new_value = sum(v)
	delta = new_value - line_value
	return c,t,v,delta

def delta1(S,l_a,l_b,a,b_idx,item_values,items,line_values,lambda1,lambda2):
	S_I_1 = S[l_a][:]
	S_I_2 = S[l_b][:]
	S_I_2.insert(b_idx,a)
	S_I_1.remove(a)
	c_I_1,t_I_1,v_I_1,delta_I_1 = diff_delta(S_I_1,items,line_values[l_a],lambda1,lambda2)
	c_I_2,t_I_2,v_I_2,delta_I_2 = diff_delta(S_I_2,items,line_values[l_b],lambda1,lambda2)
	delta_I = delta_I_1 + delta_I_2
	return S_I_1,S_I_2,c_I_1,c_I_2,t_I_1,t_I_2,v_I_1,v_I_2,c_I_2,delta_I

def delta2(S,l_a,l_b,b,a_idx,item_values,items,line_values,lambda1,lambda2):
	S_II_1 = S[l_a][:]
	S_II_2 = S[l_b][:]
	S_II_1.insert(a_idx + 1,b)
	S_II_2.remove(b)
	c_II_1,t_II_1,v_II_1,delta_II_1 = diff_delta(S_II_1,items,line_values[l_a],lambda1,lambda2)
	c_II_2,t_II_2,v_II_2,delta_II_2 = diff_delta(S_II_2,items,line_values[l_b],lambda1,lambda2)
	delta_II = delta_II_1 + delta_II_2
	return S_II_1,S_II_2,c_II_1,c_II_2,t_II_1,t_II_2,v_II_1,v_II_2,delta_II
	
def delta3(S,l_a,l_b,a,b,a_idx,b_idx,item_values,items,line_values,lambda1,lambda2):
	S_III_1 = S[l_a][:]
	S_III_2 = S[l_b][:]
	S_III_1.insert(a_idx,b)
	S_III_1.remove(a)
	S_III_2.insert(b_idx,a)
	S_III_2.remove(b)
	c_III_1,t_III_1,v_III_1,delta_III_1 = diff_delta(S_III_1,items,line_values[l_a],lambda1,lambda2)
	c_III_2,t_III_2,v_III_2,delta_III_2 = diff_delta(S_III_2,items,line_values[l_b],lambda1,lambda2)
	delta_III = delta_III_1 + delta_III_2
	return S_III_1,S_III_2,c_III_1,c_III_2,t_III_1,t_III_2,v_III_1,v_III_2,delta_III

def tabu(N,NL,S,L,items, completion,tardiness,line_values,item_values,G,lambda1,lambda2):
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
#	f = open(".\\result\\888",'w')
#	ly = open(".\\result\\ccc",'w')
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
					S_k,c_k,t_k,v_k,delta_h = same_delta(a,b,S[l_a],items,line_values_temp[l_a],lambda1,lambda2)
#					if k == 16:
#						ly.write()
				else:
					# delta_I
					S_I_1,S_I_2,c_I_1,c_I_2,t_I_1,t_I_2,v_I_1,v_I_2,c_I_2,delta_I = delta1(S,l_a,l_b,a,b_idx,item_values,items,line_values_temp,lambda1,lambda2)
					# delta_II
					S_II_1,S_II_2,c_II_1,c_II_2,t_II_1,t_II_2,v_II_1,v_II_2,delta_II = delta2(S,l_a,l_b,b,a_idx,item_values,items,line_values_temp,lambda1,lambda2)
					# delta_III
					S_III_1,S_III_2,c_III_1,c_III_2,t_III_1,t_III_2,v_III_1,v_III_2,delta_III = delta3(S,l_a,l_b,a,b,a_idx,b_idx,item_values,items,line_values_temp,lambda1,lambda2)
					delta_h = min(delta_I,delta_II,delta_III)
			elif s in from_same:
				continue
			else:
				# delta_i
				S_i_1,S_i_2,c_i_1,c_i_2,t_i_1,t_i_2,v_i_1,v_i_2,c_i_2,delta_i = delta1(S,l_a,l_b,a,b_idx,item_values,items,line_values_temp,lambda1,lambda2)
				# delta_ii
				S_ii_1,S_ii_2,c_ii_1,c_ii_2,t_ii_1,t_ii_2,v_ii_1,v_ii_2,delta_ii = delta2(S,l_a,l_b,b,a_idx,item_values,items,line_values_temp,lambda1,lambda2)
				delta_h = min(delta_i,delta_ii)
			if delta == [] or delta_h < delta:
				delta = delta_h
				a_temp,b_temp = a,b
				l_a_temp,l_b_temp = l_a,l_b
				if l_a == l_b:
					S_temp = S_k[:]
					c_temp,t_temp,v_temp = c_k,t_k,v_k
					issame,isdiff = 1,0
					out = 0
				else:
					if s in TL:
						out = 1
						issame,isdiff = 0,0
						if delta == delta_i:
							c1_temp,t1_temp,v1_temp = c_i_1,t_i_1,v_i_1
							c2_temp,t2_temp,v2_temp = c_i_2,t_i_2,v_i_2
							S1_temp,S2_temp = S_i_1,S_i_2
						elif delta == delta_ii:
							c1_temp,t1_temp,v1_temp = c_ii_1,t_ii_1,v_ii_1
							c2_temp,t2_temp,v2_temp = c_ii_2,t_ii_2,v_ii_2
							S1_temp,S2_temp = S_ii_1,S_ii_2
#						ly.write('l_a = ' + str(l_a) + ' l_b = ' + str(l_b) + '\n')
					else:
						out = 0
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
			continue
		L = generate.innerswap(L,L.index(a_temp),L.index(b_temp))
		pairs = generate.pairsets(L)
		change_set = set([a_temp,b_temp])
#		ly.write('TL  = ' + str(TL) + '\n')
#		ly.write('Same  = ' + str(from_same) + '\n')
#		ly.write('Diff  = ' + str(from_diff) + '\n')
		if out:
			TL[TL.index(change_set)] = None
			from_diff.remove(change_set)
		delete_set = TL.pop(0)
		if delete_set in from_same:
			from_same.remove(delete_set)
		elif delete_set in from_diff:
			from_diff.remove(delete_set)
		if isdiff or issame:			
			TL.append(change_set)
			if isdiff:
				from_diff.append(change_set)
			if issame:
				from_same.append(change_set)
		else:
			TL.append(None)
		if l_a_temp != l_b_temp:
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
			S[l_b_temp] = S2_temp[:]
			line_values_temp[l_a_temp] = sum(v1_temp)
			line_values_temp[l_b_temp] = sum(v2_temp)
#			ly.write('l_a_temp = '+str(l_a_temp) +' a = ' + str(a_temp) + '\n'+ str(S1_temp) + '\n')
#			ly.write('l_b_temp = '+str(l_b_temp) +' b = ' + str(b_temp) + '\n'+ str(S2_temp) + '\n')
		else:
			S[l_a_temp] = S_temp[:]
			line_values_temp[l_a_temp] = sum(v_temp)
#			ly.write('l_a_temp = l_b_temp = '+str(l_a_temp) +' a = ' + str(a_temp) +' b = '  + str(b_temp) + '\n'+ str(S_temp) + '\n')
		TL,from_same,from_diff = generate.TL_update(TL,from_same,from_diff,S)
#		ly.write(str(S) + '\n')
		Delta += delta
#		sky = []
#		for s in S:
#			sky += s
#		if len(set(sky)) == len(items):
#			print 'Yes!'
#		else:
#			print 'No!'
#			print len(set(sky))
#		print 'k =  ' +str(k)
		if Delta < delta_star:
			delta_star = Delta
			for l in xrange(m):
				S_star[l] = S[l][:]
			L_star = L[:]
			line_values = line_values_temp[:]
			item_values = item_values_temp[:]
			completion = completion_temp[:]
			tardiness = tardiness_temp[:]
#		f.write(str(k+1) +'  '+ str(delta_star+G) +'\n')			
#		print Delta, delta_star+G
#	f.close()
#	ly.close()
	return delta_star,S_star,L_star,line_values,item_values,completion,tardiness

def solve(input_data,N,NL,m,lambda1):
	lambda2 = 1 - lambda1
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
#	print 'Data loaded!'	
	S,L,completion = generate.initialization(items,n,m)
	lateness = generate.late(completion,items)
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(len(items)):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc,lambda1,lambda2)
		item_values.append(value)
#	print 'Initialization done!'

	G = generate.H(item_values,L)
	line_values = []
	for s in S:
		value = generate.H(item_values,s)
		line_values.append(value)

#	print 'Initial values done!'
	for l in xrange(m):
		delta,S[l]= basictabu.tabu(1500,NL,S[l],items,completion,tardiness,lambda1,lambda2)
		G += delta
		line_values[l] += delta
	completion,tardiness,item_values = generate.verify(S,items,lambda1,lambda2)
#	print 'Initial Tabu Search Done!'
#	print G

	delta,S,L,line_values,item_values,completion,tardiness = tabu(N,NL,S,L,items, completion,tardiness,line_values,item_values,G,lambda1,lambda2)
	G += delta
#	print G
#	print 'Virtual Tabu Search done!'
#	sky = open(".\\result\\draw",'w')
#	for s in S:
#		cc = [completion[j] for j in s]
#		tt = [tardiness[j] for j in s]
#		sky.write(str(s) + '\n' + str(cc) + '\n' + str(tt) + '\n')
#	sky.close()

	completion,tardiness,item_values = generate.verify(S,items,lambda1,lambda2)
#	print 'while the verify way is:  ' +str(sum(item_values))
	return G

if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		m = int(sys.argv[2])
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		N = 1850
		NL = 61
		a = [0.4,0.5,0.6]
		g = open(".\\result\\lambda1_200_5",'w')
		for lambda1 in a:
			G = solve(input_data,N,NL,m,lambda1)
			g.write(str(lambda1) + ' ' + str(G) +'\n')
#			print N
		g.close()
