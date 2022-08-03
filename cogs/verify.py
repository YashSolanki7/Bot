import asyncio
import json
import random

import aiofiles
import ctx
import discord
from random import randint
from discord.ext import commands
from captcha.image import ImageCaptcha

from Javier import bot


class VerifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    async def verify(self, ctx):
        sender = ctx.author

        image = ImageCaptcha(width=280, height=90)
        captcha_text = random.randint(100000, 9999999)

        captcha_text = str(captcha_text)

        data = image.generate(captcha_text)

        role_has = discord.utils.get(ctx.guild.roles, name='User')

        if role_has in ctx.author.roles:
            await ctx.send('You are verified')
        else:
            await ctx.send('Check your DMs!')

            image.write(captcha_text, 'captcha/CAPTCHA.png')

            await sender.send('Write the captcha!', file=discord.File('captcha/CAPTCHA.png'))

            print(captcha_text)

            while True:
                msg = await bot.wait_for("message", check=lambda check: check.author.id == ctx.author.id)

                if msg.guild == None:
                    break

            print(msg.content)

            if msg.content == captcha_text:
                await sender.send('You are verified')

                role = discord.utils.get(ctx.guild.roles, name='User')

                await sender.add_roles(role)
            else:
                await sender.send('Incorrect Capctha')


def setup(bot):
    bot.add_cog(VerifyCog(bot))
