# Importing #
import os
import praw
import time
import random
# import dotenv
import discord
import asyncio
from util import *

# Setup #
client = discord.Client()
# dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env")) # Load .env for local testing
reddit = praw.Reddit(
    user_agent= "Reddit Searching for Savage Cabbage#3666",
    client_id= os.getenv("REDDIT_ID"),
    client_secret= os.getenv("REDDIT_TOKEN"),
)


# Once setup finished #
@client.event
async def on_ready():
    global total_users
    total_users = 0
    for server in client.servers:
        for user in server.members:
            total_users += 1

    print(f"\tLogged in as {client.user}\n\tServer count: {len(client.servers)}\n\tMember count: {total_users}")

    await client.change_presence(game=discord.Game(name=
        "russian roulette 🔫 (unstable as I'm hosting on my local computer for devving)"
        # f"$help |~| Insulting {total_users} users across {len(client.servers)} servers |~| {random.choice(roasts_no_bold)}"
    ))


@client.event
async def on_message(m):
    if m.author.bot:
        return
    devs, admin, msg, cmd, args = await message_setup(m, client)

    # Send function #
    async def send(title, message, footer=None, channel=m.channel, sendTyping=True):
        if sendTyping:
            await client.send_typing(channel)
            await asyncio.sleep(0.75)

        embed = discord.Embed(
            title=title,
            description=message,
            color=discord.Color(random.randint(0, 0xFFFFFF)),
        )

        if footer:
            embed.set_footer(text=footer)
        await client.send_message(channel, embed=embed)

    if msg[0] == "$":  # Command
        print('Command run:', m.author, cmd, args)
        # General
        if cmd in ["help"]:
            await send(":tools: Help :gear:",
                f"""
                Every time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted (Send `$roasts` for the insults)
                To prevent a user from being roasted, add `don\'t roast the roaster` to thier roles
            
                Please consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)
                """)

        elif cmd in ["info"]:
            await send("🇮 Info :thinking:",
                f"""Created by {devs[0].mention} ({devs[0]})
                Admins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})
                Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""",
                "Code on GitHub, hosted with Heroku")

        elif cmd in ["invite", "invites"]:
            await send("**:mailbox_with_mail: Invite :homes:**",
                f"""Invite me to your server [here](https://discordapp.com/oauth2/authorize?client_id=492873992982757406&scope=bot&permissions=201590848)
                Join my support server: https://discord.gg/AJj45Sj""")

        elif cmd in ["upvote"]:
            await send("**:arrow_up: Upvote :newspaper2:**",
                "[**Discord Bot List**](https://discordbotlist.com/bots/492873992982757406/upvote)")

        # Roast
        elif cmd in ["roast"]:
            if not args:
                await send(random.choice(greetings) + " " + m.author.name + ",",
                    random.choice(roasts))
            else:
                await send(random.choice(greetings) + " " + " ".join(args) + ",",
                    random.choice(roasts))

        # Memes
        elif cmd in ["reddit", "meme"]:
            _ = time.time()
            await client.send_typing(m.channel)
            while True:
                if args:
                    r_sub = reddit.subreddit("+".join(args)).random()
                else:
                    r_sub = reddit.subreddit("+".join([
                        "meirl", "me_irl",
                        "dankmemes", "PrequelMemes",
                        "Hmmm", "wholesomememes",
                        "MinecraftMemes",
                        # "DeepFriedMemes",
                    ])).random()
                if r_sub.url.endswith(".png") or r_sub.url.endswith(".jpg"):
                    reddit_embed = discord.Embed(title=r_sub.title)
                    reddit_embed.set_image(url=r_sub.url)
                    reddit_embed.set_footer(text=f"⬆ {r_sub.score} 💭 {r_sub.num_comments}")
                    await client.send_message(m.channel, embed=reddit_embed)
                    await send('',str(round(time.time()-_, 3))+ ' sec', sendTyping=False)
                    break
                else:
                    continue


client.run(os.getenv("BOT_TOKEN"))