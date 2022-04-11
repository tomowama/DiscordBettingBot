from ast import Pass
from fileinput import close
from lib2to3.pgen2 import token
from ntpath import join
from tracemalloc import start
from unittest import result
import discord
import json

from numpy import place

client = discord.Client()





async def tokenize(s):
    arr = s.split(' ')
    arr.pop(0)
    
    if (len(arr) > 1):
        arr[0 : len(arr)] = [' '.join(arr[0 : len(arr)])]
    return arr

async def tokenizeBet(s):
    arr = s.split(' ')
    arr.pop(0)
    
    if len(arr) > 3:
        arr[2:len(arr)] = [' '.join(arr[2:len(arr)])]
    else:
        
        arr[1:len(arr)] = [' '.join(arr[1:len(arr)])]
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

    if message.content.startswith('$balance'):
        f = open('Source/balances.json', 'r')
        balances = json.load(f)
        f.close()
        
        ID = str(message.author.id)
        await message.channel.send(f"your balance is {balances[ID]}")
        
    if message.content.startswith('$startbet'): # $startbet valorant game

        name = await tokenize(message.content)
        
        
        print(name)
        await startBet(message.author.id, message.channel, name[0])
        
    if message.content.startswith('$placebet'): # send in the form "$placebet {value} {bet (t or f)} {name} "
        pass
        arr = await tokenizeBet(message.content)
        # print(arr)
        pts = int(arr[0])
        name = arr[2]
        bet = False
        if arr[1] == 't':
            bet = True
        
        ID = str(message.author.id)

        await placeBet(pts, name, message.channel, ID, bet)


    if message.content.startswith('$closebet'):
        arr = await tokenizeBet(message.content)
        
        result = False
        if arr[0] == 't':
            result = True
        name = arr[1]
        # print(arr)

        await closeBet(message.channel, result, name)
        await message.channel.send("bet has been closed.")


        
async def startBet(host, channel, name) :
    
    f = open('Source/bets.json', 'r')
    activeBets = json.load(f)
    f.close()

   
    if name in activeBets:
        await channel.send("Error: bet titled " + name + " already exists")
        return
    
    activeBets[name] = {}
    
    await channel.send(f"{host} has created a bet on {name}")
    await channel.send("React with yes to bet for, react with to bet against")
    
    
    with open('Source/bets.json', 'w') as f:
        json.dump(activeBets, f)
    f.close()

async def placeBet(points, name, channel, id, bet) : # $placebet 100 valorant game
    f = open('Source/bets.json', 'r')
    activeBets = json.load(f)
    f.close()
    f = open('Source/balances.json', 'r')
    balances = json.load(f)
    f.close()


    
    if  name not in activeBets :
        await channel.send("Error: bet titled " + name + " does not exist")
        return
    if id not in balances:
        balances[id] = "100"
    f = open('Source/balances.json', 'w')
    json.dump(balances, f)
    f.close()
    boolval = await removePoints(id, points)
    if (boolval) : #bets placed here
        print(f"type of points is {type(points)}")
        activeBets[name][id] = [points, bet]
        await channel.send("Bet Placed!")
    else:
        await channel.send("You don't have enough points") # add an @ for the person 
    
    with open('Source/bets.json', 'w') as f:
        json.dump(activeBets, f)
            
    f.close()
    

async def removePoints(id, points):
    f = open('Source/balances.json', 'r')
    balances = json.load(f)
    f.close()
    
    
    
    # if ( id not in balances) :
    #     balances[id] = 0
    bal = int(balances[str(id)])
    
    
    if (bal < points) :
        return False   
    
    
    bal -= int(points)
    balances[id] = str(bal)
    f = open('Source/balances.json', 'w')
    # json.dump(balances, f)
    f.write(json.dumps(balances))
            
    f.close()
    
    return True
    
async def closeBet(channel, result, name):
    f = open('Source/bets.json', 'r')
    activeBets = json.load(f)
    f.close()
    f = open('Source/balances.json', 'r')
    balances = json.load(f)
    f.close()
    for key in activeBets:
        for id in activeBets[key]:
            if activeBets[key][id][1] == result: #correct bet
                
                num = int(balances[id])
                value = int(activeBets[key][id][0])
                num += 2*value
                balances[id]= str(num)
                
                
    del activeBets[name]
    
    with open('Source/balances.json', 'w') as f:
        json.dump(balances, f)
            
    f.close()
    with open('Source/bets.json', 'w') as f:
        json.dump(activeBets, f)
            
    f.close()

    return True


client.run('OTYyNDU1MTI3ODI5MTMxMjk0.YlHyMA.n01LIb_TTT2Wz2J5TE3YgSE3F-U')