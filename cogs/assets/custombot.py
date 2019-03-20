from discord.ext import commands

class CustomBot(commands.Bot):
    # Create a banlist for the bot - its just users banned from the support server lol
    banlist= []
    # Admins for the bot; discord.User
    admins= []
    # Server prefixes that are requested from the database (WIP)
    serverprefixes= []
    # Commands that can't have thier cooldown bypassed by being in the support server
    no_bypass_cooldown_commands= ["daily"]
    
    # Logging how many comamnds are run
    commands_run = 0
    non_admin_commands_run = 0

    # The initial cogs to be loaded at startup
    initial_cogs = [
        # Command Cogs
        "general", "fun", # "currency",
        "memey", "text", "admin", "image",
        "animals", # "moderation",
        
        # Util cogs
        "assets.periodic"
    ]