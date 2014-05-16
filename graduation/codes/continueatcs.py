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

def ATCS(items,S,m):
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

#	f = open(".\\result\\result_" +str(load),'w')
#	f.write('Initial Solution is :\n')
#	for k in range(len(S)):
#		f.write('S_'+str(k)+': '+str(S[k])+'\n')
#	f.write('And the obj value is: '+ str(G)+'\n')
	
#	g = open(".\\result\\sky" ,'w')
#	for k in range(len(S)):
#		g.write(str(S[k]) + ' ' +str(line_values[k]) +'\n')
#	g.write('let us check\n')
	print line_values
	NR = 20
	item_values = h(S,completion,items,lambda1,lambda2)
	for k in xrange(NR):
#		g.write(str(k)+':\n')
		l_p,l_m = generate.reorder(items,S,line_values,item_values)
		print l_p,l_m
		S[l_p],c_p = ATCS(items,S[l_p],m)
		S[l_m],c_m = ATCS(items,S[l_m],m)
		S_pm = S[l_p] + S[l_m]
		c = c_p + c_m
		for j in S_pm:
			completion[j] = c.pop(0)
		line_values,G = generate.Goal(completion,items,S,lambda1,lambda2,sigma)
		print line_values
		print G
	print G
	
#		for k in range(len(S)):
#			g.write(str(S[k]) + ' ' +str(line_values[k]) +'\n')
#	g.close()
#	f.write('Final Solution is :\n')
#	for k in range(len(S)):
#		f.write('S_'+str(k)+': '+str(S[k])+'\n')
#	f.write('And the obj value is: '+ str(G)+'\n')
#	f.close()
if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
#		type_location = sys.argv[2].strip()
#		data_type_file = open(file_location, 'r')
#		data_type = ''.join(data_type_file.readlines())
#		data_type_file.close()
#		numbers = data_type.split('\n')
#		for i in range(len(numbers)):
#			input_data_file = open(".\\data\\" + str(numbers[i]),'r')
#			input_data = ''.join(input_data_file.readlines())
#			input_data_file.close()
#			solve(input_data,numbers[i])
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		solve(input_data)