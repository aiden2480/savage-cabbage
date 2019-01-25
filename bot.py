# Importing #
import os, praw, random, discord, asyncio
from commands import *
from util import *

# Setup #
client = discord.Client()
#reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',client_id=os.getenv('REDDIT_ID'),client_secret=os.getenv('REDDIT_TOKEN'))

# Globaling #
global m

# Once setup finished #
@client.event
async def on_ready():
    global total_users
    total_users = 0
    for server in client.servers:
        for user in server.members:
            total_users += 1

    print(f"\tServer count: {len(client.servers)}\n\tMember count: {total_users}")

    await client.change_presence(game=discord.Game(name=
        #"russian roulette 🔫 (re-coding!) up by feb!" 
        f"$help |~| Insulting {total_users} users across {len(client.servers)} servers |~| {random.choice(roasts_no_bold)}"
    ))


@client.event
async def on_message(m):
    if m.author.bot:  return
    
    total_users = 0
    for server in client.servers:
        for member in server.members:
            total_users += 1
    general, memes, roasts, misc = General(m), Memes(m), Roasts(m), Misc(m)
    devs, admin, msg, cmd, args = await misc.message_setup(client) # Establish needed variables

    if msg.split()[0].lower() in ["hey,", "hey"]: # Command
        # General
        if cmd in ["help"]:
            await general.help(devs, client, total_users)
        if cmd in ["info"]:
            await general.info()
        
        # Memes
        if cmd in ["meme"]:
            await memes.reddit(m, args)


client.run(os.getenv("BOT_TOKEN"))