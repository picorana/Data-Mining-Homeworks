import time
import itertools
import random

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
			print str(j) + " occurrences: " + str(i[j])
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

def verifyrandomized(doc, frequentitemsets2, threshold):
	result = {}
	frequentitemsets = {}
	for i in frequentitemsets2:
		for j in i:
			frequentitemsets[j] = 1

	with open(doc, "r") as filetoread:
		c = 0
		for line in filetoread:
			line = line.strip()
			auxvector = line.split(" ")
			for itemset in frequentitemsets:
				if set(itemset).issubset(auxvector):
					if itemset in result:
						result[itemset]+=1
					else:
						result[itemset]=1
			c+=1
			if c%1000==0:
				print c
	result2 = {}
	for r in result:
		if result[r]>=threshold:
			result2[r] = result[r]

	difference = len(result2)-len(frequentitemsets)
	print "total number of false positives found: " + str(difference)



doc = "retail.dat"
threshold = 500
p = 0.1
apriori(doc, threshold)
#frequentitemsets = apriorirandomized(doc, p, threshold*p*0.9)
#verifyrandomized(doc, frequentitemsets, threshold)