from __future__ import division
import math
import random

#define the ordering index
def Idx(time, p , due_dates, wt):
	n = len(p)
	Idx_value = [None]*n
	average = sum(p)/n
	for j in xrange(n):
		Idx_value[j] = wt[j]/p[j]*math.exp(-max(due_dates[j]-p[j]-t,0)/2/average)
	return Idx_value

# generate the poisson var
def poisson(alpha):
	n = 0
	P = random.random()
	while P >= math.exp(-alpha):
		r = random.random()
		P = P*r
		n+=1
	N = n
	return N

# generate the item release time
def release(n,alpha):
	r = [poisson(alpha)]
	for j in xrange(1,n):
		a = poisson(alpha)
		temp = a + r[-1]
		r.append(temp)
	random.shuffle(r)
	return r

# generate the job process time
def process(n):
	q = [None]*n
	for i in xrange(n):
		q[i] = poisson(5)
	return q

# generate the itme setup time
def setup(n):
	s = [None]*n
	for j in xrange(n):
		s[j] = random.randrange(1,10)
	return s

# generate the step of a job needs
def jobstep(n,a,b):
	step = [random.randrange(a,b)]
	for j in xrange(1,n):
		step.append(random.randrange(a,b))
	return step

# generate the number of jobs that a item needs
def itemjobs(n,a,b):
	n_job = [random.randrange(a,b)]
	for j in xrange(1,n):
		n_job.append(random.randrange(a,b))
	return n_job

# calculate the item process time
def processtime(n,q):
	m = len(q)
	c = [None]*n
	d= []
	for k in xrange(n):
		c[k] = (k+1)*q[0]
	for i in xrange(1,m-1):
		c[0] = c[0] + q[i]
		for k in xrange(1,n):
			c[k] = max(c[k],c[k-1])+q[i]
	return int(c[-1]/500)


# generate the job due dates with release time
def due_date_r(r,p):
	n = len(r)
	d = [None]*n
	for j in xrange(n):
		delta = int(p[j]/3)
		d[j] = r[j] + 2*p[j] + random.randrange(-delta,delta)
	return d

# generate the job due dates without release time
def due_date(p):
	n = len(p)
	flow_jobs = int(n/6/3)
	d = [None]*n
	for j in xrange(n):
		d[j] = random.randrange(2*flow_jobs*p[j],4*flow_jobs*p[j])
	return d

# generate the weights for Tardiness and Completion, just input the init
def weights(n,init):
	w  = [init]
	for j in xrange(n):
		w.append(random.randrange(2*init))
	ws = sum(w)
	for j in xrange(n):
		w[j] = w[j]/ws
	random.shuffle(w)
	return w
