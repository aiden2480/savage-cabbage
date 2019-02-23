import os
import asyncio
import requests

class DiscordBotsListComAPI:
    """Handles interactions with the discordbotslist.com API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv("DISCORDBOTLIST_TOKEN")
        self.bot.loop.create_task(self.update_stats())
        self.requests = requests

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            try:
                payload = {
                'guilds': len(list(self.bot.guilds)), 
                'users': len(self.bot.users)}
                headers = {'Authorization': f'Bot {self.token}'}
                url = f'https://discordbotlist.com/api/bots/{self.bot.user.id}/stats'
                r = requests.post(url,  headers= headers, data= payload)
                print(f'Status code:{r.status_code}')
            except Exception as e: self.logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__,e))
            await asyncio.sleep(1800) # Every 30 minutes
    
async def setup_info(bot):
    """Frequently update stats such as
    - admin user info
    """
    
    while True:
        bot.admins = [await bot.get_user_info(admin) for admin in [
            272967064531238912, # Me
            297229962971447297, # Jack
            454928254558535700, # Dana
        ]]
    
        await asyncio.sleep(2700) # Refresh every 45 mins

async def setup(bot):
    bot.loop.create_task(await setup_info(bot))
    # bot.add_cog(DiscordBotsListComAPI(bot))