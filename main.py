import discord
from discord.ext import commands
import os
from help_cog import help_cog
from music_cog import music_cog


intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', help_command=None, intents=intents)

TOKEN = ""

@bot.event
async def on_ready():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))

bot.run(TOKEN)
