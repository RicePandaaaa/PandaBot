import discord
from discord import app_commands
from random import randint
from discord.ext import commands

class Probability(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def roll(self, ctx: commands.Context, sides: int, modifier: int=0, numofrolls: int=1):
        if numofrolls > 100:
            await ctx.send("You can only do up to 100 dice rolls at one time.")

        else:
            rolls = []
            for _ in range(numofrolls):
                rolls.append(str(randint(1, sides) + modifier))

            results = ", ".join(rolls)
            await ctx.send(f"After adjusting for a modifier of {modifier}, you have rolled: {results}")

    @commands.hybrid_command()
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def coinflip(self, ctx: commands.Context, numofflips: int=1):
        if numofflips > 100:
            await ctx.send("You're only allowed a max of 100 flips at one time.")
        
        else:
            flip_results = []
            heads, tails = 0, 0
            for _ in range(numofflips):
                flip = randint(1, 2)

                if flip == 1:
                    flip_results.append("HEADS")
                    heads += 1
                else:
                    flip_results.append("TAILS")
                    tails += 1

            flip_results_str = ", ".join(flip_results)
            await ctx.send(f"HEADS came up {heads} times, and TAILS came up {tails} times.\nIn order, the following coinflips resulted in: {flip_results_str}")

    @commands.hybrid_command()
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def rng(self, ctx: commands.Context, min: int=1, max: int=20, numofnumbers: int=1):
        if numofnumbers > 100:
            await ctx.send("You're only allowed a max of 100 numbers generated at one time.")

        else:
            numbers = [str(randint(min, max)) for _ in range(numofnumbers)]
            num_results_str = ", ".join(numbers)
            await ctx.send(f"In order, the numbers generated are: {num_results_str}")


async def setup(bot):
    await bot.add_cog(Probability(bot))