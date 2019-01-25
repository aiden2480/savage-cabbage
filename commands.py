import random
import discord
from util import *

client = discord.Client()


class Misc:
    def __init__(self, Message):
        self.m = Message

    # Setup variables for messages #
    async def message_setup(self, client):
        _devs = [
            await client.get_user_info(id)
            for id in [
                272_967_064_531_238_912,  # Get
                270_138_433_370_849_280,  # users
                297_229_962_971_447_297,  # ID,
                499_740_673_424_097_303,  # but who?
            ]
        ]

        _admin = self.m.author in _devs
        _msg = self.m.content
        # _msg.split()[0] is the command prefix
        _cmd = _msg.split()[1].lower()
        _args = _msg.split()[2:]

        return _devs, _admin, _msg, _cmd, _args

    # Send function #
    async def send(self, title, message, footer=None, channel=None):
        if channel == None:
            channel = self.m.channel
        embed = discord.Embed(
            title=title, description=message, color=random.choice(message_colours)
        )

        if footer:
            embed.set_footer(text=footer)
        await client.send_message(channel, embed=embed)
send = Misc.send


class General:
    def __init__(self, Message):
        self.m = Message

    async def help(self, devs, client, total_users):
        return await send(
            self,
            ":tools: Help :wrench:",
            f"""**
        🇮 Info :thinking:**
        Every time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted (Send `$roasts` for the insults)
        To prevent a user from being roasted, add `don\'t roast the roaster` to thier roles
        
        Please consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)
        Created by {devs[0].mention} ({devs[0]})
        Admins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})
        Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""",
        )

    async def info(self):
        return await send(
            "Info",
            f"""Created by {devs[0].mention} ({devs[0]})
        Admins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})
        Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""",
        )


class Memes:
    def __init__(self, Message):
        self.m = Message

    async def reddit(self, reddit, search=None):
        while True:
            if search:
                r_sub = reddit.subreddit("+".join(args)).random()
            else:
                r_sub = reddit.subreddit("Unexpected").random()
            if r_sub.url.endswith(".png") or r_sub.url.endswith(".jpg"):
                reddit_embed = discord.Embed(title=r_sub.title)
                reddit_embed.set_image(url=r_sub.url)
                reddit_embed.set_footer(text=f"⭐ {r_sub.score} 💭 {r_sub.num_comments}")
                await client.send_message(m.channel, embed=reddit_embed)
                break
            else:
                continue


class Roasts:
    def __init__(self, Message):
        self.m = Message

    async def roast(self):
        pass
