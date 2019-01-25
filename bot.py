# Importing #
import os, praw, random, discord, asyncio
# from commands import *
from util import *

# Setup #
client = discord.Client()
general = General()
memes = Memes()
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',client_id=os.getenv('REDDIT_ID'),client_secret=os.getenv('REDDIT_TOKEN'))

# Globaling #
global m

# Functions #
async def message_setup(client, random):
    _devs = [await client.get_user_info(id) for id in [
        272967064531238912, # Get
        270138433370849280, # users
        297229962971447297, # ID,
        499740673424097303, # but who?
    ]]
    
    _admin = m.author in _devs
    _rand = random.randint(1, 15)
    _msg = m.content
    # _msg.split()[0] is the command prefix
    _cmd = _msg.split()[1].lower()
    _args = _msg.split()[2:]

    return _devs, _admin, _rand, _msg, _cmd, _args

async def send(title, message, footer = None, channel = m.channel):
    embed = discord.embed(
        title = title,
        description = message,
        color = random.choice(message_colours))
    
    if footer: embed.set_footer(text=footer)
    await client.send_message(channel, embed=embed)



# Command (classes) #
class General:
    async def help(m):
        return await send(":tools: Help :wrench:",f"""**
        🇮 Info :thinking:**
        Every time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted (Send `$roasts` for the insults)
        To prevent a user from being roasted, add `don\'t roast the roaster` to thier roles
        
        Please consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)
        Created by {devs[0].mention} ({devs[0]})
        Admins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})
        Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""")
    
    async def info(m):
        return await send('Info',f"""Created by {devs[0].mention} ({devs[0]})
        Admins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})
        Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""")

class Memes:
    async def reddit(m, reddit, search = None):
        while True:
            if search: r_sub = reddit.subreddit('+'.join(args)).random()
            else: r_sub = reddit.subreddit('Unexpected').random()
            if r_sub.url.endswith('.png') or r_sub.url.endswith('.jpg'):
                reddit_embed = discord.Embed(title= r_sub.title)
                reddit_embed.set_image(url= r_sub.url)
                reddit_embed.set_footer(text= f'⭐ {r_sub.score} 💭 {r_sub.num_comments}')
                await client.send_message(m.channel, embed= reddit_embed)
                break
            else: continue

class Roasts:
    async def roast(self):
        pass



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
        
        # Memes
        if cmd in ["meme"]:
            await memes.reddit(m, args)


client.run("NDkyODczOTkyOTgyNzU3NDA2.Dyvbaw.O1ON481O6y39td3OoAha0_LPerw")