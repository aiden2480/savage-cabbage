import os
import io
import praw
import json
import aiohttp
import discord
import textwrap
import datetime
import random as r
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from setup import greetings, roasts, roasts_str, aiohttpget

class Memey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            user_agent= "Praw scraping for Savage Cababge#3666",
            client_id= os.getenv("REDDIT_ID"),
            client_secret= os.getenv("REDDIT_TOKEN"))
    

    # Roasting
    @commands.group(aliases= ["burn", "bully"])
    @commands.cooldown(2, 3)
    async def roast(self, ctx):
        if ctx.invoked_subcommand is None: # Roast self (idk why u would though)
            await ctx.send(embed= discord.Embed(
                title= f"{r.choice(greetings)} {ctx.author.name},",
                description= r.choice(roasts),
                color= r.randint(0, 0xFFFFFF)
            ))
        
        if ctx.subcommand_passed is discord.User: # Roast another user (that's more like it)
            await ctx.send(embed= discord.Embed(
                title= f"{r.choice(greetings)} {str(ctx.subcommand_passed)},",
                description= r.choice(roasts),
                color= r.randint(0, 0xFFFFFF)
            ))
    
    #################################### NEED TO FIX ####################################
    @roast.command(name= "list")
    async def _list(self, ctx, page: int = 1):
        num_of_pages, left_over= divmod(len(pages), 5)
        if left_over: num_of_pages += 1
        if page not in range(1, num_of_pages+1): return await ctx.send(embed= discord.Embed(description= f"Invalid page number (pick from 1-{num_of_pages}", color= r.randint(0, 0xFFFFFF)))

        embed= discord.Embed(
            title= "You asked for it buddy",
            description= roasts_str.replace("\n", "\n\n"),
            color= r.randint(0, 0xFFFFFF))

        embed.set_footer(f"Page **{page}** of **{num_of_pages}**")
        await ctx.send(embed= embed)


    """
    # Make your own memes!
    @commands.cooldown(3, 10)
    @commands.group(aliases= ["makememe"])
    async def makeameme(self, ctx):
        if ctx.invoked_subcommand is None:
            embed= discord.Embed(title= "Make-a-meme!", description= "No Idea what to make as content, but hey, at least I added the embed colour right?", color= r.randint(0, 0xFFFFFF))
            embed.set_footer(text= f"First time? use '{ctx.prefix}makeameme example' for an example!")
            await ctx.send(embed= embed)
    

    @makeameme.command()
    async def example(self, ctx):
        embed= discord.Embed(
            title= "Make-a-meme!", color= r.randint(0, 0xFFFFFF),
            description= f"Format:\n```fix\n{ctx.prefix}makeameme <template> <top text>::<bottom text>```"
                f"Here's an example on how to use this command;\n```fix\n{ctx.prefix}makeameme tried at least::you tried```"
                "This command will produce the image to the upper right ↗️")
        embed.set_footer(text= f"'{ctx.prefix}makeameme templates' to view the meme templates")
        embed.set_thumbnail(url= "https://memegen.link/_dHJpZWQJYXRfbGVhc3QveW91X3RyaWVk.jpg")
        await ctx.send(embed= embed)


    @makeameme.command()
    async def templates(self, ctx):
        await ctx.send(embed= discord.Embed(
            title= "The different meme templates are;",
            description= "I really should make this command....",
            color= r.randint(0, 0xFFFFFF)
        ))"""

    # Quotes
    @commands.cooldown(2, 4)
    @commands.command(aliases= ["chucknorrisquote"])
    async def chucknorris(self, ctx):
        """Get chuck norris ~~jokes~~ facts"""
        await ctx.trigger_typing()

        data = json.loads(await aiohttpget("https://api.chucknorris.io/jokes/random"))
        embed = discord.Embed(description= data["value"], color= r.randint(0, 0xFFFFFF))
        embed.set_author(name= "Chuck Norris Fact", url= data["url"], icon_url= data["icon_url"])
        
        await ctx.send(embed= embed)
    

    @commands.cooldown(2, 4)
    @commands.command(aliases= ["donaldtrumpquote", "trumpquote"])
    async def donaldtrump(self, ctx):
        """Dumb quotes from the master of dumb quotes"""
        await ctx.trigger_typing()

        data = json.loads(await aiohttpget("https://api.tronalddump.io/random/quote"))
        embed = discord.Embed(description= data["value"], color= r.randint(0, 0xFFFFFF))
        embed.set_author(name= "Donald Trump Quote", url= data["_embedded"]["source"][0]["url"], icon_url= "https://docs.tronalddump.io/images/logo.png")
        
        await ctx.send(embed= embed)


    @commands.cooldown(2, 4)
    @commands.command(aliases= ["yomamajoke"])
    async def yomama(self, ctx):
        """yeah, its really much like the other 2"""
        await ctx.trigger_typing()

        data = json.loads(await aiohttpget("https://api.yomomma.info/"))
        embed = discord.Embed(description= data["joke"], color= r.randint(0, 0xFFFFFF))
        embed.set_author(name= "Yo Mama Joke", icon_url= "https://vignette.wikia.nocookie.net/deathbattlefanon/images/9/9e/4EA24A5C-67EE-45CE-8BD7-C37876575DA0.png")
        
        await ctx.send(embed= embed)


    @commands.command()
    @commands.cooldown(2, 4)
    async def dadjoke(self, ctx):
        """Dad jokes 🙄"""
        await ctx.trigger_typing()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com", headers= {"Accept": "application/json"}) as response:
                data = json.loads(await response.text())
        embed = discord.Embed(description= data["joke"], color= r.randint(0, 0xFFFFFF))
        embed.set_author(name= "Dad Joke", url= f"https://icanhazdadjoke.com/j/{data['id']}", icon_url= "https://images.discordapp.net/avatars/503720029456695306/cb6bb2fc3e552a68064d06f808d71fa8.png")
        
        await ctx.send(embed= embed)


    """
    # Reddit Scraping
    @commands.cooldown(3, 10)
    @commands.command(aliases= ["reddit"])
    async def meme(self, ctx, subreddit="dankmemes"):
        async with ctx.channel.typing():
            while True:
                r_sub = self.reddit.subreddit("+".join([
                    "meirl", "me_irl", "dankmemes", 
                    "Hmmm", "wholesomememes", "PrequelMemes",
                    "MinecraftMemes", "ROBLOXmemes", # "DeepFriedMemes",
                ])).random()

                #if r_sub.url.endswith(".png") or r_sub.url.endswith(".jpg"):
                    #embed = discord.Embed(title= r_sub.title, color= r.randint(0, 0xFFFFFF))
                    #embed= discord.Embed()
                    #embed.set_image(url= r_sub.url)
                    #embed.set_footer(text= f"⬆ {r_sub.score} 💭 {r_sub.num_comments}")
                    #print("got one!")
                    #await ctx.say(embed= embed)
                    #break
                #else: continue
    

    # Completely broken
    @commands.command()
    @commands.cooldown(3, 10)
    async def vr(self, ctx, *, text):
        embed = discord.Embed(color= r.randint(0, 0xFFFFFF))
        im = Image.open(io.BytesIO("cogs/assets/memey/templates/vr.jpg"))
        d = ImageDraw.Draw(im)
        d.text((60, 525), "\n".join(textwrap.wrap(text, 13)), (100, 100, 200), ImageFont.truetype("cogs/assets/memey/fonts/batmanforever.ttf", 25))
        d.text()
        
        im.save(f"cogs/assets/memey/temp/{ctx.author.id}.jpg")
        embed.set_image(url= f"attachment://cogs/assets/memey/temp/{ctx.author.id}.jpg")
        await ctx.send(embed= embed)
        os.remove(f"cogs/assets/memey/temp/{ctx.author.id}.jpg")"""
        

def setup(bot): bot.add_cog(Memey(bot))