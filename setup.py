# Importing
import os
import praw
import time
import random
import discord

# Message setup function
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

    _admin = m.author in _devs
    _msg = m.content
    _cmd = _msg.split()[0][1:].lower()
    _args = _msg.split()[1:]

    return _devs, _admin, _msg, _cmd, _args

# Change bot status
async def change_status(client, dev, *message):
    status = random.choice([
        # Playing
        (0, "Tetris"),
        # (0, "█▀█ █▄█ ▀█▀"),
        (0, "with ya mum (We're playing connect 4, what did you think?)"),

        # Streaming
        (1, "¯\_(ツ)_/¯"),
        (1, "(╯°□°）╯︵ ┻━┻"),
        (1, "┬─┬ ノ( ゜-゜ノ)"),

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

    status = (status[0], status[1]+ ' |~| $help')
    if message: status = (status[0], '%s |~| %s' % (status[1], message[0]))

    await client.change_presence(
        game= discord.Game(
            name= status[1],
            type= status[0],
            url= "https://twitch.tv/chocolatejade42",
        ))
    
    return status # Type tuple

# Attribute Dictionary function (for accessing values as attributes)
class AttrDict(dict):
    def __getattr__(self, attr): return self[attr]
    def __setattr__(self, attr, value): self[attr] = value

# 'cmd': ['Description of help message', [Aliases], classifier]
CMDS = AttrDict({
    # General
    'help': ['Your average help message', [None], 'general'],
    'info': ['Stats about the bot', [None], 'general'],
    'status': ['Change my status :hugging:', [None], 'general'],
    'invite': ['Invite links for the bot', ['invites'], 'general'],
    'vote': ['Vote for the bot on Discord bot lists', ["upvote"], 'general'],
    
    # DM commands
    'suggest': ['Suggest stuff for the bot and report bugs idk', ['bug'], 'dm'],

    # Roast
    'roast': ['Utterly obliviate someone\'s self-esteem', ['burn', 'feelsbadman'], 'roast'],

    # Meme
    'reddit': ['Get the freshest memes around', ['meme'], 'meme'],

    # Text
    'partyparrot': ['Send kewl messages with <a:partyparrot:538925147634008067>', ['party'], 'text'],

    # Fun commands
    '8ball': ['Ask the all-mighty, all-knowing :8ball:!', [None], 'fun'],
    'spr': ['Play spr!', [None], 'fun'],
    'ttt': ['Play Tic Tac Toe!', ['tictactoe'], 'fun'],
})

CMD_CLASSES= list(set([CMDS[command][2] for command in CMDS]))

# Load .env for local testing
try:
    import dotenv
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ModuleNotFoundError: pass

# Setup reddit
reddit = praw.Reddit(
    user_agent= "Reddit Searching for Savage Cabbage#3666",
    client_id= os.getenv("REDDIT_ID"),
    client_secret= os.getenv("REDDIT_TOKEN"),
)

# Emojis code
class emojis:
    partyparrot = '<a:partyparrot:538925147634008067>'

# Roasts list
roasts = [
    # "Oof!",
    "Hecc off!",
    "You are a dirt puddle!",
    "Go commit **neck-rope**",
    "Go commit **bullet-face**",
    "You're fatter than big smoke",
    "Go commit **choke-on-water**",
    "You are smelly and not very smart",
    "You have a face made for **radio**",
    "Go commit **oxygen-not-reach-lung**",
    "Go commit **food-not-reach-stomach**",
    "You're so ugly that Hello Kitty said **goodbye** to you",
    # "I've seen some pricks in my life, but **you're a cactus!**",
    "You're as useless as **ejection seats** on a **helicopter**",
    "You bring everyone a lot of joy, when you **leave the room**",
    "If what you don't know can't hurt you, you must be **invulnerable!**",
    "Somebody once told me that you aren't the sharpest tool in the shed",
    "You've got a photographic memory but **with the lens cover glued on**",
    "Roses are red, Violets are blue, God made me pretty, **What happened to you**?",
    "There are several people in this world that I find obnoxious and you are **all of them**",
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. **I think you owe it an apology**"
    # "You're as straight as the pole your mum dances on"
]

# Eightball answers for the 8ball command
eightball_answers = [
    # Yes
    "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Duh, of course"
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
for roast in roasts_no_bold: roasts_str+= f"{roast}\n"