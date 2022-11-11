import requests,os

try:
  from config import *
  os.system('pm2 start bot.py --name {} --interpreter python3 --interpreter-args -u'.format(BOT_ID))
except Exception as e:
  API_ID = 20914232
  API_HASH = '38b1d3ae53407ab641ef05b7e43bf86a'
  out ="""
from pyrogram import enums
API_ID = 20914232
API_HASH = '38b1d3ae53407ab641ef05b7e43bf86a'
"""
  def Bot(TOKEN,method,data):
    url = "https://api.telegram.org/bot{}/{}".format(TOKEN,method)
    post = requests.post(url,data=data)
    return post.json()
  ID = ""
  go = True
  while go:
    token = input("input you're bot TOKEN:")
    get = Bot(token,"getme",{})
    if get["ok"]:
      out = out+"\n"+"TOKEN = '{}'\nBOT_ID = TOKEN.split(':')[0]".format(token)
      go = False
      ID = token.split(':')[0]

    else:
      print("TOKEN is invalid, Try again")

  sudo = input("input you're ID:")
  out = out+"\n"+"SUDO = {}".format(sudo)

  f = open("config.py","w+") 
  f.write(out)
  f.close()

  os.system('pm2 start bot.py -f --name {} --interpreter python3 --interpreter-args -u'.format(ID))
