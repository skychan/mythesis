import sys
sys.path.append(".\\functions")
import generate
import continueatcs
import continuetabu
import random
from collections import namedtuple
Item = namedtuple("Item", ['process','release','setup','due','wt','wc'])

lambda1 = 0.6
lambda2 = 0.4
sigma = 0.5

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

def same_S(S,l,a_idx,b_idx):
	S_t = []
	for s in S:
		S_t.append(s[:])
	S_t[l] = generate.innerswap(S_t[l],a_idx,b_idx)
	return S_t

def test_G(items,S,lambda1,lambda2,sigma):
	c_temp,v_temp = continueatcs.complete_time(S,items,lambda1,lambda2,sigma)
	_,G = generate.Goal(c_temp,items,S,lambda1,lambda2,sigma)
	return G

def diff1_S(S,l_a,l_b,a,b_idx):
	S_t = []
	for s in S:
		S_t.append(s[:])
	S_1 = S_t[l_a][:]
	S_2 = S_t[l_b][:]
	S_2.insert(b_idx,a)
	S_1.remove(a)
	S_t[l_a] = S_1
	S_t[l_b] = S_2
	return S_t

def diff2_S(S,l_a,l_b,b,a_idx):
	S_t = []
	for s in S:
		S_t.append(s[:])
	S_1 = S[l_a][:]
	S_2 = S[l_b][:]
	S_1.insert(a_idx + 1,b)
	S_2.remove(b)
	S_t[l_a] = S_1
	S_t[l_b] = S_2	
	return S_t

def diff3_S(S,l_a,l_b,a,b,a_idx,b_idx):
	S_t = []
	for s in S:
		S_t.append(s[:])
	S_1 = S[l_a][:]
	S_2 = S[l_b][:]
	S_1.insert(a_idx,b)
	S_1.remove(a)
	S_2.insert(b_idx,a)
	S_2.remove(b)
	S_t[l_a] = S_1
	S_t[l_b] = S_2	
	return S_t

def tabu(N,NL,S,L,items,G,lambda1,lambda2,sigma):
	TL = [None]*NL
	from_same = []
	from_diff = []
	pairs = generate.pairsets(L)
	G_star = G
	L_star = L[:]
#	m = len(S)
#	S_star = [None]*m
#	for l in xrange(m):
#		S_star[l] = S[l][:]
	# backup all the var
	for k in xrange(N):
		G_test = 0
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
					# a <--> b
					S_temp = same_S(S,l_a,a_idx,b_idx)
					G_temp = test_G(items,S_temp,lambda1,lambda2,sigma)
				else:
					# a -> b's
					S_temp_1 = diff1_S(S,l_a,l_b,a,b_idx)
					G_temp_1 = test_G(items,S_temp_1,lambda1,lambda2,sigma)
					# b -> a's
					S_temp_2 = diff2_S(S,l_a,l_b,b,a_idx)
					G_temp_2 = test_G(items,S_temp_2,lambda1,lambda2,sigma)		
					# a <--> b
					S_temp_3 = diff3_S(S,l_a,l_b,a,b,a_idx,b_idx)
					G_temp_3 = test_G(items,S_temp_3,lambda1,lambda2,sigma)

					G_temp = min(G_temp_1,G_temp_2,G_temp_3)
			elif s in from_same:
				break
			else:
				# a -> b's
				S_temp_1 = diff1_S(S,l_a,l_b,a,b_idx)
				G_temp_1 = test_G(items,S_temp_1,lambda1,lambda2,sigma)
				# b -> a's
				S_temp_2 = diff2_S(S,l_a,l_b,b,a_idx)
				G_temp_2 = test_G(items,S_temp_2,lambda1,lambda2,sigma)	
				G_temp = min(G_temp_1,G_temp_2)

			if G_test == 0 or G_temp < G_test:
				G_test = G_temp
				a_temp,b_temp = a,b
				l_a_temp,l_b_temp = l_a,l_b
				if l_a == l_b:
					S_star = S_temp
					issame,isdiff = 1,0
				else:
					if G_temp == G_temp_1:
						S_star = S_temp_1
						issame,isdiff = 0,0
					elif G_temp == G_temp_2:
						S_star = S_temp_2
						issame,isdiff = 0,0
					elif G_temp == G_temp_3:
						S_star = S_temp_3
						issame,isdiff = 0,1
		if G_test == 0:
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
		S = S_star
		G = G_test
		print G
		print 'k =  ' +str(k)
		if G < G_star:
			G_star = G
			S_c = []
			for s in S:
				S_c.append(s[:]) 
			L_star = L[:]
	return G_star,S_c

def solve(input_data,N,NL):
	Data = input_data.split('\n')					# load data
	n = len(Data) -1						# get the amount of items
	items = []
	for j in xrange(n):
		data = Data[j]
		parts = data.split()
		p = int(parts[0])					# get the process time
		r = int(parts[1])
		s = int(parts[2])						# get the setup time
		d = int(parts[3])					# get the due date
		wt = int(parts[4])					# get the tardiness weights
		wc = int(parts[5])					# get the completion weights
		items.append(Item(p,r,s,d,wt,wc))			# combine those item data
	print 'Data loaded!'	
	m = 5
	S,L,completion,item_free = generate.initialization_c(items,n,m)
	print 'Initialization done!'
	line_values,G = generate.Goal(completion,items,S,lambda1,lambda2,sigma)
	print 'Initial values done!'

	# initial tabu
	Nt = 144
	for l in xrange(m):
		G,S,line_values,completion = continuetabu.tabu(Nt,NL,S,l,items,G,completion,line_values,lambda1,lambda2,sigma)
	print 'Initial Tabu Search Done!'

	G,S = tabu(N,NL,S,L,items,G,lambda1,lambda2,sigma)
	print G
	print 'Virtual Tabu Search done!'

#	completion,tardiness,item_values = generate.verify(S,items)
#	print 'while the verify way is:  ' +str(sum(item_values))
#	return G

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