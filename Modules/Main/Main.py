import discord
from discord.ext import commands
from Modules.Base.Base import Base, BaseInstance


class Main(Base):  # main cog
    @commands.command(pass_context=True, no_pm=True)
    async def hi(self, ctx):
        if self.check_permissions(ctx):
            bot_instance = self.get_instance(ctx)
            await self.bot.say(self.get_personality_data(bot_instance).format(self.bot.name))
        else:
            await self.bot.say("User does not meet required permissions")

    @commands.command(pass_context=True, no_pm=True)
    async def changepersonality(self, ctx, *, personality: str):
        if self.check_permissions(ctx):
            bot_instance = self.get_instance(ctx)
            if personality in self.bot.active_personalities:
                bot_instance.current_personality = personality
                bot_instance.update()
                key = "ok"
            else:
                key = "notok"
            await self.bot.say(self.get_personality_data(bot_instance)[key].format(personality))
        else:
            await self.bot.say("User does not meet required permissions")

    @commands.command(pass_context=True, no_pm=True)
    async def gdbe(self, ctx):
        if self.check_permissions(ctx) is True:
            bot_instance = self.get_instance(ctx)

            await self.bot.say("```{}```".format(bot_instance.get_database_entry()))

    @commands.command()
    async def raiseerror(self):
        raise Exception("raiseerror called")

    def help(self):
        return "Main is a module with default commands.", \
               {"hi": "Acts like a ping. Displays a salute message",
                "changepersonality": "This is command changes the personality with which the bot will \
                                      act in the current server. It requires Manage Server permissions."}


class MainInstance(BaseInstance):  # hold the properties that this module needs
    def convert_to_dictionary(self):
        return dict()
