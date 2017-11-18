import discord
from discord.ext import commands

import json


class Vince:  # main cog
    def __init__(self, bot, init_data, personalities):
        self.bot = bot
        self.name = init_data["name"]
        self.personalities = personalities
        self.current_personality = "normal"

    @commands.command(pass_context=True, no_pm=True)
    async def hi(self, ctx):
        await self.bot.say(self.personalities[self.current_personality]["Vince"]["hi"].format(self.name))

    @commands.command(pass_context=True, no_pm=True)
    async def change_personality(self, ctx, *, personality: str):
        if personality in self.personalities:
            self.current_personality = personality
            key = "ok"
        else:
            key = "notok"
        await self.bot.say(self.personalities[self.current_personality]["Vince"]["change_personality"][key].format(personality))


bot = commands.Bot(command_prefix="v$")
token = None
vince = None


@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))


def init(config_file):
    global token
    global vince

    with open(config_file, "r") as f:
        json_config = json.load(f)

    with open(json_config["token_file"]) as f:
        token = f.read()

    with open(json_config["personalities_file"]) as f:
        personalities = json.load(f)

    vince = Vince(bot, json_config, personalities)
    bot.add_cog(vince)


def run():
    bot.run(token)
