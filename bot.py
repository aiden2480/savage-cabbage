import os
import sys
import time
import discord
import logging
import random as r
from setup import *
from discord.ext import commands

bot = commands.AutoShardedBot(
    command_prefix= commands.when_mentioned_or('$'),
    owner_id= 272967064531238912,
    case_sensetive= True)

# Setup events
@bot.event
async def on_ready():
    """My async setup function"""
    
    await bot.change_presence(activity= discord.Game(name= "bot up!"))
    print(f'Logged in as {bot.user} ({len(list(bot.get_all_members()))} users across {len(bot.guilds)} guilds)')

    for cog in [
        "general", "currency"
    ]: bot.load_extension(f"cogs.{cog}")

    bot.commands_run = bot.non_admin_commands_run = 0
    bot.admins = [bot.get_user_info(admin) for admin in [
        272967064531238912,  # Me
        270138433370849280,  # Jensen
        297229962971447297,  # Jack
        499740673424097303,  # Alt
    ]]

    await bot.get_channel(542961329867063326).send(embed= discord.Embed(
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
    bot.send = SendEmbed(bot, ctx).Send

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
    no_bypass_cooldown_commands = ['daily']
    
    if isinstance(error, commands.CommandOnCooldown):
        if user_in_support_guild(bot, ctx.message.author):
            if ctx.command.name not in no_bypass_cooldown_commands: return await ctx.reinvoke()
            else: embed.title, embed.description= "Slow it down, cmon", str(error)
        
        else: embed.title, embed.description= "Slow it down, cmon", f"{str(error)}\n\n[Join the support guild]({SUPPORT_GUILD_INVITE}) and you won't have to wait!"
        await ctx.send(embed= embed)
    
    else:
        print(sys.exc_info())
        
        embed.title, embed.color= f"An error occoured", 0xFF8C00
        embed.description= f"**Traceback:**\n```{format_error(error)}```"

        await bot.get_channel(546570094449393665).send(embed= embed)

        await ctx.send(embed= discord.Embed(
            title= "💣 Oof, an error occoured 💥",
            description= f"Please [join the support guild]({SUPPORT_GUILD_INVITE}) and tell **{str(bot.get_user_info(272967064531238912))}** what happened to help fix this bug",
            color= 0xFFA500
        ))


bot.run(os.getenv("BOT_TOKEN"))