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
        await ctx.channel.typing()

        while True:
            submission = self.reddit.subreddit("+".join([
                "dankmemes"
            ])).random()

            if submission.url.endswith(".png") or submission.url.endswith(".jpg"):
                embed = discord.Embed(title= submission.title)
                embed.set_image(url= submission.url)
                embed.set_footer(text= f"⬆ {submission.score} 💭 {submission.num_comments}")

                await ctx.send(embed= embed)
                break
            else: continue


def setup(bot): bot.add_cog(Memey(bot))