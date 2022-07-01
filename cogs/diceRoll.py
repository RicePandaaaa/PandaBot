from discord import app_commands
from random import randint
from discord.ext import commands

class DiceRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, sides, modifier=0, numOfRolls=1):
        rolls = []
        for _ in range(numOfRolls):
            rolls.append(str(randint(1, int(sides)) + modifier))

        results = ", ".join(rolls)
        await ctx.send(f"After adjusting for a modifier of {modifier}, you have rolled: {results}")

    @commands.command()
    async def coinflip(self, ctx, numOfFlips=1):
        if numOfFlips > 15:
            await ctx.send("You're only allowed a max of 15 flips at one time.")
        
        else:
            flip_results = []
            for _ in range(numOfFlips):
                flip_results.append("HEADS" if randint(1, 2) == 1 else "TAILS")

            flip_results_str = ", ".join(flip_results)
            await ctx.send(f"In order, the following coinflips resulted in: {flip_results_str}")



async def setup(bot):
    await bot.add_cog(DiceRoll(bot))