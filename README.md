# AnkhbotCTTPoints
Scripts for Streamlabs Chatbot to check twitter for CTT, and give points to whoever tweets the stream.

Instructions:


1- After importing to Chatbot, open EmptyKeys folder, and copy the files into the main folder (where GetCTT.py is). Open keys.txt, and fill in your customer key/secret and access token/secret between the single quotes.

  	To get customer key/secret and access token/secret:
  
      a- Login to the apps.twitter.com interface using your Twitter credentials

      b- Create an app 
      
      c- Open the app, and navigate to the 'Keys and Access Tokens' page (That's where consumer key/secter are)

      d- Scroll down and click on the 'Create my access token' button (That's when you get your access token/secret)

2- open Command Prompt, and type "start C:\python27\scripts\pip.exe install twython" (without quotes) to install twython library (to get twitter data). When it is installed, install colorama library: "start C:\python27\scripts\pip.exe install colorama" (to have coloured text)

3- On Chatbot, make sure to set your Twitter message and saving settings before running/enabling the command.

4- Make sure to follow your bot account to receive whispers asking to provide twitch accounts. (Not sure if this is still necessary! But better safe than sorry)

When you start each stream, make sure you send a reset command to empty the list.

When script is loaded and enabled, a black window (python.exe) will pop-up. CTT and mentions (if enabled) will appear on that page. Do not close that window, as it runs the script of doing the twitter search. If not interested in getting notified: keep it minimised. Close manually when monitoring CTT is not needed (i.e. script is disabled.) 
NOTE: if the "Only when live" is enabled, the python.exe window will open automatically only when you are live. If you are not live and it is enabled, you will have to open it manually (click on OPEN TWITTER MONITOR button in the script UI on chatbot). 


NOTE: This script is a bit complicated to set up. If you need help, please conact me. 
