import discord
from discord.ext import commands


class Logger:  # main cog
    def __init__(self, bot, resource, personality_data):
        self.bot = bot
        self.resource = resource
        self.personality_data = personality_data

    def get_instance(self, serverid):
        return self.bot.instance_manager.get_instance(serverid)

    @commands.command(pass_context=True, no_pm=True)
    async def log_here(self, ctx):
        bot_instance = self.get_instance(ctx.message.channel.server.id)
        logger_instance = bot_instance.modules_instances["Logger"]
        logger_instance.log_channel = ctx.message.channel.id
        bot_instance.update()
        await self.bot.say(
            self.personality_data[bot_instance.current_personality]["log_here"].format(ctx.message.channel.id))

    async def on_message(self, message):
        bot_instance = self.get_instance(message.channel.server.id)
        logger_instance = bot_instance.modules_instances["Logger"]

        if logger_instance.log_channel is not None and (message.channel.id != logger_instance.log_channel):
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            message_content = message.content
            message_content = message_content.replace("`", "'").replace("\n", "\n+ ")

            await self.bot.send_message(log_channel,
                                        "{}, #{}:```diff\n+ {}```".format(
                                            message.author.name,
                                            message.channel.name,
                                            message_content
                                        ))

    async def on_message_delete(self, message):
        bot_instance = self.get_instance(message.channel.server.id)
        logger_instance = bot_instance.modules_instances["Logger"]

        if logger_instance.log_channel is not None and message.channel.id != logger_instance.log_channel:
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            message_content = message.content
            message_content = message_content.replace("`", "'").replace("\n", "\n- ")

            await self.bot.send_message(log_channel,
                                        "{}, #{}:```diff\n- {}```".format(
                                            message.author.name,
                                            message.channel.name,
                                            message_content
                                        ))

    async def on_message_edit(self, before, after):
        bot_instance = self.get_instance(before.channel.server.id)
        logger_instance = bot_instance.modules_instances["Logger"]

        if logger_instance.log_channel is not None and before.channel.id != logger_instance.log_channel:
            log_channel = self.bot.get_channel(logger_instance.log_channel)

            before_content = before.content
            before_content = before_content.replace("`", "'").replace("\n", "\n- ")
            after_content = after.content
            after_content = after_content.replace("`", "'").replace("\n", "\n+ ")

            await self.bot.send_message(log_channel,
                                        "{}, #{}:```diff\n- {}\n+ {}```".format(
                                            before.author.name,
                                            before.channel.name,
                                            before_content,
                                            after_content
                                        ))


class LoggerInstance:  # hold the properties that this module needs
    def __init__(self, bot_instance, entry=None, config=None):
        self.bot_instance = bot_instance
        self.log_channel = None
        if "log_channel" in entry:
            self.log_channel = entry["log_channel"]
        elif config is None:
            self.log_channel = config["log_channel"]
        else:
            pass
            # it doesn't need any configuration

    def get_attributes(self):  # converts class' attributes to a dict, so the database can be updated
        return {"log_channel": self.log_channel}
