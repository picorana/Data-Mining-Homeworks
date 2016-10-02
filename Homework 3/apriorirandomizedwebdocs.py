import time
import itertools
import random
from collections import defaultdict

def apriori(nomefile, threshold):

	start_time = time.time()

	print "finding single items..."
	singleitems = findsingleitems(nomefile)
	print "number of single items found: " + str(len(singleitems))

	print "removing items under threshold..."
	singleitems = finditemsoverthreshold(singleitems, threshold)
	print str(len(singleitems)) + " single items occurring at least " + str(threshold) + " times found"
	#print singleitems
	print ""

	frequentitemsets = []
	auxitemsets = {}
	previousauxitemsets = singleitems

	k = 2
	print "finding k = " + str(k) + " sized frequent itemsets..."
	auxitemsets = find2frequentitemsets(nomefile, singleitems, k, threshold, "auxfile1.dat")
	print str(len(auxitemsets)) + " frequent itemsets of size k=" + str(k) + " found"
	print ""
	frequentitemsets.append(auxitemsets)

	while auxitemsets != {}:
		k+=1
		if k%2!=0:
			print "finding k = " + str(k) + " sized frequent itemsets..."
			auxitemsets = findkfrequentitemsets("auxfile1.dat", singleitems, auxitemsets, k, threshold, "auxfile2.dat")
			print str(len(auxitemsets)) + " frequent itemsets of size k=" + str(k) + " found"
			print ""
			frequentitemsets.append(auxitemsets)
		else:
			print "finding k = " + str(k) + " sized frequent itemsets..."
			auxitemsets = findkfrequentitemsets("auxfile2.dat", singleitems, auxitemsets, k, threshold, "auxfile1.dat")
			print str(len(auxitemsets)) + " frequent itemsets of size k=" + str(k) + " found"
			print ""
			frequentitemsets.append(auxitemsets)


	print "-------------------"
	count = 0
	for i in frequentitemsets:
		for j in i:
	#		print str(j) + " occurrences: " + str(i[j])
			count += 1

	end_time = time.time() - start_time
	print "total time: " + str(end_time)
	print "total number of frequent itemsets: " + str(count)
	return frequentitemsets





def findsingleitems(nomefile):
	start_time = time.time()
	result = {}
	with open(nomefile, "r") as filetoread:
		c = 0
		for line in filetoread:
			line.strip("\n")
			auxvector = line.split(" ")
			for item in auxvector:
				if item in result:
					result[item] += 1
				else:
					result[item] = 1
			c+=1
			if c%100000 == 0:
				print c
	end_time = time.time() - start_time
	print "elapsed time: " + str(end_time)
	return result

def finditemsoverthreshold(singleitems, threshold):
	result = {}
	for item in singleitems:
		if singleitems[item] >= threshold:
			result[item] = singleitems[item]
	return result

def findkfrequentitemsets(nomefile, singleitems, previousauxitemsets, k, threshold, filetowrite):
	start_time = time.time()
	result = {}
	result2 = {}
	f = open(filetowrite, "w")
	with open(nomefile, "r") as filetoread:
		c = 0
		for line in filetoread:
			line = line.strip()
			auxvector = line.split(" ")
			auxy = {}
			for i in auxvector:
				if i in singleitems:
					auxy[i] = 1
			auxvector = sorted(list(auxy))
			auxauxvector2 = cleanauxvector(auxvector, previousauxitemsets)
			if auxauxvector2!=[] and len(auxauxvector2)>k:
				auxstring = ""
				for d in auxauxvector2:
					auxstring+= str(d) + " "
				auxstring+="\n"
				f.write(auxstring)
			l1 = list(itertools.combinations(auxauxvector2, k))
			for l in l1:
				if l in result:
					result[l] += 1
				else:
					result[l] = 1
			c+=1
			if c%100000 == 0:
				print c

	for r in result:
		if result[r]>=threshold:
			result2[r] = result[r]

	end_time = time.time()-start_time
	print "elapsed time: " + str(end_time)

	return result2


def find2frequentitemsets(nomefile, singleitems, k, threshold, filetowrite):
	start_time = time.time()
	result = {}
	result2 = {}
	f = open(filetowrite, "w")
	with open(nomefile, "r") as filetoread:
		c = 0
		for line in filetoread:
			line = line.strip()
			auxvector = line.split(" ")
			auxvector2 = []
			for i in auxvector:
				if i in singleitems:
					auxvector2.append(i)
			auxvector2 = sorted(auxvector2)
			if auxvector2!=[] and len(auxvector2)>k:
				auxstring = ""
				for d in auxvector2:
					auxstring+=str(d) + " "
				auxstring+="\n"
				f.write(auxstring)
			l1 = list(itertools.combinations(auxvector2, k))
			for l in l1:
				if l in result:
					result[l] += 1
				else:
					result[l] = 1
			c+=1
			if c%100000 == 0:
				print c

	for r in result:
		if result[r]>=threshold:
			result2[r] = result[r]

	end_time = time.time()-start_time
	print "elapsed time: " + str(end_time)

	return result2

def cleanauxvector(auxvector, previousauxitemsets):
	result = {}
	for i in previousauxitemsets:
		if set(i).issubset(auxvector):
			for j in i:
				if j not in result:
					result[j] = 1
	result2 = sorted(list(result))
	return result2







def randomize(nomefile, samplingprob):
	start_time = time.time()
	print "sampling file..."
	with open(nomefile, "r") as filetoread:
		with open("webdocsrandomized.dat", "w") as filetowrite:
			c=0
			for line in filetoread:
				if random.random()<=samplingprob:
					filetowrite.write(line)
	print ""
	end_time = time.time() - start_time
	print "elapsed time: " + str(end_time)





def apriorirandomized(doc, p, threshold):
	randomize(doc, p)
	frequentitemsets = apriori("webdocsrandomized.dat", threshold)
	return frequentitemsets





def verifyrandomized(doc, frequentitemsets, threshold):
	print "verifying randomized results..."
	#singleitems = findsingleitems2(frequentitemsets[0])
	singleitems = finditemsoverthreshold(findsingleitems(doc), threshold)
	print "number of single items found: " + str(len(singleitems))
	print ""
	frequentitemsets = findfrequentitemsets3(doc, frequentitemsets, threshold, singleitems)


def findsingleitems2(frequentitemsets):
	result = defaultdict(int)
	for i in frequentitemsets:
		for j in i:
			result[j] = 1
	return result

def findfrequentitemsets2(doc, frequentitemsets, threshold, singleitems):
	result = defaultdict(int)
	result2 = defaultdict(int)



	setarray = []
	for i in range(len(frequentitemsets)):
		setarray.append(itertools.chain(frequentitemsets[i]))

	c = 0
	auxresult = defaultdict(int)
	auxresult2 = set()
	with open(doc, "r") as filetoread:
		while i in range(len(frequentitemsets)):
			for line in filetoread:
				line = line.strip()
				line = line.split(" ")
				line = set(line).intersection(set(singleitems))
				if len(auxresult2)>0:
					line = set(line).intersection(auxresult2)
				k=2

				linecombinations = itertools.combinations(line, k)
				for l in linecombinations:
					result[l] += 1
					auxresult[l] += 1	

				#line = set(line).intersection(set(setarray[0]))

				#linecombinations = itertools.combinations(line, k+1)	
				#for l in linecombinations:
				#	result[l] += 1		

				c+=1
				if c%100000==0:
					print c

			auxresult2 = set()

			for itemset in auxresult:
				if auxresult[itemset]>=threshold:
					auxresult2.add(itemset)
			auxresult2 = auxresult2.intersection(set(setarray[i]))

			i+=1


	for r in result:
		if result[r] >= threshold:
			result2[r] = result[r]

	print len(result2)

def findfrequentitemsets3(doc, frequentitemsets, threshold, singleitems):
	start_time = time.time()
	result = defaultdict(int)
	result2 = defaultdict(int)



	setarray = []
	for i in range(len(frequentitemsets)):
		setarray.append(itertools.chain(frequentitemsets[i]))

	c = 0

	with open(doc, "r") as filetoread:
		for line in filetoread:
			line = line.strip()
			line = line.split(" ")
			line = set(line).intersection(set(singleitems))
			for i in frequentitemsets:
				for j in i:
					if set(j).issubset(line):
						result[j] += 1 
			c+=1
			if c%100000==0:
				print c


	for r in result:
		if result[r] >= threshold:
			result2[r] = result[r]
	end_time = time.time() - start_time
	print "frequent itemsets found: " + str(len(result2))
	print "elapsed time: " + str(end_time)

doc = "webdocs.dat"
threshold = 500000
p = 0.0001
#apriori(doc, threshold)
frequentitemsets = apriorirandomized(doc, p, threshold*p*0.9)
verifyrandomized(doc, frequentitemsets, threshold)
