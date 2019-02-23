import time
import discord
import random as r
from setup import emojis
from discord.ext import commands
from cogs.assets import paginator
from setup import VERSION, RUN_TIME

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= "help")
    async def _help(self, ctx, *, command: str = None):
        """Stop it, get some help"""
        
        try:
            if command is None:
                p = await paginator.HelpPaginator.from_bot(ctx)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command.lower())

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
            await p.paginate()
        except Exception as e:
            await ctx.send(e)


    @commands.command()
    async def info(self, ctx):
        """Info and stats about the bot"""
        embed = discord.Embed(
            color= r.randint(0, 0xFFFFFF),
            description= f"Here's the info for **{self.bot.user}**")
        fields = {
            "Developer :computer:": self.bot.admins[0],
            "Admin 1 :tickets:": self.bot.admins[1],
            "Admin 2 :golf:": self.bot.admins[2],
            "Servers :homes:": len(self.bot.guilds),
            "Total users :busts_in_silhouette:": len(list(self.bot.get_all_members())),
            "Version :white_check_mark:": VERSION,
            "Ping :ping_pong:": str(int(self.bot.latency*1000))+ "ms",
            "Last restart :calendar:": RUN_TIME,
            "Region :earth_asia:": "Australia",
            "Code platform :bow_and_arrow:": "Replit",
            "Hosting service :dart:": "Replit",
            "Language :airplane:": "discord.py rewrite\nPython 3.7"}

        for field in fields: embed.add_field(name= field, value= fields[field])
        await ctx.send(embed= embed)

        if ctx.author in self.bot.admins:
            embed = discord.Embed(description= "Admin stats", color= r.randint(0, 0xFFFFFF))
            fields = {"Commands run": self.bot.commands_run, "Commands run not admin": self.bot.non_admin_commands_run}
            for field in fields: embed.add_field(name= field, value= fields[field])
            await ctx.send(embed= embed)


    @commands.command()
    @commands.cooldown(2, 60)
    async def suggest(self, ctx, *, suggestion):
        """Suggest a feature, command or report a bug!"""
        
        embed = discord.Embed(
            title= f"Suggestion recieved from {ctx.author.name}",
            description= f"{ctx.author.mention}: {suggestion}",
            color= r.randint(0, 0xFFFFFF))
        embed.set_footer(text= ctx.author, icon_url= ctx.author.avatar_url)

        await self.bot.get_channel(502963219879559168).send(embed= embed, files= files)
        await ctx.send(embed= discord.Embed(
            color= r.randint(0, 0xFFFFFF),
            title= "Suggestion recieved",
            description= "We'll get back to you shortly"
        ))


    @commands.command()
    @commands.cooldown(1, 5)
    async def invite(self, ctx):
        await self.bot.send(
            "**:mailbox_with_mail: Invite :homes:**",
            f"""Invite me to your server [here]({BOT_INVITE_LINK})
            Join my support server: {SUPPORT_GUILD_INVITE}""")
    

    @commands.command()
    @commands.cooldown(3, 10)
    async def vote(self, ctx):
        await self.bot.send("**:arrow_up: Upvote links :newspaper2:**",
            " - [**Discord Bot List**](https://discordbotlist.com/bots/492873992982757406/upvote)")


def setup(bot): bot.add_cog(General(bot))