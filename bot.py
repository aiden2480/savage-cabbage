# Importing #
import os, praw, random, discord, asyncio
from commands import *
from util import *

# Setup #
client = discord.Client()
general = General()
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',client_id=os.getenv('REDDIT_ID'),client_secret=os.getenv('REDDIT_TOKEN'))
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
    devs, admin, rand, msg, cmd, args = await message_setup(m, client, random) # Establish needed variables

    if msg.split()[0].lower() in ["hey,", "hey"]: # Command
        # General
        if cmd in ["help"]:
            await general.help()
        if cmd in ["info"]:
            await general.info()
        
        #



client.run("NDkyODczOTkyOTgyNzU3NDA2.Dyvbaw.O1ON481O6y39td3OoAha0_LPerw")