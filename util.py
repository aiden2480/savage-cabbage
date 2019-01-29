# This is the stuff that is constantly changing

import time
import random
import discord
from setup import AttrDict

# Message setup function #
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


CMDS = AttrDict({ # 'cmd': ['Description of help message', [Aliases], classifier]
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