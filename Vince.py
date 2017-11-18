import discord
from discord.ext import commands

import json


class Vince:  # main cog
    def __init__(self, bot, init_data):
        self.bot = bot
        self.name = init_data["name"]

    @commands.command(pass_context=True, no_pm=True)
    async def hi(self, ctx):
        await self.bot.say("Hi, I am {}, nice to meet you!".format(self.name))


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

    vince = Vince(bot, json_config)
    bot.add_cog(vince)


def run():
    bot.run(token)
