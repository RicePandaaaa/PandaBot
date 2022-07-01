import discord
from discord import app_commands
from random import randint
from discord.ext import commands

class DiceRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def roll(self, interaction: discord.Interaction, sides: int, modifier: int=0, numofrolls: int=1):
        rolls = []
        for _ in range(numofrolls):
            rolls.append(str(randint(1, sides) + modifier))

        results = ", ".join(rolls)
        await interaction.response.send_message(f"After adjusting for a modifier of {modifier}, you have rolled: {results}")

    @commands.hybrid_command()
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def coinflip(self, ctx, numofflips=1):
        if numofflips > 15:
            await ctx.send("You're only allowed a max of 15 flips at one time.")
        
        else:
            flip_results = []
            for _ in range(numofflips):
                flip_results.append("HEADS" if randint(1, 2) == 1 else "TAILS")

            flip_results_str = ", ".join(flip_results)
            await ctx.send(f"In order, the following coinflips resulted in: {flip_results_str}")



async def setup(bot):
    await bot.add_cog(DiceRoll(bot))