import os
import dbl
import json
import asyncio
import aiohttp
from discord.ext.commands import Bot, Cog

# Discord Bot sites
class DiscordBotsListComAPI(Cog):
    """POST data to the bots webpage on https://discordbotlist.com
    Data posted:
        - Guild Count
        - Total Users
        - Voice connections
    """
    
    def __init__(self, bot: Bot):
        self.bot, self.token = bot, os.getenv("DISCORDBOTLIST_TOKEN")
        self.dbl_header = {"Authorization": f"Bot {self.token}", "Content-Type": "application/json"}
        self.session = aiohttp.ClientSession(loop= bot.loop)
        self.bot.loop.create_task(self.poster())

    async def poster(self):
        while True:
            dbl_payload = {
                "guilds": len(self.bot.guilds),
                "users": len(self.bot.users)}
                # "voice_connections": len(self.bot.voice_clients)}
            
            async with self.session.post(
                f"https://discordbotlist.com/api/bots/{self.bot.user.id}/stats",
                headers= self.dbl_header, data= json.dumps(dbl_payload)) as dbl:
                    response = await dbl.text()
                    print('Guild count posted to DBL: [{}]: {}'.format(dbl.status, response))
            
            await asyncio.sleep(1500) # Repost every half hour

class DiscordBotsOrgAPI(Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot, self.token = bot, os.getenv("DBL_TOKEN")
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            try:
                await self.dblpy.post_server_count()
                print('posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                await self.bot.get_channel(546570094449393665).send('Failed to post server count to <https://discordbots.org>\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

# Update user info
async def setup_info(bot):
    """Frequently update stats such as
    - admin user info (names, avatars and the like)
    """
    
    while True:
        await asyncio.sleep(1500) # Refresh every half hour

        bot.admins = [await bot.get_user_info(admin) for admin in [
            272967064531238912, # Me
            454928254558535700, # Dana
            297229962971447297, # Jack
        ]]


def setup(bot: Bot):
    bot.loop.create_task(setup_info(bot))

    # bot.add_cog(DiscordBotsOrgAPI(bot)) # No token yet
    # bot.add_cog(DiscordBotsListComAPI(bot)) # Not posting for some reason