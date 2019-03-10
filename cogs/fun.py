import discord
import asyncio
import random as r
from discord.ext import commands
from setup import eightball_answers

class Fun(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.cooldown(2, 3)
    @commands.command(name= "8ball")
    async def eightball(self, ctx, *, question: str= None):
        """Ask the mystical 🎱 a question"""
        def check(ctx2): return ctx2.author == ctx.author
        
        if question is None:
            await self.bot.send("", "What do you want to ask the mystical 8ball? (c to cancel)")
            
            try: msg = await self.bot.wait_for("message", check= check, timeout= 15.0)
            except commands.CommandInvokeError or TimeoutError: return await bot.send("", "Timed out")
    
            else: await self.bot.send(f":8ball: {question} :rabbit2:", r.choice(eightball_answers))
        else: await self.bot.send(f":8ball: {question} :rabbit2:", r.choice(eightball_answers))


    @commands.command()
    @commands.cooldown(2, 5)
    async def spr(self, ctx, option):
        """Play spr with the bot"""
        try: userchoice = {"✂": "scissors", "📰": "paper", "🗞": "paper", "scissors": "scissors", "paper": "paper", "rock": "rock"}[option.lower()]
        except KeyError: return await self.bot.send("", "Please use a valid option from **scissors**, **paper**, **rock**, 🗞 and 📰")
    
        compchoice = r.choice(["scissors", "paper", "rock"])
        
        if userchoice == compchoice: result = "It's a tie!"
        if (userchoice == "scissors" and compchoice == "paper") or \
            (userchoice == "paper" and compchoice == "rock") or \
                (userchoice == "rock" and compchoice == "scissors"): \
                    result = "You win!"
        else: result = "I win!"

        await ctx.send(embed= discord.Embed(
            color= r.randint(0, 0xFFFFFF),
            title= f":scissors: SPR with {ctx.author} :newspaper:",
            description= f"I chose **{compchoice}** and you chose **{userchoice}**, **{result}**",
        ))


    @commands.command()
    @commands.cooldown(3, 6)
    async def hack(self, ctx, user: discord.User):
        """Hack a user or bot (Why does everyone have russian passwords???)"""
        progresses = ["▯▯▯▯", "▮▯▯▯", "▮▮▯▯", "▮▮▮▯", "▮▮▮▮"]
        emails = ["icloud.com", "gmail.com", "yahoo.com", "mememail.com", "hotmail.com", "shaggy.org"]
        passwords = [
            "vizaVilE", "lafozhiy", "oLyabAZh", "zhudyury", "miStotyA", "azHutimi", "nyAvapiG", "lihAepeT", "bzhuvedi", "ktipuvOR",
            "chuAzhTe", "tigoSokE", "kiloCHup", "tuVVtIaZ", "nyuRYAhu", "lyutDyuH", "vaboorma", "obschami", "IvoTsuzh", "duSchuOt",
            "lebiloch", "gurEliZH", "Shpizhzy", "shIzerUr", "holologi", "etyaRodV", "schaNIpe", "zumYANii", "nyanusch", "sugonoyu",
            "loRozyat", "helEzYUm", "dYuoscHi", "koGasAte", "tsaMarit", "saanturu", "edizEsor", "DefenUts", "bivYAoTk", "puNOroen",
            "dOpivogi", "motiveny", "SchatyUn", "chuNyApi", "pishoGaF", "HohoGAsy", "nyunisch", "hevoVomi", "votsisch", "TochaEgu"]
        embed = discord.Embed(
            title= progresses[0], description= "Hacking in progress",
            color= discord.Color(r.randint(0, 0xFFFFFF)))
        msg = await ctx.send(embed= embed)
        await asyncio.sleep(2)

        if not user.bot: data = (
            ("Finding email address...", "Email", f"{user.name.replace(' ','_')}@{r.choice(emails)}", "❌ Attempt blocked"),
            ("Finding IP address...", "IP Address", ".".join(map(str, (r.randint(0, 255) for _ in range(4)))), "❌ Attempt blocked"),
            ("Collecting passwords...", "Password", f"||{r.choice(passwords)}||", f"||{r.choice(passwords)}||"), # Always gets user password
            ("Selling data to facebook...", "Facebook", "Data sold! :dollar:", "❌ Insignificant data"))
        else: data = (
            ("Scrambling bot database...", "Database", "Nothing left :smiling_imp:", "❌ Attempt blocked"),
            ("Changing commands...", "Commands", "Scrambled!", "❌ Attempt blocked"),
            ("Changing playing status...", "Playing status", "Hacked!", "❌ Attempt blocked"),
            ("Leaving all servers...", "Servers", "All gone!", "❌ Attempt blocked"))

        _ = 0
        for action, short, choice1, choice2 in data:
            _ += 1
            embed.title, embed.description= progresses[_], action
            await msg.edit(embed= embed)
            await asyncio.sleep(r.randint(1500, 3000)/ 1000)

            embed.add_field(name= short, value= r.choice([choice1, choice1, choice1, choice2]))
            await msg.edit(embed= embed)
            await asyncio.sleep(2)
        embed.title, embed.description= "Hack complete", f"Finished hacking {user}"
        await msg.edit(embed= embed)


def setup(bot): bot.add_cog(Fun(bot))