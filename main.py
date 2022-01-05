import discord
import os
import requests # Generates HTTP request to get data from the API
import json # The data from the HTTP request is in the form of json, so in order to process and use it, json module is used
import random
from replit import db


# To keep the bot alive
from keep_alive import keep_alive




def get_joke():
  """This function will generate random jokes"""
  # API used is jokeAPI.v2
  response = requests.get("https://v2.jokeapi.dev/joke/Any")
  json_data = json.loads(response.text)
  # print(json_data)
  joke = json_data['setup'] + "\n" + json_data['delivery']
  return(joke)

# Collection of words, if they are present in a normal sentence, will generate an encouraging message
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "It will get better"
]

#to determine if the bot should respond to sad words or not.
if "responding" not in db.keys():
  db["responding"] = True





def get_quote():
  """This function will generate random inspirational quotes"""
  # API used is zenquotes.io
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = str(json_data[0]['q']) + "\n" + " -" + str(json_data[0]['a'])
  return(quote)


def update_encouragements(encouraging_message):
  """
  Accepts an encouraging message as an argument.
  Through this, Users will be able to add custom encouraging messages for the bot to use directly from the Discord chat."""

  # If the encouraging message is in the database
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  # If the ecouraging message is not in the database
  else:
    db["encouragements"] = encouraging_message

def delete_encouragement(index):
  """
  Will delete a particular encouragement from the database"""
  encouragements = db["encouragements"]
  # If a person passes an index that is actually in that list
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements








# Creating client connection that connects to Discord.
# To create it, an instance is made through the below command
client = discord.Client()
# To register an event, "Client.event" decorator is used
@client.event
# This decorator requires asynchronus function to be called
# asynchronus Function - a function that requires callbacks. callbacks are basically function "calls" that are ready to be used after a thing/event/task has occured


async def on_ready():
  """
  This function is kind of a starter function that will show a message when the bot is ready to use.
  """
  print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  """This Function will sense the message from the user which, in future, mayb be needed to perform a particular task"""
  # Either the message will be given by the user or the bot itself.
  # So if the bot sends the message, idts that we have to do anything

  # If the message is sent by bot user
  if message.author == client.user:
    return


  #Show Commands that the user can perform
  help_string = "```1.Say hello to the bot - $hello" + "\n\n 2.responds to dejected messages"+ "\n\n 3.Turn off response to usual dejected messages - $response false"+"\n\n 4.Turn on response to usual dejected messages - $response True"+"\n\n 5.Generate random inspiring messages - $inspire"+"\n\n 6.Generate random jokes - $joke"+"\n\n 7.add encouraging messages to database - $new --add_message--"+"\n\n 8.list all encouraging messages fo database - $list"+"\n\n 8.delete the encouraging messages from database - $del --index--```"
  if message.content.startswith('$help'):
    await message.channel.send(help_string)
    


  # If message is sent by human in terms of a command
  #  we check if the Message.content starts with '$hello'. If so, then the bot replies with 'Hello!' to the channel it was used in.
  if message.content.startswith('$hello'):
    await message.channel.send('Hello! fellow mate')

  # If the message starts with "$inspire", then it will show up a random inspiring message generated from an API 
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if message.content.startswith('$joke'):
    joke = get_joke()
    await message.channel.send(joke)
  

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"].value

    # If any sentence has a word from sad_words array, then
    # an encouragement is generated from the starter_encouragements array
    # Update : Encouragements will now be picked up from options
    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  
    
  # Adding a new "User Submittedd message" to the database
  if message.content.startswith("$new"):
    encouraging_message = message.content.split("$new ",1)[1]
    if len(encouraging_message) > 0:
      update_encouragements(encouraging_message)
      await message.channel.send("New Encouraging message added!")

  # Deleting encouragements
  if message.content.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)


  # Showing the list of the added encouragements
  if message.content.startswith("$list"):
    """Displaying all the customized encouragements"""
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  # Turning off/on responses to dejected messages.
  if message.content.startswith("$responding"):
    """
    If the user needs to set responding as true or false"""
    value = message.content.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("responding is on.")
    elif value.lower() == "false":
      db["responding"] = False
      await message.channel.send("responding is off.")



keep_alive()
client.run(os.environ['TOKEN'])
