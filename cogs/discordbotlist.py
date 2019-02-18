import os
import logging
import asyncio
import requests

class DiscordBotsListComAPI:
    """Handles interactions with the discordbotslist.com API"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('client')
        self.token = os.getenv("DISCORDBOTLIST_TOKEN")
        self.bot.loop.create_task(self.update_stats())
        self.requests = requests

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            self.logger.info('Attempting to post server count...')
            try:
                payload = {
                'guilds': len(list(self.bot.guilds)), 
                'users': len(self.bot.users)}
                headers = {'Authorization': f'Bot {self.token}'}
                url = f'https://discordbotlist.com/api/bots/{self.bot.user.id}/stats'
                r = requests.post(url,  headers= headers, data= payload)
                print(f'Status code:{r.status_code}')
            except Exception as e: self.logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__,e))
            await asyncio.sleep(1800)

class DiscordBotsGGAPI:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(DiscordBotsListComAPI(bot))
    bot.add_cog(DiscordBotsGGAPI(bot))