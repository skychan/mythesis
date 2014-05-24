from __future__ import division
import sys
sys.path.append(".\\functions")
import generate
import continueatcs
import continuetabu
import random
from collections import namedtuple
Item = namedtuple("Item", ['process','release','setup','due','wt','wc'])

def same_S(S,l,a_idx,b_idx):
	S_t = []
	for s in S:
		S_t.append(s[:])
	S_t[l] = generate.innerswap(S_t[l],a_idx,b_idx)
	return S_t

def test_G(items,S,lambda1,lambda2):
	c_temp,v_temp = continueatcs.complete_time(S,items,lambda1,lambda2)
#	_,G = generate.Goal(c_temp,items,S,lambda1,lambda2)
	return sum(v_temp)

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

def tabu(N,NL,S,L,items,G,lambda1,lambda2):
	TL = [None]*NL
	from_same = []
	from_diff = []
	pairs = generate.pairsets(L)
	G_star = G
	L_star = L[:]
	S_c = []
	S_ori = []
	for s in S:
		S_ori.append(s[:])
		S_c.append(s[:])
#	m = len(S)
#	S_star = [None]*m
#	for l in xrange(m):
#		S_star[l] = S[l][:]
	# backup all the var
	G_test = 0
	for k in xrange(N):
		issame = 0
		isdiff = 0
		out = 0
		s = random.choice(pairs)
		move = 0
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
				G_temp = test_G(items,S_temp,lambda1,lambda2)
			else:
				# a -> b's
				S_temp_1 = diff1_S(S,l_a,l_b,a,b_idx)
				G_temp_1 = test_G(items,S_temp_1,lambda1,lambda2)
				# b -> a's
				S_temp_2 = diff2_S(S,l_a,l_b,b,a_idx)
				G_temp_2 = test_G(items,S_temp_2,lambda1,lambda2)
				# a <--> b
				S_temp_3 = diff3_S(S,l_a,l_b,a,b,a_idx,b_idx)
				G_temp_3 = test_G(items,S_temp_3,lambda1,lambda2)
				G_temp = min(G_temp_1,G_temp_2,G_temp_3)
		elif s in from_same:
			continue
		elif s in from_diff:
			# a -> b's
			S_temp_1 = diff1_S(S,l_a,l_b,a,b_idx)
			G_temp_1 = test_G(items,S_temp_1,lambda1,lambda2)
			# b -> a's
			S_temp_2 = diff2_S(S,l_a,l_b,b,a_idx)
			G_temp_2 = test_G(items,S_temp_2,lambda1,lambda2)	
			G_temp = min(G_temp_1,G_temp_2)
		if G_test == 0 or G_temp < G_test:
#			print G_temp
			move = 1
			G_test = G_temp
			a_temp,b_temp = a,b
			l_a_temp,l_b_temp = l_a,l_b
			if l_a == l_b:
				S_star = S_temp
				issame,isdiff = 1,0
				out = 0
			else:
				if s in TL:
					out = 1
					issame,isdiff = 0,0
					if G_temp == G_temp_1:
						S_star = S_temp_1
					elif G_temp == G_temp_2:
						S_star = S_temp_2
				else:
					out = 0
					if G_temp == G_temp_1:
						S_star = S_temp_1
						issame,isdiff = 0,0
					elif G_temp == G_temp_2:
						S_star = S_temp_2
						issame,isdiff = 0,0
					elif G_temp == G_temp_3:
						S_star = S_temp_3
						issame,isdiff = 0,1
		if move == 0:
			continue
		L = generate.innerswap(L,L.index(a_temp),L.index(b_temp))
		pairs = generate.pairsets(L)
		change_set = set([a_temp,b_temp])
#		generate.pairsets_update(pairs,change_set)
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
		S = S_star
		G = G_test
#		print G
#		print 'k =  ' +str(k)
		TL,from_same,from_diff = generate.TL_update(TL,from_same,from_diff,S)
		if G < G_star:
			G_star = G
			l =0 
			for s in S:
				S_c[l][:] = s[:]
				l += 1
			L_star = L[:]
#	if G_star < G:
	return G_star,S_c
#	else:
#		return G,S_ori

def solve(input_data,N,NL,lambda1,m):
	lambda2 = 1 - lambda1
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
#	print 'Data loaded!'	
	S,L,completion,item_free = generate.initialization_c(items,n,m)
	print 'Initialization done!'
	line_values,G = generate.Goal(completion,items,S,lambda1,lambda2)
#	print G
	print 'Initial values done!'

	# initial tabu
	
	for l in xrange(m):
		G,S,line_values,completion = continuetabu.tabu(N,NL,S,l,items,G,completion,line_values,lambda1,lambda2)
#		print G,sum(line_values)
#	print 'Initial Tabu Search Done!'

	G,S = tabu(N,NL,S,L,items,G,lambda1,lambda2)
	c,v = continueatcs.complete_time(S,items,lambda1,lambda2)
#	print G,sum(line_values)
	Rb,_ = generate.balance_rate(completion,S)
	print G,sum(v)


	return G,Rb
#	print 'Virtual Tabu Search done!'

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
		m = int(sys.argv[2])
		N = 3
#		lambda1 = 0.6
		NL = 2
		a = [0.4,0.5,0.6]
		f = open(".\\result\\cv_"  +str(int(file_location[7:]))+ "_" + str(m),'w')
		for lambda1 in a:
			G = []
			for i in xrange(3):
				G_temp,Rb_temp = solve(input_data,N,NL,lambda1,m)
				if G == [] or G_temp<G:
					G = G_temp
					Rb = Rb_temp
			f.write(str(lambda1) +' ' + str(G) +' ' +str(Rb)+ '\n')
		f.close()
#		N = 1
#		lambda1 = 0.6
#		NL = 2
#		G,Rb = solve(input_data,N,NL,lambda1,m)
