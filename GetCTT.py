print("###Keep This window open. Close if you want to change settings on Streamlabs Chatbot###")

#---------------------------------------
#	Import Libraries
#---------------------------------------
import sys, json, os, codecs, time, winsound

from TwitterSearch import *
from ast import literal_eval
from datetime import datetime, timedelta

import colorama
from colorama import init
init()
from colorama import Fore, Back, Style


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




#Get local time difference to UTC 
DTS = time.localtime().tm_isdst
TZ = time.timezone / 3600
TD = DTS - TZ




#Get variables from Settings file
path = os.path.dirname(os.path.abspath(__file__))
Settingsf = codecs.open("{}\settings.json".format(path),encoding='utf-8-sig',mode="r+")
Settings = dict()
Settings = json.load(Settingsf, encoding='utf-8-sig')
CTTMsg = Settings['CTTMsg']
RefreshTime = Settings['RefreshTime']
MentionsOn = Settings['MentionsOn']
Mention = Settings['Mention']
CTTColour = Settings['CTTColour']
CTTBG = Settings['CTTBackground']
MentionColour = Settings['MentionColour']
MentionBG = Settings['MentionBG']
sound = Settings['Sound']
Settingsf.close()

#Set text and background colours
#Running code in Python Shell will not show colours, but codes. Colours only work in CMD
def Tcolour(colour):
    if colour == "RED":    
        return(Fore.RED)
    elif colour == "BLACK":
        return(Fore.BLACK)
    elif colour == "BLUE":
        return(Fore.BLUE)
    elif colour == "CYAN":
        return(Fore.CYAN)
    elif colour == "GREEN":
        return(Fore.GREEN)
    elif colour == "MAGENTA":
        return(Fore.MAGENTA)
    elif colour == "WHITE":
        return(Fore.WHITE)
    elif colour == "YELLOW":
        return(Fore.YELLOW)
    
def Bcolour(colour):
    if colour == "RED":    
        return(Back.RED)
    elif colour == "BLACK":
        return(Back.BLACK)
    elif colour == "BLUE":
        return(Back.BLUE)
    elif colour == "CYAN":
        return(Back.CYAN)
    elif colour == "GREEN":
        return(Back.GREEN)
    elif colour == "MAGENTA":
        return(Back.MAGENTA)
    elif colour == "WHITE":
        return(Back.WHITE)
    elif colour == "YELLOW":
        return(Back.YELLOW)    
    
#Print colour codes for user
print Tcolour(CTTColour) + Bcolour(CTTBG) + "This is a CTT" + Fore.RESET + Back.RESET
print Tcolour(MentionColour) + Bcolour(MentionBG) + "This is a Mention" + Fore.RESET + Back.RESET

#Get Twitter keys
Keysf = open("{}\keys.txt".format(path),"r+")
Keysr = Keysf.read()
Keys = dict()
Keys = literal_eval(Keysr)
Keysf.close()

#Create Mentions list
mentions = dict()
mentions = {'Empty': 2}


while True:

    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords([CTTMsg]) # let's define all words we would like to have a look for
        tso.set_language('en') # we want to see English tweets only
        tso.set_include_entities(False) # and don't give us all those entity information
##        tso.set_since(datetime.date.today())
##        tso.set_result_type('recent')
        
        # Deal with authentication
        ts = TwitterSearch(
            consumer_key = Keys['consumer_key'],
            consumer_secret = Keys['consumer_secret'],
            access_token = Keys['access_token'],
            access_token_secret = Keys['access_token_secret']
         )
        
        #Get Today
        day = time.strftime("%a %b %d",time.gmtime()) 
        year = time.strftime("%Y",time.gmtime())

        #Get CTT List
        path = os.path.dirname(os.path.abspath(__file__))
        pendingf = open('{}\Pending.txt'.format(path),'r+')
        Tread = pendingf.read()
        tweeters = dict()
        tweeters = literal_eval(Tread)
        pendingf.close()
        
         # Search Twitter
        for tweet in ts.search_tweets_iterable(tso):
            TweetLocalTime = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours = TD) 
            # if user is not marked 1 (CTT but not reveived points), add to list marked 1.
            if tweet['created_at'].startswith(day) and tweet['created_at'].endswith(year):
                if tweet['user']['screen_name'].lower() in tweeters.keys():
                    if tweeters[tweet['user']['screen_name'].lower()] == 0:
                        tweeters[tweet['user']['screen_name'].lower()] = 1
                        print Tcolour(CTTColour) + Bcolour(CTTBG) + "({}) CTT: @{}".format(TweetLocalTime,tweet['user']['screen_name']) + Fore.RESET + Back.RESET
                        if sound == True:
                            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                else:
                    tweeters[tweet['user']['screen_name'].lower()] = 1
                    print Tcolour(CTTColour) + Bcolour(CTTBG) + "({}) CTT: @{}".format(TweetLocalTime,tweet['user']['screen_name']) + Fore.RESET + Back.RESET
                    if sound == True:
                        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

        #Return CTT list to file
        pendingf = open("{}\Pending.txt".format(path),"w+") # add Services/Scripts/CTT to file
        pendingf.write(str(tweeters))
        
        pendingf.close()


    except TwitterSearchException as e: # take care of all errors
        print(e)
        #Parent.SendTwitchMessage("e")

    if MentionsOn == True:
        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.set_keywords([Mention]) # set key word to be searched for
            tso.set_language('en') # we want to see English tweets only
            tso.set_include_entities(False) # and don't give us all those entity information
            # Deal with authentication
            ts = TwitterSearch(
                consumer_key = Keys['consumer_key'],
                consumer_secret = Keys['consumer_secret'],
                access_token = Keys['access_token'],
                access_token_secret = Keys['access_token_secret']
             )
            
             # Search twitter:
            for tweet in ts.search_tweets_iterable(tso):
                                
                TweetLocalTime = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours = TD) 
                
                # if new mention, display on window, and add to mentions list.
                if tweet['created_at'].startswith(day) and tweet['created_at'].endswith(year) and CTTMsg not in tweet['text']:
                    if tweet['id'] in mentions.keys():
                        if mentions[tweet['id']] == 0:
                            mentions[tweet['id']] = 1
                            print Tcolour(MentionColour) + Bcolour(MentionBG) + "({}) @{} tweeted: {}".format(TweetLocalTime,tweet['user']['screen_name'],tweet['text'].encode('ascii','ignore')) + Fore.RESET + Back.RESET
                            if sound == True:
                                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

                    else:
                        mentions[tweet['id']] = 1
                        
                        print Tcolour(MentionColour) + Bcolour(MentionBG) + "({}) @{} tweeted: {}".format(TweetLocalTime,tweet['user']['screen_name'],tweet['text'].encode('ascii','ignore')) + Fore.RESET + Back.RESET
                        if sound == True:
                            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)



        except TwitterSearchException as e: # take care of all  errors 
            print(e)
            #Parent.SendTwitchMessage("e")


    ## Delay next refresh
    time.sleep(RefreshTime*60)

######    OTHER PARAMETERS THAT CAN BE USED FROM TWEET:
######    tweet['text'] : text of tweet
######    tweet['id'] : id of tweet
######    tweet['retweet_count']: number of retweets
######    tweet['favorite_count'] : number of likes
######    tweet['created_at'] : date and time of creating tweet (in UTC)
######    tweet['user']['name'] : Display name
######    tweet['user']['screen_name'] : @name
######    tweet['user']['id'] : user id
######    tweet['user']['statuses_count'] : number of tweets by user
######    tweet['user']['friend_count'] : number of user's friends
######    tweet['user']['location'] : location of user
######    tweet['user']['following'] : whether is following authenticator
######    tweet['user']['created_at'] : date and time of creating user account (in UTC)
        

