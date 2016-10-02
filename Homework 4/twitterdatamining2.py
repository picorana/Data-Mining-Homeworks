from twython import Twython
from twython import TwythonStreamer
from collections import defaultdict
import time
import random
import hashlib

APP_KEY = 'yf5nlSPspdfTGDd0HZiUtF0bQ'
APP_SECRET = 'BhzCUVhXREU9qN8ZZiA41qxDetHBwFUa6NHZiuNtBR9A1W4N13'
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAJ2efgAAAAAAbEXmT1iLaoBzLSM85YGb8DYnXJM%3DUSqCa93feF3SvWTVeiOBHk9A5Rds7E70mGjuJLjGWqKRBfIIiZ'

OAUTH_TOKEN = '420332315-sZ1nEI2hJ3llXYHe1SRY0wqj2nxNvyzrwayf0GLe'
OAUTH_TOKEN_SECRET = 'u7aYkYVT31eeNygFum62c0JCYa4yMR0MKnX3xfAWjRxm9'

oauth_verifier = '0235938'

_memomask = {}


class MyStreamer(TwythonStreamer):
    count = 0
    secondMoment = 0
    f = open("tweets.txt", 'w')
    hasharray = list()
    temporarysecondmomentdict = defaultdict(int)
    secondMomentBuffer = []

    def on_success(self, data):
        if self.count == 0:
            for i in range(1000):
                self.hasharray.append(self.hashFamily(i))

        self.count+=1

        if 'user' in data and data['user']!=None and data['user']['name']!="":
            nomeutente = data['user']['name']
            tempsum = 0
            for h in self.hasharray:
                if hash(h(nomeutente.encode('utf-8')))%2==0:
                    self.temporarysecondmomentdict[h]+=1
                else:
                    self.temporarysecondmomentdict[h]-=1
            #self.secondMoment += tempsum/len(self.hasharray)

            if hash(nomeutente)%2==0:
                self.secondMoment+=1
            else:
                self.secondMoment-=1

            #if h1(nomeutente)%2==0:
            #    self.secondMoment+=1
            #else:
            #    self.secondMoment-=1
            print  str(self.count) + " - " + nomeutente + ": ",

        if 'text' in data:
            line = data['text'].encode('utf-8').replace("\n", " ")
            print line
        self.f.write(nomeutente.encode('utf-8') + "\t" + line + "\n")
    	

        if self.count%10==0:
            avg2 = 0
            avg3 = 0
            for i in self.temporarysecondmomentdict:
                avg2+=self.temporarysecondmomentdict[i]*self.temporarysecondmomentdict[i]
                avg3+=self.temporarysecondmomentdict[i]
            avg2 = avg2/len(self.temporarysecondmomentdict)
            avg3 = avg3/len(self.temporarysecondmomentdict)
            self.secondMomentBuffer.append((self.secondMoment*self.secondMoment))
            avg = 0
            for i in self.secondMomentBuffer:
                avg+=i
            avg = avg/len(self.secondMomentBuffer)
            print ""
            print "----"
            print "Number of tweets: " + str(self.count)
            print "Second moment of this round:" + str((self.secondMoment*self.secondMoment))
            print "Average Second Moment: " + str(avg2)
            print "Control value: " + str(avg3)
            print "----"

        print ""
        

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

    def hash_function(self, n):
      mask = _memomask.get(n)
      if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)
      def myhash(x):
        return hash(x) ^ mask
      return myhash

    def hashFamily(self, i):
        resultSize = 8 # how many bytes we want back
        maxLen = 20 # how long can our i be (in decimal)
        salt = str(i).zfill(maxLen)[-maxLen:]
        def hashMember(x):
            return hashlib.sha512(x + salt).hexdigest()[-resultSize:]
        return hashMember


def calculateSecondMoment(usermap):
    result = 0
    whyarray=list()
    for i in range(len(usermap)):
        if random.random()<.5:
            whyarray.append(-1)
        else:
            whyarray.append(1)
    k=0
    for j in usermap:
        result += (usermap[j]*usermap[j])*whyarray[k]
        k+=1
    print result




stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='ciao', locations='12.23,41.65,12.85,42.14')