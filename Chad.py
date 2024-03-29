import discord
import os
import requests
import json
import random
from replit import db



client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "You are a great person!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
 
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
 
  if msg.startswith('ayo inspire'):
     quote = get_quote()
     await message.channel.send(quote)
  
  
  if msg.startswith('ayo hi'):
     await message.channel.send("Hello " + message.author.mention + "!")
  if msg.startswith('ayo what should I do'):
     await message.channel.send("Bruh you are literally asking a bot what to do lol.")
  
  if db["responding"]:
     options = starter_encouragements
     if "encouragements" in db.keys():
      options.extend(db["encouragements"])

  if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("ayo new"):
     encouraging_message = msg.split("ayo new ",1)[1]
     update_encouragements(encouraging_message)
     await message.channel.send("New encouraging message added.")
  

  if msg.startswith("ayo del"):
     encouragements = []
     if "encouragements" in db.keys():
      index = int(msg.split("ayo del",1)[1])
      delete_encouragment(index)
      encouragements = list(db["encouragements"])
     await message.channel.send(encouragements)

  if msg.startswith("ayo list"):
     encouragements = []
     if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
     await message.channel.send(encouragements)

  if msg.startswith("ayo responding"):
     value = msg.split("ab responding ",1)[1]

     if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
     else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

client.run(os.getenv('TOKEN'))
