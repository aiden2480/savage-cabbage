import os
import time
import asyncio
import discord
import aiohttp
import datetime
import traceback
import random as r
from discord.ext import commands


# Load env for local testing
try:
    import dotenv
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ModuleNotFoundError: pass


# Classes
class SendEmbed:
    def __init__(self, ctx): self.bot, self.ctx = ctx.bot, ctx
    
    async def Send(self, title, message, color= r.randint(0, 0xFFFFFF), channel= None, **options):
        """Custom send function with embeds!"""
        
        # Setup embed
        messengable= channel or self.ctx
        is_param = lambda param: param in options.keys()
        embed = discord.Embed(title= title, description= message, color= color)

        # Add stuff to embed
        if is_param('fields'):
            for field in options['fields']:
                embed.add_field(name= field, value= options['fields'][field])
        if is_param('footer'): embed.set_footer(text= options['footer'])

        # Send
        return await messengable.send(embed= embed)

class emojis:
    # Non animated
    thinkok= "<:savagethinkok:547987410357846040>"
    coin= "<:coin:551663295799492611>"

    # Animated
    partyparrot= "<a:savagepartyparrot:538925147634008067>"


# Functions
async def prefix(bot, message):
    """No prefix needed for DM's"""
    prefixes= ["$"] # For Savage Cabbage
    if bot.user.id == 499721180379349016: prefixes= ["-"] # Savage Cabbage Beta
    if message.guild:
        try: prefixes = [bot.serverprefixes[str(message.guild.id)]]
        except KeyError: pass # No custom prefix
    if message.guild is None: prefixes.append("") # DM doesn't need prefix
    
    return commands.when_mentioned_or(*prefixes)(bot, message)

def tb_to_str(tb):
    """Takes a traceback and turns it into a string"""
    _= ""
    for line in TracebackException(
        type(tb[0]), tb[1], tb[2]
    ).format(chain= True): _+= line
    return _

def get_time():
    """Time in format DD/MM/YYYY HH:MM:SS (str)"""
    
    dt = str(datetime.datetime.now()).split()
    time = dt[1].split(".")[0]
    _date = dt[0].split("-")
    date = "/".join([_date[2], _date[1], _date[0]])
    
    return f"{date} {time}"

async def change_status(bot, *, type_text: tuple = None):
    """Change the bot's playing status"""
    if type_text == None: type_text= r.choice([
        # Playing
        (0, "Tetris"),
        (0, "Russian Roulette"),

        # Streaming
        (1, "◉_◉"),
        (1, "⌐■_■"),
        (1, "(ง’̀-‘́)ง"),
        (1, "( ͡ᵔ ͜ʖ ͡ᵔ )"),
        (1, "¯\_(ツ)_/¯"),
        (1, "(づ￣ ³￣)づ"),
        (1, "(╯°□°）╯︵ ┻━┻"),
        (1, "┬─┬ ノ( ゜-゜ノ)"),
        # (1, "╭∩╮（︶︿︶）╭∩╮"),
        (1, "┻━┻ ︵ ＼( °□° )／ ︵ ┻━┻"),

        # Listening to
        (2, "ASMR"),
        (2, "the voices in my head"),
        (2, "desu desu desu 10 hours"),
        (2, "my dev banging his head on the keyboard"),
        
        # Watching
        (3, "out for nonces"),
        (3, "Hamezza on YouTube"),
        (3, f"{bot.admins[0]} code!"),
    ])

    type_text = (int(type_text[0]), type_text[1])
    if type_text[0] == 0: await bot.change_presence(activity= discord.Game(name= type_text[1]))
    if type_text[0] == 1: await bot.change_presence(activity= discord.Streaming(name= type_text[1], url= "https://twitch.tv/chocolatejade42"))
    if type_text[0] == 2: await bot.change_presence(activity= discord.Activity(type= discord.ActivityType.listening, name= type_text[1]))
    if type_text[0] == 3: await bot.change_presence(activity= discord.Activity(type= discord.ActivityType.watching, name= type_text[1]))

    return type_text

async def aiohttpget(url):
    """GET a url via non-blocking aiohttp"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Lambdas
random_colour = lambda: r.randint(0, 0xFFFFFF)
user_in_support_guild = lambda bot, user: user in bot.get_guild(496081601755611137).members
format_error = lambda error: "\n".join(traceback.format_exception(type(error), error, error.__traceback__, 10))


# Logs
UPDATE_LOG = {
    "0.0.3": "yayeet",
    "0.0.2": "no u",
    "0.0.1": "Start development"
}


# Variables
RUN_TIME = get_time()
VERSION = list(UPDATE_LOG)[0]
SOURCE_CODE = "https://github.com/aiden2480/savage-cabbage"
SUPPORT_GUILD_INVITE = SUPPORT_SERVER_INVITE = "https://discord.gg/AJj45Sj"
WEBSITE_HOMEPAGE = "https://savage-cabbage.chocolatejade42.repl.co" # "https://savage-cabbage.herokuapp.com"
BOT_INVITE_LINK = discord.utils.oauth_url(492873992982757406, permissions= discord.Permissions(201641024), redirect_uri= SUPPORT_GUILD_INVITE)
# Permissions: add_reactions, attach_files, change_nickname, embed_links, external_emojis, manage_nicknames, read_messages, send_messages


# Long lists
roasts = [
    "Heck off!",
    "You are a dirt puddle!",
    "Go commit **neck-rope**",
    "Go commit **bullet-face**",
    "You're fatter than big smoke",
    "Go commit **choke-on-water**",
    "You are smelly and not very smart",
    "You have a face made for **radio**",
    "Go commit **oxygen-not-reach-lung**",
    "Go commit **food-not-reach-stomach**",
    "You are the reason **I doubt evolution**",
    "I'm jealous of people that don't know you",
    "A million years of evolution and **we get you???**",
    "You're as useless as **handles** on a **snowball**",
    "To which foundation do I need to donate to help you?",
    "You're the reason the gene pool **needs a lifeguard**",
    "You're so ugly that Hello Kitty said **goodbye** to you",
    "You're as bright as a black hole, and **twice** as dense",
    "Your birth certificate is an **apology from the hospital**",
    "You're as useless as **ejection seats** on a **helicopter**",
    "You bring everyone a lot of joy when you **leave the room**",
    "Well I could agree with you, but then **we'd both be wrong**",
    "I don't have the time **nor the crayons** to explain it to you",
    "You have a face only a mother could love - **and she hates it!**",
    "Stephen Hawking did great with his disability, **why can't you**?",
    "Somebody once told me that you aren't the sharpest tool in the shed",
    "If what you don't know can't hurt you, you must be **invulnerable!**",
    "You've got a photographic memory but **with the lens cover glued on**",
    "I bet your brain feels as good as new, seeing as **you never use it**",
    "You must have a very low opinion of people if you think they are your equals",
    "Roses are red, Violets are blue, God made me pretty, **What happened to you**?",
    "I'd tell you to go outside, but that would just **ruin everyone else's day** too",
    "There are several people in this world that I find obnoxious and you are **all of them**",
    "Yo mama so is so stupid that she climbed over a glass wall **to see what was behind it**",
    "I would have liked to insult you, but with your intelligence, **it would have been a compliment**",
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. **I think you owe it an apology**"]

eightball_answers= [
    # Yes
    "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Duh, of course", "hella",
    # Maybe
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "whaaaaat? y u no *concentrate*?", 
    # No
    "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.", "Heck no", "u wish"]

hack_emails = [
    "icloud.com", "gmail.com", "yahoo.com",
    "mememail.com", "hotmail.com", "shaggy.org"]

# Other variables and data setup
roasts_str = ""
one_in_what = 15
greetings = ["Hey", "Yo", "Wassup", "Oi"]
roasts_no_bold = [roast.replace("**", "") for roast in roasts]
for roast in sorted(roasts_no_bold, key= len): roasts_str += f"{roast}\n"
_runtime_ = time.time()