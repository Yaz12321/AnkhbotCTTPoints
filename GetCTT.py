#---------------------------------------
#	Import Libraries
#---------------------------------------
import sys, json, os, codecs, time

from TwitterSearch import *

from ast import literal_eval


#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "CTTupdate"
Website = ""
Creator = "Yaz12321"
Version = "1.0"
Description = "Part 1: Create a list of viewers who CTT"

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:

# > 1.0< 
    # Official Release



path = os.path.dirname(os.path.abspath(__file__))
Settingsf = codecs.open("{}\settings.json".format(path),encoding='utf-8-sig',mode="r+")
Settings = dict()
Settings = json.load(Settingsf, encoding='utf-8-sig')
CTTMsg = Settings['CTTMsg']
RefreshTime = Settings['RefreshTime']
Settingsf.close()

Keysf = open("{}\keys.txt".format(path),"r+")
Keysr = Keysf.read()
Keys = dict()
Keys = literal_eval(Keysr)
Keysf.close()

tim = time.time()
while True:
    if time.time() > tim + (RefreshTime*60):
        tim = time.time()
        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.set_keywords([CTTMsg]) # let's define all words we would like to have a look for
            tso.set_language('en') # we want to see English tweets only
            tso.set_include_entities(False) # and don't give us all those entity information
            # it's about time to create a TwitterSearch object with our secret tokens
            ts = TwitterSearch(
                consumer_key = Keys['consumer_key'],
                consumer_secret = Keys['consumer_secret'],
                access_token = Keys['access_token'],
                access_token_secret = Keys['access_token_secret']
             )
            

            day = time.strftime("%a %b %d",time.localtime())
            year = time.strftime("%Y",time.localtime())
            path = os.path.dirname(os.path.abspath(__file__))
            pendingf = open('{}\Pending.txt'.format(path),'r+')
            Tread = pendingf.read()
            tweeters = dict()
            tweeters = literal_eval(Tread)
            pendingf.close()
            
            
            
             # this is where the fun actually starts :)
            for tweet in ts.search_tweets_iterable(tso):
                
                if tweet['created_at'].startswith(day) and tweet['created_at'].endswith(year):
                    if tweet['user']['screen_name'].lower() in tweeters.keys():
                        if tweeters[tweet['user']['screen_name'].lower()] == 0:
                            tweeters[tweet['user']['screen_name'].lower()] = 1
                            print(tweet['user']['screen_name'])
                    else:
                        tweeters[tweet['user']['screen_name'].lower()] = 1
                        print(tweet['user']['screen_name'])

            pendingf = open("{}\Pending.txt".format(path),"w+") # add Services/Scripts/CTT to file
            pendingf.write(str(tweeters))
            #print(time.strftime("%a %b %d %H:%M:%S +0000 %Y",time.localtime()))
            pendingf.close()

            #print(tweet)

        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)
            #Parent.SendTwitchMessage("e")

            


