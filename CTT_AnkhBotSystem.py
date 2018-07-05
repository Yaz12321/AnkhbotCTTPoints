#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import time
from ast import literal_eval



#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "CTTGivePoints"
Website = ""
Creator = "Yaz12321"
Version = "1.0"
Description = "Give Points to viewers who tweet the stream"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version: 

# > 1.0 < 
    # Official Release

# Future Version:
    # Replace the use of browser to direct use of SLOBS

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.LiveOnly = True
            self.WhoIscmd = "!whois"
            self.Resetcmd = "!resetctt"
            self.Permission = "Caster"
            self.PermissionInfo = ""
            self.GetPointsMsg = "Thank you {0} for tweeting. You have received {1} {2}. "
            self.WhoIsMsg = "Who is {0} from Twitter? Respond by {1} [twitter] [twitch]"
            self.CTTPayout = 30
            self.RefreshTime = 10
            self.ResetMsg = "CTT List has been reset"
            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    

    global t
    t = time.time()

    global end
    end = 0
    global Trigger
    Trigger = 0
    global n
    n = 0 

    global MySettings
    # Load in saved settings
    MySettings = Settings(settingsFile)

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return


def Execute(data):

    #Reset List
    if Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo) and data.GetParam(0).lower() == MySettings.Resetcmd:
        fil = open("Services/Scripts/CTT/Pending.txt","w+")
        fil.write("{'Empty': 2}")
        fil.close()
        Parent.SendTwitchMessage(MySettings.ResetMsg)
        
    if MySettings.LiveOnly == False:
        live = True
    else:
       live = Parent.IsLive()
    
    #Get twitch account from streamer
    if Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo) and data.GetParam(0).lower() == MySettings.WhoIscmd :
        tweetac = data.GetParam(1)
        twitchac = data.GetParam(2)
        f = open("Services/Scripts/CTT/whois.txt","r+")
        accounts = dict()
        accounts = literal_eval(f.read())
        f.close()
        accounts[tweetac] = twitchac
        f = open("Services/Scripts/CTT/whois.txt","w+")
        f.write(str(accounts))
        f.close()
        Parent.SendTwitchMessage("Twitch account {} has been assigned to {}".format(twitchac,tweetac))
        AddP()

    return

def AddP():

    path = os.path.dirname(os.path.abspath(__file__))
    os.system("start {}\GetCTT.py".format(path))
    
    global t
    t = time.time()

    #Get Twitter-to-Twitch conversion list
    f = open("Services/Scripts/CTT/whois.txt","r+")
    accounts = dict()
    accounts = literal_eval(f.read())
    f.close()
    
    #Get CTT List
    tweets = dict()
    fil = open("Services/Scripts/CTT/Pending.txt","r+")  
    tweets = literal_eval(fil.read())
    fil.close()


    #Check list for users who tweeted
    for CTT in tweets.keys():
        if tweets[CTT] == 1:
            #if twitter account is in conversion list 
            if CTT in accounts.keys():
                #Give points to twitch account
                twitcha = accounts[CTT].lower()
                gotpoints = Parent.AddPoints(twitcha,MySettings.CTTPayout)
                #Users can only recieve points when in chat. If they have received the points:
                if gotpoints == True:
                    #Change their mark to 2 (given points)
                    tweets[CTT] = 2
                    #Announce on chat
                    Parent.SendTwitchMessage(MySettings.GetPointsMsg.format(CTT,MySettings.CTTPayout,Parent.GetCurrencyName()))
            else:
                #if not in conversion list, ask streamer to provide twitch account.
                Parent.SendStreamWhisper(Parent.GetChannelName(),MySettings.WhoIsMsg.format(CTT,MySettings.WhoIscmd))

    #Save list back to file.
    fil = open("Services/Scripts/CTT/Pending.txt","w+")
    fil.write(str(tweets))
    fil.close()
    

    
    return



def Tick():

    #Timer
    if MySettings.LiveOnly == False:
        live = True
    else:
       live = Parent.IsLive()
    
    if time.time() > t + (MySettings.RefreshTime*60) and live == True:
        AddP()
    return 

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
