import re
import random
import asyncio
import datetime

import discord
from discord.ext import commands

from utils.util import GetMessage


class Postrental(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="postrental",
        description="Post your rental!"
    )
    @commands.guild_only()
    @commands.has_role('User')
    async def postrental(self, ctx):
        await ctx.send("Lets start this Posting, answer the questions I ask and we shall proceed.")

        questionList = [
            ["What is the price of your rental?"," "],
            ["What location of your rental?"," "],
            ["How many rooms are available?", "  "],
            ["Write  a short description about your rental", "  "]
        ]
        listque = [
            ["Price", " "],
            ["Location", " "],
            ["Rooms Available", "  "],
            ["Description"," "]
        ]
        answers = {}

        for i, question in enumerate(questionList):
            answer = await GetMessage(self.bot, ctx, question[0], question[1])

            if not answer:
                await ctx.send("You failed to answer, please answer quicker next time.")
                return

            answers[i] = answer

        embed = discord.Embed(name="Rental Request")
        for key, value in answers.items():
            embed.add_field(name=f" `{listque[key][0]}`", value=f"-> `{value}`", inline=False)

        channel = ctx.channel
        await ctx.message.delete()
        limit = datetime.datetime.now() - datetime.timedelta(weeks=2)
        purged = await channel.purge(limit=12, after=limit)
        purged = len(purged)

        m = await ctx.send("Congrats! Your posting has been published \n Your posting will last for 3 days" , embed=embed)


        try:
            reaction, member = await self.bot.wait_for(
                "reaction_add",
                timeout=259200,
                check=lambda reaction, user: user == ctx.author
                and reaction.message.channel == ctx.channel
            )
        except asyncio.TimeoutError:
            await ctx.send("Confirmation Failure. Please try again.")
            return


def setup(bot):
    bot.add_cog(Postrental(bot))