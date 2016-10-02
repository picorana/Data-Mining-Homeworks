from collections import defaultdict
usermap = defaultdict(int)


with open("tweets.txt", 'r') as filetoread:
	for line in filetoread:
		line = line.split("\t")
		user = line[0]

		usermap[user] += 1

maxtweets = 0
userwithmaxtweets = ""
tweetoccurrences = defaultdict(int)
for i in usermap:
	if usermap[i]>maxtweets:
		maxtweets = usermap[i]
		userwithmaxtweets = i
	tweetoccurrences[usermap[i]]+=1

maxoccurrences = 0
for j in tweetoccurrences:
	if tweetoccurrences[j]>maxoccurrences:
		maxoccurrences = j

auxsum = 0		
auxsum2 = 0
for user in usermap:
	auxsum2 += usermap[user]
	auxsum += usermap[user]*usermap[user]

print "total tweets: " + str(auxsum2)
print "number of users: " + str(len(usermap))
print "second moment: " + str(auxsum)
print "----"
print "user who tweeted the most: " + str(userwithmaxtweets) + " with " + str(maxtweets) + " tweets"
print str(tweetoccurrences[1]) + " users tweeted only once"
print str(tweetoccurrences[2]) + " users tweeted twice"
print str(tweetoccurrences[3]) + " users tweeted thrice"
