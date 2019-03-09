import time
import discord
import random as r
from discord.ext import commands
from setup import emojis, change_status
from setup import VERSION, RUN_TIME, BOT_INVITE_LINK, SUPPORT_GUILD_INVITE

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    '''
    # Help command
    @commands.group(name= "help")
    async def _help(self, ctx, *, command: str = None):
        """Stop it, get some help"""
        
        if ctx.invoked_subcommand is None:
            pass#await pass
        if ctx.invoked_subcommand
    '''



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
            "Code platform :bow_and_arrow:": "GitHub",
            "Hosting service :dart:": "Heroku",
            "Language :airplane:": "discord.py rewrite\nPython 3.7"}

        for field in fields: embed.add_field(name= field, value= fields[field])
        await ctx.send(embed= embed)

        if ctx.author in self.bot.admins:
            embed = discord.Embed(description= "**Admin stats**", color= r.randint(0, 0xFFFFFF))
            fields = {"Commands run": self.bot.commands_run, "Commands run not admin": self.bot.non_admin_commands_run}
            for field in fields: embed.add_field(name= field, value= fields[field])
            await ctx.send(embed= embed)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f":ping_pong: Pong - **{str(int(self.bot.latency*1000))}**ms :ping_pong:")


    @commands.cooldown(2, 10)
    @commands.command(name= "status", disabled= True)
    async def _status(self, ctx, *status):
        """Change my status!"""

        conversion = {0: "Playing", 1: "Streaming", 2: "Listening to", 3: "Watching"}
        if status == ():
            _ = await change_status(self.bot)
            await ctx.send(embed= discord.Embed(
                description= "ok, my status is now **{0} {1}**".format(conversion[_[0]], _[1]),
                color= r.randint(0, 0xFFFFFF)))
        elif ctx.author in self.bot.admins:
            embed= discord.Embed(title= "Admin status change", color= r.randint(0, 0xFFFFFF))
            try: _ = await change_status(self.bot, type_text= ({"playing": 0, "streaming": 1, "listeningto": 2, "watching": 3}[status[0]], " ".join(status[1:])))
            except (KeyError, IndexError): return await ctx.send(embed= discord.Embed(
                color= r.randint(0, 0xFFFFFF),
                description= f"Proper usage: `{ctx.prefix}status [playing|streaming|listeningto|watching] <status>`"))

            embed.description = "ok, my status is now **{0} {1}**".format(conversion[_[0]], _[1]),
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

        msg = await self.bot.get_channel(502963219879559168).send(embed= embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

        await ctx.send(embed= discord.Embed(
            color= r.randint(0, 0xFFFFFF),
            title= "Suggestion recieved",
            description= "We'll get back to you shortly"
        ))


    @commands.command()
    @commands.cooldown(1, 5)
    async def invite(self, ctx):
        """Invite the bot or join my support server"""
        await self.bot.send(
            "**:mailbox_with_mail: Invite :homes:**",
            f"""Invite me to your server [here]({BOT_INVITE_LINK})
            Join my support server: {SUPPORT_GUILD_INVITE}""")
    

    @commands.command()
    @commands.cooldown(3, 10)
    async def vote(self, ctx):
        """Vote for the bot on discord bot sites"""
        await self.bot.send("**:arrow_up: Upvote links :newspaper2:**",
            " - [**Discord Bot List**](https://discordbotlist.com/bots/492873992982757406/upvote)")
    

    @commands.cooldown(3, 5)
    @commands.command(aliases=["whois", "user-info"], disabled= True)
    async def userinfo(self, ctx, user: discord.Member):
        if user is None: user = ctx.author
                
        embed = discord.Embed(color=r.randint(0, 0xFFFFFF), title=f'User Info for {user.name}')
        embed.add_field(name='Status', value=f'{ctx.message.author.status}')       
        embed.add_field(name='Account Created', value=ctx.message.author.created_at.__format__('%A, %B %d, %Y'))
        embed.add_field(name='ID', value=f'{ctx.message.author.id}')
        embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed= embed)


def setup(bot): bot.add_cog(General(bot))