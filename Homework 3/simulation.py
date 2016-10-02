import random
import itertools
from collections import defaultdict
import time
import matplotlib.pyplot as plt
import numpy as np



def build(n, m, p):
	result = set()
	k=0
	for i in range(m):
		auxset = set()
		for j in range(n):
			if random.random()<=p:
				auxset.add(j)
		auxset = frozenset(auxset)
		result.add(auxset)
		k +=1
		#if k%10000==0:
		#	update_progress(k*100/m)
	return result

def finditemoccurrences(target, item):
	count = 0
	for i in target:
		if item in i:
			count+=1
	#print "occurrences of item " + str(item) + " : " + str(count)
	return count

def calculateexpectedvalue(m):
	count = 0
	for i in range(m):
		count+=0.005
	print "How many times do we expect to see a particular item? answer: " + str(count)
	return count

def calculateexpectedvalueofapair(m):
	count = 0
	for i in range(m):
		count+=0.005*0.005
	print "How many times do we expect to see a pair? answer: " + str(count)
	return count

def countitemsoverexpectedvalue(target, evalue, n):
	evaluepercent = evalue+(evalue/100)*10
	howmanyover = 0
	result = defaultdict(int)

	for i in target:
		for j in i:
			result[j] += 1

	result2 = defaultdict(int)

	for r in result:
		if result[r] >= evaluepercent:
			result2[r] = result[r]

	print ""
	print "there are " + str(len(result2)) + " items that occur at least ten percent more times than the expected value"
	
	return result

def countpairsoverexpectedvalue(target, evaluepair, n, l11):
	evaluepairperfive = evaluepair*5
	result = defaultdict(int)
	result2 = defaultdict(int)
	for basket in target:
		#basket = set(basket).intersection(set(l11))
		l1 = itertools.combinations(basket, 2)
		for l in l1:
			result[l]+=1

	maxoccurrences = 0

	for r in result:
		if result[r]>=evaluepair*5:
			result2[r] = result[r]
			if result[r]>maxoccurrences:
				maxoccurrences = result[r]
	print ""
	print "there are " + str(len(result2)) + " pairs that occur at least five times more than the expected value"
	print "the most frequent pair appears " + str(maxoccurrences) + " times"
	return result


def update_progress(progress):
    print '\r[{0}] {1}%'.format('#'*(progress/10), progress)



#main
n = 2000
m = 100000
p = 0.005
start_time = time.time()

k = 0

while k<10:

	print "Simulation " + str(k) + ":"

	target = build(n, m, p)
	step_time = time.time() - start_time
	evalue = calculateexpectedvalue(m)
	evaluepair = calculateexpectedvalueofapair(m)
#finditemoccurrences(target, 10)
#finditemoccurrences(target, 11)
	l1 = countitemsoverexpectedvalue(target, evalue, n)
	step_time = time.time() - start_time
	pairsoccurrences = countpairsoverexpectedvalue(target, evaluepair, n, l1)

	step_time = time.time() - start_time

	k+=1

	print ""
	print ""