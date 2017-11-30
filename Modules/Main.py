import discord
from discord.ext import commands


class Main:  # main cog
    def __init__(self, bot, init_data):
        self.bot = bot
        self.name = init_data["name"]

    @commands.command(pass_context=True, no_pm=True)
    async def hi(self, ctx):
        await self.bot.say(self.bot.personalities[self.current_personality]["Vince"]["hi"].format(self.name))

    @commands.command(pass_context=True, no_pm=True)
    async def change_personality(self, ctx, *, personality: str):
        if personality in self.bot.personalities:
            self.bot.current_personality = personality
            key = "ok"
        else:
            key = "notok"
        await self.bot.say(self.bot.personalities[self.current_personality]["Vince"]["change_personality"][key].format(personality))
