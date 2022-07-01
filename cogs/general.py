import discord, typing
from discord.ext import commands, tasks
from discord.ext.commands import Context, Greedy
from discord import app_commands
from datetime import datetime, timezone
import time


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.timer_length = 0
        self.timer_start = 0
        self.channel_id = 0

    @commands.hybrid_command(aliases=["rb", "ph"])
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def rulebook(self, ctx):
        await ctx.send("The player's handbook can be seen online at http://online.anyflip.com/dkneq/yerq/mobile/index.html#p=1")

    @commands.hybrid_command(brief="Get the current time", description="Get the current time in UTC", aliases=["time"])
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def clock(self, ctx):
        current_time = datetime.now(timezone.utc).strftime("%H:%M:%S")
        await ctx.send(f"The time in UTC is: {current_time}")

    @commands.hybrid_command(brief="Set a timer", description="Set a timer with a maximum of 3600 seconds")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def timer(self, ctx, seconds):
        # Set variables
        self.timer_start = time.monotonic()
        self.timer_length = int(seconds)
        self.channel = self.bot.get_channel(ctx.channel.id)
        await ctx.send(f"Now starting a timer for {seconds} seconds.")

        # Start the timer
        self.timerLoop.start()

    @commands.command()
    @commands.guild_only()
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException as error:
                print(error)
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @tasks.loop()
    async def timerLoop(self):
        current_seconds = time.monotonic()
        # Check if the elapsed time has been at least met
        if current_seconds - self.timer_start >= self.timer_length:
            await self.channel.send("Timer is up!")
            self.timerLoop.cancel()


    
async def setup(bot):
    await bot.add_cog(General(bot))