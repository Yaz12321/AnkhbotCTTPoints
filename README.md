# AnkhbotCTTPoints
Scripts for Streamlabs Chatbot to check twitter for CTT, and give points to whoever tweets the stream.

Instructions:


1- After importing to Chatbot, open EmptyKeys folder, and copy the files into the main folder. open keys.txt, and fill in your customer key/secret and access token/secret between the single quotes.

  	To get customer key/secret and access token/secret:
  
    a- go to https://apps.twitter.com
  
    b- create a new app.
  
    c- in the app, under 'Keys and Access Tokens' you will get your customer key and secret.
  
    d- from the app, create access token.
  
  
2- open Command Prompt, and type "start C:\python27\scripts\pip.exe install TwitterSearch" (without quotes) to install TwitterSearch library. When it is installed, install colorama library: "start C:\python27\scripts\pip.exe install colorama"

3- On Chatbot, make sure to set your Twitter message and saving settings before running/enabling the command.

4- Make sure to follow your bot account to receive whispers asking to provide twitch accounts.

When you start each stream, make sure you send a reset command to empty the list.

When script is loaded and enabled, a black window (python.exe) will pop-up. CTT and mentions (if enabled) will appear on that page. Do not close that window, as it runs the script of doing the twitter search. If not interested in getting notified: keep it minimised. Close manually when monitoring CTT is not needed (i.e. script is disabled.) 
