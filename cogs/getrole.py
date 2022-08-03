import asyncio
import json

import aiofiles
import discord
from random import randint
from discord.ext import commands
from Javier import bot
from discord.utils import get


class Getrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
#1004217007375388683: access server
    @bot.listen('on_message')
    async def what(message):
        if message.channel.id == 1004212747858358404:
            if message.content.startswith('view'):
                embedvar = discord.Embed(title="React to this message to view the advertisments",
                                         description="Click the corresponding emoji to receive your role.\n<:download:1004218205113417859> - React here"

                                                , color=0x00ff00)

                msg = await message.channel.send(embed=embedvar)

                emoji1 = '<:download:1004218205113417859>'
                await msg.add_reaction(emoji1)
                print("Changed message embed color.")

            elif message.content.startswith('update'):
                embedvar2 = discord.Embed(title="React to this message to get your roles!",
                                          description="Click the corresponding emoji to receive your role.\n<:accd:978778815071408189> - React here"
                                                      "\n<:C_:847464916646494228> - "
                                                      "C++", color=0x00ff00)
                channel = bot.get_channel(1004212747858358404)
                msg = await channel.fetch_message(1004221181001486346)
                await msg.edit(embed=embedvar2)

                print("Updated role reaction message.")


    @bot.event
    async def on_raw_reaction_add(payload):
        guild = bot.get_guild(payload.guild_id)
        member = get(guild.members, id=payload.user_id)
        # channel and message IDs should be integer:
        if payload.channel_id == 1004212747858358404 and payload.message_id == 1004221181001486346:
            if str(payload.emoji) == "<:download:1004218205113417859>":
                role = get(payload.member.guild.roles, name='Access')
            else:
                role = get(guild.roles, name=payload.emoji)

            if role is not None:
                await payload.member.add_roles(role)
                print(f"Assigned {member} to {role}.")

    @bot.event
    async def on_raw_reaction_remove(payload):
        guild_id = payload.guild_id
        guild = bot.get_guild(guild_id)

        role = None
        if payload.channel_id == 1004212747858358404 and payload.message_id == 1004221181001486346:
            if str(payload.emoji) == "<:download:1004218205113417859>":
                role = discord.utils.get(guild.roles, name='Access')


            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print("done")
                else:
                    print("Member not found")
            else:
                print("Role not found")


def setup(bot):
    bot.add_cog(Getrole(bot))