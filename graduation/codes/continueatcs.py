import sys
sys.path.append(".\\functions")
import generate
from collections import namedtuple
Item = namedtuple("Item", ['process','release','setup','due','wt','wc'])

def  h(tardiness,completion,wt,wc):			# define the contribution of one item for the obj function
	value = lambda1*wt*tardiness + lambda2*wc*completion
	return value
lambda1 = 0.6
lambda2 = 0.4

def ATCS(items,S):
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


def solve(input_data):
	Data = input_data.split('\n')					# load data
	n = len(Data) -1							# get the amount of items
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
	S,L,completion = generate.initialization(items,n,5)
	print 'Initialization done!'

	lateness = generate.late(completion,items)
	tardiness = generate.tard(lateness)
	item_values = []
	for j in xrange(n):
		item = items[j]
		wt,wc = item.wt,item.wc
		t,c = tardiness[j],completion[j]
		value = h(t,c,wt,wc)
		item_values.append(value)
	G = generate.H(item_values,L)
	line_values = []
	for s in S:
		value = generate.H(item_values,s)
		line_values.append(value)
	print 'Initial values done!'
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
	NR = 100
	for k in xrange(NR):
#		g.write(str(k)+':\n')
		l_p,l_m = generate.reorder(items,S,line_values,item_values)
		S[l_p],c_p = ATCS(items,S[l_p])
		S[l_m],c_m = ATCS(items,S[l_m])
		for j in S[l_p]:
			completion[j] = c_p.pop(0)
			c = completion[j]
			item = items[j]
			wt,wc = item.wt,item.wc
			late = completion[j] - item.due
			t = generate.tard(late)
			item_values[j] = h(t[0],c,wt,wc)
		for j in S[l_m]:
			completion[j] = c_m.pop(0)
			c = completion[j]
			item = items[j]
			wt,wc = item.wt,item.wc
			late = completion[j] - item.due
			t = generate.tard(late)
			item_values[j] = h(t[0],c,wt,wc)
		delta_p = generate.H(item_values,S[l_p]) - line_values[l_p]
		delta_m = generate.H(item_values,S[l_m]) - line_values[l_m]
		line_values[l_p] += delta_p
		line_values[l_m] += delta_m
		G = G + delta_m + delta_p
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