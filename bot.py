# Importing & setup #
import os, random, discord, asyncio
from commands import *
client = discord.Client()

async def send():
    pass
print('connected!')
# Once setup finished, event #
@client.event
async def on_ready():
    global total_users
    total_users = 0
    for server in client.servers:
        for user in server.members:
            total_users += 1

    print(f"\tServer count: {len(client.servers)}\n\tMember count: {total_users}")

    await client.change_presence(game=discord.Game(name=
        "with knives"#f"$help |~| Insulting {total_users} users across {len(client.servers)} servers |~| {random.choice(roasts_no_bold)}"
    ))

@client.event
async def on_message(m):
    if m.author.bot: return
    devs = await message_setup(m, client)

    print(m.content)
    if ".hi" in m.content:
        await client.send_message(m.channel, "yeet")

client.run(os.getenv("BOT_TOKEN"))