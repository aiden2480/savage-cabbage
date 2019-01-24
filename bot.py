# Importing & setup #
import os, random, discord, asyncio
from commands import *
client = discord.Client()

async def send():
    pass

# Once setup finished, event #
@client.event
async def on_ready():
    global total_users
    total_users = 0
    for server in client.servers:
        for user in server.members:
            total_users += 1

    print(f"""\n
    |===============================|
    | Discord.py up, Server started |
    | I'm in as {client.user} |
    |===============================|
    | HTTP Requests,data and errors |
    |===============================|
    
    \tServer count: {len(client.servers)}
    \tMember count: {total_users}
    \n""")

    await client.change_presence(game=discord.Game(name=
        f"$help |~| Insulting {total_users} users across {len(client.servers)} servers |~| {random.choice(roasts_no_bold)}"
    ))

@client.event
async def on_message(m):
    if m.author.bot or m.author in blacklisted: return
    devs = await message_setup(m)



client.run(os.getenv("BOT_TOKEN"))