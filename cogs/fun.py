import discord
import asyncio
import random as r
from discord.ext import commands
from setup import eightball_answers

class Fun:
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


    @commands.cooldown(2, 5)
    @commands.command()
    async def spr(self, ctx, option):
        try: userchoice = {"✂": "scissors", "📰": "paper", "🗞": "paper"}[option.lower()]
        except KeyError: return await self.bot.send("", "Please use a valid option from **scissors**, **paper**, **rock**, 🗞 and 📰")
        if userchoice not in ["scissors", "paper", "rock"]: return await self.bot.send("", "Please use a valid option from **scissors**, **paper**, **rock**, 🗞 and 📰")
    
        compchoice = r.choice(["scissors", "paper", "rock"])
        # if userchoice == compchoice: result = "It's a tie!"
        # if userchoice == "scissors" and compchoice == "paper": result = "You win!"
        # if userchoice == "paper" and compchoice == "rock": result = "You win!"
        # if userchoice == "rock" and compchoice == "scissors": result = "You win!"
        # else: result = "I win!"
        
        if userchoice == compchoice: result = "It's a tie!"
        if (userchoice == "scissors" and compchoice == "paper") or \
            (userchoice == "paper" and compchoice == "rock") or \
                (userchoice == "rock" and compchoice == "scissors"): \
                    result = "You win!"
        else: result = "I win!"

        await ctx.send(discord.Embed(
            color= r.randint(0, 0xFFFFFF),
            title= f":scissors: SPR with {ctx.author} :newspaper:",
            description= f"I chose **{compchoice}** and you chose **{userchoice}**, **{result}**",
        ))


    @commands.command()
    @commands.cooldown(3, 6)
    async def hack(self, ctx, user: discord.User):
        progresses = ["▯▯▯▯", "▮▯▯▯", "▮▮▯▯", "▮▮▮▯", "▮▮▮▮"]
        embed = discord.Embed(
            title= progresses[0], description= "Hacking in progress",
            color= discord.Color(r.randint(0, 0xFFFFFF)))
        msg = ctx.send(embed= embed)
        await asyncio.sleep(2)

        if not user.bot: data = (
            ("Finding email address...", "Email", f"{m.mentions[0].name.replace(' ','_')}@{r.choice(hack_emails)}", "❌ Attempt blocked"),
            ("Finding IP address...", "IP Address", ".".join(map(str, (r.randint(0, 255) for _ in range(4)))), "❌ Attempt blocked"),
            ("Collecting passwords...", "Password", "||ShAggy_15_G0d||", "❌ Attempt blocked"),
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