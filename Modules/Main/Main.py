import discord
from discord.ext import commands
from Modules.Base.Base import Base, BaseInstance


class Main(Base):  # main cog
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


class MainInstance(BaseInstance):  # hold the properties that this module needs
    def convert_to_dictionary(self):
        return dict()