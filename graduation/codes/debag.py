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


import sys
if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		c = processtime(input_data)
		print c