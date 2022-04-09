from ntpath import join
import discord
import pickle
import nltk 
import numpy

client = discord.Client()

@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
    if message.content.startswith('$startbet'): # $startbet 100 valorant game 
        tokens = message.word_tokenize(message)
        amount = tokens[1]
        subject = numpy.split(tokens, 2)
        subject = join(subject)
        startBet(message.author, amount, subject)

async def startBet(host, amount, subject) :
    await message.channel.send(host + "has created a " + amount +" bet on " + subject)
    await message.channel.send("React with yes to bet for, react with to bet against")
    
    
    
    
client.run('OTYyNDU1MTI3ODI5MTMxMjk0.YlHyMA.dBSEzhwFMhI8nEXXs6iLXBPy0N8')