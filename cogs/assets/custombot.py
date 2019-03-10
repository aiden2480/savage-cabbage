from discord.ext import commands

class CustomBot(commands.Bot):
    commands_run = non_admin_commands_run = 0
    
    serverprefixes= []
    no_bypass_cooldown_commands = ["daily"]
    banlist, initial_cogs = [], [
        "general", "fun", "currency",
        "memey", "text", "admin", "image",
        "moderation"
    ]