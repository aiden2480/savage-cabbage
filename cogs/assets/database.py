"""
Database code that I use to try and connect to my online database, hopefully it works!
"""


import os
import json
import discord
import aiohttp
import asyncio


# Main Class
class Database:
    def __init__(self):
        async def init(self):
            self.base_url = os.getenv("DATABASE_URL")
            self.session= aiohttp.ClientSession()
        asyncio.run(init(s))
    

    # Main functions
    async def store(self, key, value):
        """Store data into the database using the POST method"""
        pass
    
    async def get(self, key, value):
        """Get data from the database using the GET method"""
        return json.loads(await self.session.get(self.__format_url__(key)))
    
    async def delete(self, key):
        """Delete data from the database using the DELETE method"""
        pass
    

    # Helper funcions
    def __format_url__(self, key):
        """Format the initial db url using the key given to make a better url 👌"""
        return f"{self.base_url}/{key}"
    
    async def __user_in_db_check__(self, user: discord.User):
    """Checks that a user has run a command before and is in my database, if not, adds them to it"""
        async with self.session.get(self.__format_url__(f"users/{user.id}")) as response:
            pass