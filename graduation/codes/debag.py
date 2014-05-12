import sys,pprint
sys.path.append(".\\functions")
import hello
import basi

'''
def processtime(input_data):
	data = input_data.split('\n')
	first_line = data[0].split()
	n = int(first_line[0])
	m = int(first_line[1])
	q = []
	m = len(data)
	for i in xrange(1,m):
		q.append(int(data[i]))
	print q
	print n
	print 'data loaded'
	c = [None]*n
	d= []
	for k in xrange(n):
		c[k] = (k+1)*q[0]

	for i in xrange(1,m-1):
		c[0] = c[0] + q[i]
		for k in xrange(1,n):
			c[k] = max(c[k],c[k-1])+q[i]
	return c[-1]
'''
def generate(input_data):
	data = input_data.split('\n')
	n = int(data[3])
	s = basi.setup(n)
	r = basi.release(n,3)
	f = open(".\\result\\haha",'w')
	step = basi.jobstep(n,8,20)
	q = basi.process(step[0])
	n_job = basi.itemjobs(n,1000,2000)
	p = [basi.processtime(n_job[0],q)]
	for j in xrange(1,n):
		q = basi.process(step[j])
		temp = basi.processtime(n_job[j],q)
		p.append(temp)
	d = basi.due_date_r(r,p)
	print p,s[0],r,d
	for i in xrange(n):
		f.write(str(p[i]))
		f.write(' ')
		f.write(str(r[i]))
		f.write(' ')
		f.write(str(s[i]))
		f.write(' ')
		f.write(str(d[i])+'sky')
		f.write(' ')
		f.write('\n')
	f.close()
	return s


import sys
if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		output = sys.argv[2].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		c = generate(input_data)
		output_file = open(output,'w')
		output_file.write(str(c))		
		output_file.close()
		
