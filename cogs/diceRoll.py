import discord
from random import randint
from discord.ext import commands

class DiceRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, sides, modifier=0, numOfRolls=1):
        rolls = []
        for i in range(numOfRolls):
            rolls.append(str(randint(1, int(sides)) + modifier))

        results = ", ".join(rolls)
        await ctx.send(f"After adjusting for a modifier of {modifier}, you have rolled: {results}")


def setup(bot):
    bot.add_cog(DiceRoll(bot))