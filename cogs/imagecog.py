import aiohttp
import discord
import asyncio
from io import BytesIO
from typing import Union
from functools import partial
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont


class ImageCog(commands.Cog):
    def __init__(self, bot: commands.Bot): self.bot, self.session= bot, aiohttp.ClientSession(loop= bot.loop)

    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:
        avatar_url = user.avatar_url_as(format= "png")
        async with self.session.get(avatar_url) as response: avatar_bytes = await response.read()
        return avatar_bytes

    @staticmethod
    def processing(avatar_bytes: bytes, colour: tuple) -> BytesIO:
        with Image.open(BytesIO(avatar_bytes)) as im:
            with Image.new("RGB", im.size, colour) as background:
                rgb_avatar = im.convert("RGB")
                with Image.new("L", im.size, 0) as mask:
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.ellipse([(0, 0), im.size], fill= 255)
                    background.paste(rgb_avatar, (0, 0), mask= mask)
                final_buffer = BytesIO()
                background.save(final_buffer, "png")
        final_buffer.seek(0)

        return final_buffer

    @commands.command()
    async def circle(self, ctx, *, member: discord.Member = None):
        """Display the user's avatar on their colour."""
        member = member or ctx.author

        async with ctx.typing():
            if isinstance(member, discord.Member): member_colour = member.colour.to_rgb()
            else: member_colour = (0, 0, 0)
            
            avatar_bytes = await self.get_avatar(member)
            fn = partial(self.processing, avatar_bytes, member_colour)
            final_buffer = await self.bot.loop.run_in_executor(None, fn)
            
            file = discord.File(filename="circle.png", fp=final_buffer)
            await ctx.send(file=file)
    
    """
    @commands.command()
    async def testvr(self, ctx, *, text= "text1"):
        async with ctx.typing():
            with Image.open(BytesIO("cogs/assets/memey/templates/vr.jpg")) as im:
                buffer= BytesIO()
                im.save(buffer, "jpg")
            buffer.seek(0)
            file= discord.File(filename= "vr.jpg", fp= buffer)
            await ctx.send(file= file1)
        
        async with ctx.typing():
            with open("cogs/assets/memey/templates/vr.jpg") as f:
                with Image.open(BytesIO(f.read())) as im:
                    buffer= BytesIO()
                    d, font = ImageDraw.Draw(im), ImageFont.truetype("cogs/assets/fonts/memey/batmanforever.ttf")
                    
                    d.text((60, 525), text, (100, 100, 200), font)
                    
                    im.save(buffer, "jpg")
            buffer.seek(0)
            file2 = discord.File(filename= "vr.jpg", fp= buffer)
            await ctx.send(file= file2)
        
        await asyncio.sleep(3)

        async with ctx.typing():
            with open("cogs/assets/memey/templates/vr.jpg", "rb") as f:
                im, buffer= Image.open(f.read()), BytesIO()
                d, font= ImageDraw.Draw(im), ImageFont.truetype("cogs/assets/memey/fonts/batmanforever.ttf")
                
        
                im.save(buffer, "JPEG")
            buffer.seek(0)
            await ctx.send(file= discord.File(filename= "vr.jpg", fp= buffer))
    """     


def setup(bot): bot.add_cog(ImageCog(bot))