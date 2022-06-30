import discord
from discord.ext import commands, tasks

from datetime import datetime, timezone
import time


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.timer_length = 0
        self.timer_start = 0
        self.channel_id = 0

    @commands.command(aliases=["rb", "ph"])
    async def rulebook(self, ctx):
        await ctx.send("The player's handbook can be seen online at http://online.anyflip.com/dkneq/yerq/mobile/index.html#p=1")

    @commands.command(aliases=["time"])
    async def clock(self, ctx):
        current_time = datetime.now(timezone.utc).strftime("%H:%M:%S")
        await ctx.send(f"The time in UTC is: {current_time}")

    @commands.command()
    async def timer(self, ctx, seconds):
        self.timer_start = time.monotonic()
        self.timer_length = int(seconds)
        self.channel = self.bot.get_channel(ctx.channel.id)
        await ctx.send(f"Now starting a timer for {seconds} seconds.")
        self.timerLoop.start()

    @tasks.loop()
    async def timerLoop(self):
        current_seconds = time.monotonic()
        if current_seconds - self.timer_start >= self.timer_length:
            await self.channel.send("Timer is up!")
            self.timerLoop.cancel()


    
def setup(bot):
    bot.add_cog(General(bot))