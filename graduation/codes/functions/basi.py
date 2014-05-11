from __future__ import division
import math #use the math module
import random
# define the obj function
#def Goal(wt,wc):

#define the ordering index
def Idx(time, p , due_dates, wt):
	n = len(p)
	Idx_value = [None]*n
	average = sum(p)/n
	for j in xrange(n):
		Idx_value[j] = wt[j]/p[j]*math.exp(-max(due_dates[j]-p[j]-t,0)/2/average)
	return Idx_value

# generate the job release time
def release(n):
	r = [None]*n
	for j in xrange(n):
		r[j] = random.randrange(10)/5
	return r
# generate the job due dates


# generate the weights for Tardiness and Completion
#def weights(n):
#	for j in xrange(n):

#NL = 2  # the list length of Tabu list
#TL = [None]*NL
#S_0 = S
