import discord
from discord.ext import commands


class Main:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def hi(self, ctx):
        await self.bot.say("Hello, there! o/")

