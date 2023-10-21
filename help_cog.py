import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.help_message = """ 
```
Let the whole world know my name.

General Commands:
/help - Helps.
/p <keywords> - Scours the dark depths of Youtube and adds the video it finds to the queue.
/q - Display queue.
/skip - King Crimson.
/clear - Clears.
/leave - Leaves.
/pause - Pauses (and resumes).
/resume - Resumes.
```
"""
        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)
        
        await self.send_to_all(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

    @commands.command(name="help", help="Helps you in your daily affairs.")
    async def help(self,ctx):
        await ctx.send(self.help_message)

async def setup(bot):
    await bot.add_cog(help_cog(bot)) 