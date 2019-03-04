import discord
import pyfiglet
from setup import emojis
from discord.ext import commands

class Text(commands.Cog):
    def __init__(self, bot): self.bot = bot
    
    
    @commands.command()
    @commands.cooldown(1, 2)
    async def partyparrot(self, ctx, *, text):
        """Send kewl messages with the partyparrot emoji"""
        await self.bot.send("", emojis.partyparrot.join(text.split()))
    

    @commands.command()
    @commands.cooldown(2, 3)
    async def emojify(self, ctx, *, text: str):
        result= ""
        for character in text:
            if character in list("abcdefghijklmnopqrstuvwxyz"):
                result += f":regional_indicator_{character.lower()}: "
            else: result += character.lower()
        await ctx.send(result)
    

    @commands.cooldown(2, 3)
    @commands.command(name= "ascii")
    async def _ascii(self, ctx, *, text):
        """Converts normal text into huge ascii text!"""
        if len(text) > 30: return await ctx.send("Maximum of `30` characters")
        
        if len(text) in range(1, 11): data = [
            str(pyfiglet.Figlet("univers").renderText(text)).replace("`", "`​")]
        if len(text) in range(11, 21): data= [
            str(pyfiglet.Figlet("univers").renderText(text[0:10])).replace("`", "`​"),
            str(pyfiglet.Figlet("univers").renderText(text[10:])).replace("`", "`​")]
        if len(text) in range(21, 31): data= [
            str(pyfiglet.Figlet("univers").renderText(text[0:10])).replace("`", "`​"),
            str(pyfiglet.Figlet("univers").renderText(text[10:20])).replace("`", "`​"),
            str(pyfiglet.Figlet("univers").renderText(text[20:])).replace("`", "`​")]
        
        for text in data: await ctx.send(f"```fix\n{text}```")


def setup(bot): bot.add_cog(Text(bot))