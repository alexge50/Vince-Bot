import discord
from discord.ext import commands
from Modules.Base.Base import Base, BaseInstance


class Logger(Base):  # main cog
    @commands.command(pass_context=True, no_pm=True)
    async def log_here(self, ctx):
        bot_instance = self.get_instance(ctx.message.channel.server.id)
        logger_instance = self.get_module(bot_instance, "Logger")
        logger_instance.log_channel = ctx.message.channel.id
        bot_instance.update()

        await self.bot.say(
            self.get_personality_data(bot_instance)["log_here"].format(ctx.message.channel.id))

    async def on_message(self, message):
        bot_instance = self.get_instance(message.channel.server.id)
        logger_instance = self.get_module(bot_instance, "Logger")

        if logger_instance.log_channel is not None and (message.channel.id != logger_instance.log_channel):
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            message_content = message.content
            message_content = message_content.replace("`", "'").replace("\n", "\n+ ")

            await self.bot.send_message(log_channel,
                                        "<@{}>, <#{}>:```diff\n+ {}```".format(
                                            message.author.id,
                                            message.channel.id,
                                            message_content
                                        ))

    async def on_message_delete(self, message):
        bot_instance = self.get_instance(message.channel.server.id)
        logger_instance = self.get_module(bot_instance, "Logger")

        if logger_instance.log_channel is not None and message.channel.id != logger_instance.log_channel:
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            message_content = message.content
            message_content = message_content.replace("`", "'").replace("\n", "\n- ")

            await self.bot.send_message(log_channel,
                                        "<@{}>, <#{}>:```diff\n- {}```".format(
                                            message.author.id,
                                            message.channel.id,
                                            message_content
                                        ))

    async def on_message_edit(self, before, after):
        bot_instance = self.get_instance(before.channel.server.id)
        logger_instance = self.get_module(bot_instance, "Logger")

        if logger_instance.log_channel is not None and before.channel.id != logger_instance.log_channel:
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            before_content = before.content
            before_content = before_content.replace("`", "'").replace("\n", "\n- ")
            after_content = after.content
            after_content = after_content.replace("`", "'").replace("\n", "\n+ ")

            await self.bot.send_message(log_channel,
                                        "<@{}>, <#{}>:```diff\n- {}\n+ {}```".format(
                                            before.author.id,
                                            before.channel.id,
                                            before_content,
                                            after_content
                                        ))


class LoggerInstance(BaseInstance):
    def __init__(self, bot_instance, entry=None, config=None):
        super().__init__(bot_instance, entry, config)
        self.log_channel = None

    def init(self, config):
        self.log_channel = config["log_channel"]

    def convert_to_dictionary(self):
        return dict(log_channel= self.log_channel)
