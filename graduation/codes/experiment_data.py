import sys,pprint
sys.path.append(".\\functions")
import generate

def generate_data(input_data):						# generate experiment data and store in the data file
	data = input_data.split('\n')
	N = len(data)
	for k in xrange(N):
		n = int(data[k])
		s = generate.setup(n)
		r = generate.release(n,3)
		f = open(".\\data\\"+str(data[k]),'w')
		step = generate.jobstep(n,8,20)
		q = generate.process(step[0])
		n_job = generate.itemjobs(n,1000,2000)
		p = [generate.processtime(n_job[0],q)]
		wt = generate.weights(n,8)
		wc = generate.weights(n,6)
		for j in xrange(1,n):
			q = generate.process(step[j])
			temp = generate.processtime(n_job[j],q)
			p.append(temp)
		d = generate.due_date_r(r,p)
		for i in xrange(n):
			f.write(str(p[i])+' ' + str(r[i]) + ' ' + str(s[i]) + ' ' + str(d[i]) + ' ' + str(wt[i]) + ' ' + str(wc[i]) + '\n')
		f.close()
		print 'data_' + str(data[k]) +' '+ 'done!'

import sys
if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		generate_data(input_data)		