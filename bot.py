import os
import time
import discord
import logging
import random as r
from setup import *
from discord.ext import commands


on_ready_run= False
bot = commands.AutoShardedBot(
    command_prefix= commands.when_mentioned_or('$', 'sc$'),
    owner_id= 272967064531238912,
    case_sensetive= True)


# Setup events
@bot.event
async def on_ready():
    """My async setup function"""

    bot.admins = [await bot.get_user_info(admin) for admin in [
        272967064531238912, # Me
        297229962971447297, # Jack
        454928254558535700, # Dana
    ]]

    bot.current_status = await change_status(bot)
    print(f'Logged in as {bot.user} ({len(list(bot.get_all_members()))} users across {len(bot.guilds)} guilds)')


    bot.commands_run = bot.non_admin_commands_run = 0
    bot.initial_cogs = [
        "general", "fun", "currency",
        "memey", "text", "admin",
    ]
    

    bot.remove_command("help")
    bot.no_bypass_cooldown_commands = ["daily"]
    for cog in bot.initial_cogs: bot.load_extension(f"cogs.{cog}")

    if bot.user.id == 492873992982757406: await bot.get_channel(542961329867063326).send(embed= discord.Embed(
        title= "Bot restarted",
        description= get_time(),
        color= 0x00BFFF))


# Guild events
@bot.event
async def on_guild_join(guild):
    """Log joining a guild"""
    
    embed = discord.Embed(
        title= "Guild join",
        color= 0x228B22,
        description= f"Joined **{guild.name}** (**{guild.member_count- 1}** other members)")
    
    embed.set_thumbnail(url= guild.icon_url)
    embed.add_field(name= "Guild Members", value= guild.member_count)
    embed.add_field(name= "New Total Guilds", value= len(bot.guilds))

    await bot.get_channel(542474215282966549).send(embed= embed)

@bot.event
async def on_guild_remove(guild):
    """Log leaving a guild"""
    
    embed = discord.Embed(
        title= "Kicked from guild",
        color= 0xf44e42,
        description= f"Kicked from **{guild.name}** (**{guild.member_count- 1}** other members)")
    
    embed.set_thumbnail(url= guild.icon_url)
    embed.add_field(name= "Guild Members", value= guild.member_count)
    embed.add_field(name= "New Total Guilds", value= len(bot.guilds))

    await bot.get_channel(542474215282966549).send(embed= embed)


# Message events
@bot.before_invoke
async def before_invoke(ctx):
    """Setup refreshing data"""
    bot.send = SendEmbed(ctx).Send

@bot.event
async def on_command(ctx):
    """Log commands run"""
    
    embed = discord.Embed(title= "Command run", description= f"```{ctx.message.content}```", color= 0xf9e236)
    embed.add_field(name= "User", value= ctx.author)
    embed.add_field(name= "Channel", value= ctx.channel)
    embed.add_field(name= "Guild", value= ctx.guild)
    embed.set_thumbnail(url= ctx.guild.icon_url)
    embed.set_footer(text= ctx.author, icon_url= ctx.author.avatar_url)
    await bot.get_channel(542961329867063326).send(embed= embed)

    bot.commands_run += 1
    if ctx.author not in bot.admins: bot.non_admin_commands_run += 1


# Error events
@bot.event
async def on_command_error(ctx, error):
    """Handle errors"""
    
    embed = discord.Embed(color = r.randint(0, 0xFFFFFF))
    missing_param_errors = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError)
    
    if isinstance(error, commands.NotOwner):
        embed.title, embed.description= "Owner only command! :stop_button:", f"Lol I don't even know how you found this command but good job {emojis.thinkok}"

        await ctx.send(embed= embed)

    elif isinstance(error, commands.CommandOnCooldown):
        if user_in_support_guild(bot, ctx.message.author):
            if ctx.command.name not in bot.no_bypass_cooldown_commands: return await ctx.reinvoke()
            else: embed.title, embed.description= "Slow it down, cmon", str(error)
        
        else: embed.title, embed.description= "Slow it down, cmon", f"{str(error)}\n\n[Join the support guild]({SUPPORT_GUILD_INVITE}) and you won't have to wait!"
        await ctx.send(embed= embed)
    
    elif isinstance(error, missing_param_errors):
        await ctx.send(embed= discord.Embed(
            color= r.randint(0, 0xFFFFFF),
            title= "Incorrect usage of command",
            description= f"This is the correct usage:\n**{ctx.prefix}{ctx.command.signature}**"
        ))
    
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"thats not a command lol {emojis.partyparrot}")

    else:        
        embed.title, embed.color= f"An error occoured", 0xFF8C00
        embed.description= f"**Traceback:**\n```py\n{format_error(error)}```"

        await bot.get_channel(546570094449393665).send(embed= embed)

        embed.color, embed.title, embed.description = 0xFFA500, "💣 Oof, an error occoured 💥", \
            f"Please [join the support guild]({SUPPORT_GUILD_INVITE}) and tell **{bot.admins[0]}** what happened to help fix this bug"
        embed.set_footer(text= "< Look for this guy!", icon_url= bot.admins[0].avatar_url)

        await ctx.send(embed= embed)


# import webserver
# webserver.start_server(bot)
bot.run(os.getenv("BOT_TOKEN"))