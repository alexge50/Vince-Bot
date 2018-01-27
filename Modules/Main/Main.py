import discord
from discord.ext import commands


class Main:  # main cog
    def __init__(self, bot, resource, personality_data):
        self.bot = bot
        self.resource = resource
        self.personality_data = personality_data

    def get_instance(self, serverid):
        return self.bot.instance_manager.get_instance(serverid)

    @commands.command(pass_context=True, no_pm=True)
    async def hi(self, ctx):
        bot_instance = self.get_instance(ctx.message.channel.server.id)
        await self.bot.say(self.personality_data[bot_instance.current_personality]["hi"].format(self.bot.name))

    @commands.command(pass_context=True, no_pm=True)
    async def change_personality(self, ctx, *, personality: str):
        bot_instance = self.get_instance(ctx.message.channel.server.id)
        if personality in self.bot.personalities:
            bot_instance.current_personality = personality
            bot_instance.update()
            key = "ok"
        else:
            key = "notok"
        await self.bot.say(
            self.personality_data[bot_instance.current_personality]["change_personality"][key].format(
                personality))

    @commands.command(pass_context=True, no_pm=True)
    async def gdbe(self, ctx):
        bot_instance = self.bot.instance_manager.get_instance(ctx.message.channel.server.id)

        await self.bot.say("```{}```".format(bot_instance.get_database_entry()))


class MainInstance:  # hold the properties that this module needs
    def __init__(self, bot_instance, entry=None, config=None):
        self.bot_instance = bot_instance
        if entry is not None:
            pass
        elif config is None:
            pass
        else:
            pass
            # it doesn't need any configuration

    def get_attributes(self):  # converts class' attributes to a dict, so the database can be updated
        return dict()
