from ast import Pass
from ntpath import join
from tracemalloc import start
import discord
import json

client = discord.Client()





async def tokenize(s):
    arr = s.split(' ')
    arr.pop(0)
    
    if (len(arr) > 1):
        arr[0 : len(arr)] = [' '.join(arr[1 : len(arr)])]
    return arr

@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client)) # 8===========D

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
    if message.content.startswith('test'):
        print(tokenize(message.content))
        
        await message.channel.send(message.content)
        
    if message.content.startswith('$startbet'): # $startbet valorant game

        name = await tokenize(message.content)
        
        
        print(name)
        await startBet(message.author.id, message.channel, name[0])
        


        
        
        

        # input
        



        # message.content.split("")


        #OLD CODE
        # tokens = message.word_tokenize(message)
        
        # amount = tokens[1]
        # subject = numpy.split(tokens, 2)
        # subject = join(subject)
        # startBet(message.author, amount, subject)


async def startBet(host, channel, name) :
    
    f = open('Source/bets.json', 'r')
    activeBets = json.load(f)
    f.close()

   
    if name in activeBets:
        await channel.send("Error: bet titled " + name + " already exists")
        return
    
    activeBets[name] = {}
    print(activeBets)
    await channel.send(f"{host} has created a bet on {name}")
    await channel.send("React with yes to bet for, react with to bet against")
    
    
    with open('Source/bets.json', 'w') as f:
        json.dump(activeBets, f)
    f.close()

async def placeBet(points, name, channel, id) : # $placebet 100 valorant game
    f = open('Source/bets.json', 'r')
    activeBets = json.load(f)
    f.close()
    
    if not name in activeBets :
        await channel.send("Error: bet titled " + name + " does not exist")
        return

    if (removePoints(id, points)) : #bets placed here
        
        activeBets[name][id] = points
        await channel.send("Bet Placed!")
    else:
        await channel.send("You don't have enough points") # add an @ for the person 
    
    with open('Source/bets.json', 'w') as f:
        json.dump(activeBets, f)
            
    f.close()
    
    
async def addPoints(id, points) :
    f = open('Source/balances.json', 'r')
    balances = json.load(f)
    f.close()
    
    if (not id in balances) :
        balances[id] = 0
        
    balances[id] += int(points)

    with open('Source/balances.json', 'w') as f:
        json.dump(balances, f)
            
    f.close()
    
    return True

async def removePoints(id, points) :
    f = open('Source/balances.json', 'r')
    balances = json.load(f)
    f.close()
    
    if (not id in balances) :
        balances[id] = 0
     
    if (balances[id] < points) :
        return False   
    
    balances[id] -= int(points)
    
    with open('balances.json', 'w') as f:
        json.dump(balances, f)
            
    f.close()
    
    return True
    
client.run('OTYyNDU1MTI3ODI5MTMxMjk0.YlHyMA.crSbD36OxFZIrSbPAlkumZqMz3w')