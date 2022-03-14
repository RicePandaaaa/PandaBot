import os
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

"""
Just a cute message to let me know the bot is on
"""
@bot.event
async def on_ready():
    channel = bot.get_channel(READY_CHANNEL_ID)

    await channel.send("Hey Tony, I'm all ready to go! o7")

"""
Load the bot with cogs
"""
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(TOKEN)
