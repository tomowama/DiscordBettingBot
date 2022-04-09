import discord.py

import discord
    
@client.event
async def on_ready():
    client.loop.create_task(benScan())
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('TOKEN')