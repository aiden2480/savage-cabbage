# Importing
import os
import sys
import praw
import time
import random
import discord
import traceback
from datetime import datetime as dt

# Format time var
if True:
    _ = str(dt.now())[:19].split()
    __= _[1]
    _= _[0].split('-')
    _.reverse()
    run_time= (" ".join(["/".join(_), __]), time.time())

# Functions
async def message_setup(m, client):
    _devs = [
        await client.get_user_info(id)
        for id in [
            272967064531238912,  # Me
            270138433370849280,  # Jensen
            297229962971447297,  # Jack
            499740673424097303,  # Alt
        ]
    ]

    _admin= m.author in _devs    
    _total_users= 0

    for server in client.servers:
        for member in server.members:
            _total_users+= 1
    
    _in_support_server= m.author in client.get_server(str(496081601755611137)).members

    return _devs, _admin, _total_users, _in_support_server

async def change_status(client, dev, *message):
    status = random.choice([
        # Playing
        (0, "Tetris"),
        # (0, "with ya mum (We're playing connect 4, what did you think?)"),

        # Streaming
        (1, "◉_◉"),
        (1, "⌐■_■"),
        (1, "(ง’̀-‘́)ง"),
        (1, "( ͡ᵔ ͜ʖ ͡ᵔ )"),
        (1, "¯\_(ツ)_/¯"),
        (1, "(づ￣ ³￣)づ"),
        (1, "(╯°□°）╯︵ ┻━┻"),
        (1, "┬─┬ ノ( ゜-゜ノ)"),
        (1, "╭∩╮（︶︿︶）╭∩╮"),
        (1, "┻━┻ ︵ ＼( °□° )／ ︵ ┻━┻"),

        # Listening to
        (2, "ASMR"),
        (2, "the voices in my head"),
        (2, "desu desu desu 10 hours"),
        (2, "my dev banging his head on the keyboard"),
        
        # Watching
        (3, "out for nonces"),
        (3, f"{dev} code!"),
        (3, "Hamezza on YouTube"),
        # (3, "Hentai with Jensen"),
    ])

    status = (status[0], status[1]+ ' |~| $help |~| please fill out the bit.ly/savage-cabbage-survey')
    if message: status = (status[0], '%s |~| %s' % (status[1], message[0]))

    await client.change_presence(
        game= discord.Game(
            name= status[1],
            type= status[0],
            url= "https://twitch.tv/chocolatejade42",
        ))
    
    return status # Type tuple

def tb_to_str(tb: tuple):
    try:
        _= ""
        for line in traceback.TracebackException(
            type(tb[0]), tb[1], tb[2]
        ).format(chain= True): _+= line
        return _
    except AttributeError: return None


# Classes
class emojis:
    partyparrot= "<a:partyparrot:538925147634008067>"

class AttrDict(dict):
    def __getattr__(self, attr): return self[attr]
    def __setattr__(self, attr, value): self[attr] = value


# Commands variables
CMDS = AttrDict({
    # General
    'help': ['Your average help message', ['cmds', 'whatsthis'], 'general'],
    'info': ['Stats about the bot', [None], 'general'],
    'status': ['Change my status 🤗', [None], 'general'],
    'invite': ['Invite links for the bot', ['invites'], 'general'],
    'vote': ['Vote for the bot on Discord bot lists', ["upvote"], 'general'],
    
    # DM commands
    'suggest': ['Suggest stuff for the bot and report bugs', ['bug'], 'dm'],

    # Roast
    'roast': ['Utterly obliviate someone\'s self-esteem', ['burn', 'feelsbadman'], 'roast'],

    # Meme
    'meme': ['Get the freshest memes around', ['reddit'], 'memey'],

    # Image
    'imgur': ["Get images from imgur!", ["image"], 'image'],
    
    # Text
    'partyparrot': ['Send kewl messages with partyparrot', ['party'], 'text'],

    # Fun commands
    '8ball': ['Ask the all-mighty, all-knowing 🎱!', [None], 'fun'],
    'spr': ['Play spr!', [None], 'fun'],
    #'ttt': ['Play Tic Tac Toe!', ['tictactoe'], 'fun'],
})

CMDS_LIST= list(CMDS)
CMD_CLASSES= list(sorted(set([CMDS[command][2] for command in CMDS])))
CLASS_CMDS= {class_: [] for class_ in CMD_CLASSES}

for class_ in CMD_CLASSES:
    for command in CMDS:
        if CMDS[command][2] == class_:
            CLASS_CMDS[class_].append(command)

# Load .env (if locally hosting)
try:
    import dotenv
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ModuleNotFoundError: pass

# Setup third-party authentication
reddit= praw.Reddit(
    user_agent= "Reddit Searching for Savage Cabbage#3666",
    client_id= os.getenv("REDDIT_ID"),
    client_secret= os.getenv("REDDIT_TOKEN"))
imgur_auth= "Client-ID "+ os.getenv("IMGUR_ID")

# Roasts list
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
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. **I think you owe it an apology**",
]

# Eightball answers for the 8ball command
eightball_answers= [
    # Yes
    "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Duh, of course", "hella",
    # Maybe
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "whaaaaat? y u no *concentrate*?", 
    # No
    "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.", "Heck no", "u wish", 
]

# Other variables and data setup
commands_run= commands_run_not_admin= 0
roasts_str= ""

one_in_what= 15
greetings= ["Hey", "Yo", "Wassup", "Oi"]
roasts_no_bold= [roast.replace("**", "") for roast in roasts]
for roast in sorted(roasts_no_bold): roasts_str+= f"{roast}\n"



SHARD_COUNT= 5
BOT_VERSION= "v0.3.5"

# Links and global
SUPPORT_SERVER_INVITE= "https://discord.gg/AJj45Sj"
BOT_INVITE_LINK= "https://discordapp.com/oauth2/authorize?client_id=492873992982757406&scope=bot&permissions=201641024&response_type=code&redirect_uri=https%3A%2F%2Fsavage-cabbage.herokuapp.com%2Fserver-invite"
