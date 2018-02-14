import discord
from discord.ext import commands
from Modules.Base.Base import Base, BaseInstance


class Logger(Base):  # main cog
    @commands.command(pass_context=True, no_pm=True)
    async def setlogchannel(self, ctx):
        if self.check_permissions(ctx):
            bot_instance = self.get_instance(ctx)
            logger_instance = self.get_module(bot_instance, "Logger")
            logger_instance.log_channel = ctx.message.channel.id
            bot_instance.update()

            await self.say(
                self.get_personality_data(bot_instance).format(ctx.message.channel.id))
        else:
            await self.bot.say("User does not meet required permissions")

    async def on_message(self, message):
        bot_instance = self.get_instance(message)
        logger_instance = self.get_module(bot_instance, "Logger")

        if logger_instance.log_channel is not None and (message.channel.id != logger_instance.log_channel):
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            message_content = message.content
            message_content = message_content.replace("`", "'").replace("\n", "\n+ ")

            embed = discord.Embed(colour=discord.Colour(0x839827),
                                  description="<@{}>, <#{}>: ```diff\n+ {}```".format(
                                      message.author.id,
                                      message.channel.id,
                                      message_content
                                  ))

            await self.send_message(destination=log_channel, embed=embed)

    async def on_message_delete(self, message):
        bot_instance = self.get_instance(message)
        logger_instance = self.get_module(bot_instance, "Logger")

        if logger_instance.log_channel is not None and message.channel.id != logger_instance.log_channel:
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            message_content = message.content
            message_content = message_content.replace("`", "'").replace("\n", "\n- ")

            embed = discord.Embed(colour=discord.Colour(0xe53739),
                                  description="<@{}>, <#{}>: ```diff\n- {}```".format(
                                      message.author.id,
                                      message.channel.id,
                                      message_content
                                  ))

            await self.send_message(destination=log_channel, embed=embed)

    async def on_message_edit(self, before, after):
        bot_instance = self.get_instance(before)
        logger_instance = self.get_module(bot_instance, "Logger")

        if logger_instance.log_channel is not None and before.channel.id != logger_instance.log_channel:
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            before_content = before.content
            before_content = before_content.replace("`", "'").replace("\n", "\n- ")
            after_content = after.content
            after_content = after_content.replace("`", "'").replace("\n", "\n+ ")

            embed = discord.Embed(colour=discord.Colour(0xb46830),
                                  description="<@{}>, <#{}>:```diff\n- {}\n+ {}```".format(
                                            before.author.id,
                                            before.channel.id,
                                            before_content,
                                            after_content
                                        ))

            await self.send_message(destination=log_channel, embed=embed)

    def help(self):
        return "Logger is a module that logs message creation, deletion and changing events.", {
                "setlogchannel": "It sets the channel from which was invoked as the log channel. \
                                  It requires Manage Server permissions."}


class LoggerInstance(BaseInstance):
    def __init__(self, bot_instance, entry=None, config=None):
        self.log_channel = None
        super().__init__(bot_instance, entry, config)

    def init(self, config):
        self.log_channel = config["log_channel"]

    def convert_to_dictionary(self):
        return dict(log_channel=self.log_channel)
