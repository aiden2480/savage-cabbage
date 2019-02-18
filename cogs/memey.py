import os
import io
import praw
import discord
import textwrap
import random as r
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

class Memey:
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            user_agent= "Praw scraping for Savage Cababge #3666",
            client_id= os.getenv("REDDIT_ID"),
            client_secret= os.getenv("REDDIT_TOKEN")
        )
    
    @commands.command(aliases= ["reddit"])
    async def meme(self, ctx):
        _ = time.time()
        
    
    #@commands.command()
    #async def spongebob1(self, ctx):
    #    pass
    
    #@commands.command()
    #async def spongebob2(self, ctx, *, text: str):
    #    im = Image.open('img_templates/spongebob2.jpg')
    #    d = ImageDraw.Draw(im)
    #    font = ImageFont.truetype('assets/batmanforever.ttf', 30)

    #    d.text((60, 85), '\n'.join(textwrap.wrap(text, 8)), font= font, fill= (100, 100, 200))
    #    em = discord.Embed(color= r.randint(0, 0xFFFFFF))

    #    em.set_image(io.BytesIO(im))
    #    await ctx.send(embed= em, file= discord.File(im, 'spongebob.jpg'))


def setup(bot): bot.add_cog(Memey(bot))