import os
import asyncio
import discord
import datetime
import random as r
from traceback import TracebackException

# Load env for local testing
try:
    import dotenv
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ModuleNotFoundError: pass

# Classes
class SendEmbed:
    def __init__(self, bot, ctx): self.bot, self.ctx = bot, ctx
    
    async def Send(self, title, message, color= r.randint(0, 0xFFFFFF), channel= None, **options):
        # Setup
        if channel == None: channel = self.ctx
        is_param = lambda param: param in options.keys()
        embed = discord.Embed(title= title, description= message, color= color)

        # Add stuff to embed
        if is_param('fields'):
            for field in options['fields']:
                embed.add_field(name= field, value= options['fields'][field])
        if is_param('footer'): embed.set_footer(text= options['footer'])

        # Send
        return await channel.send(embed= embed)

# Functions
def tb_to_str(tb: tuple):
    _= ""
    for line in TracebackException(
        type(tb[0]), tb[1], tb[2]
    ).format(chain= True): _+= line
    return _

def get_time():
    #"""Time in format DD/MM/YYYY HH:MM:SS"""
    dt = str(datetime.datetime.now()).split()
    time = dt[1].split(".")[0]
    _date = dt[0].split("-")
    date = "/".join([_date[2], _date[1], _date[0]])
    
    return f"{date} {time}"

# Lambdas
user_in_support_guild = lambda bot, user: user in bot.get_guild(496081601755611137).members
format_error = lambda error: "\n".join(traceback.format_exception(type(error), error, error.__traceback__, 10))

# Variables
SUPPORT_GUILD_INVITE = "https://discord.gg/AJj45Sj"
BOT_INVITE_URL = ""