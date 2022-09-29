import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

import sqlite3

class Mobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Connect to the databse
        self.db_file = "Mon.db"
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()

    @commands.hybrid_command(brief="Mob information",
                      description="Get information on a specific mob")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def mobinfo(self, ctx, name):
        results = self.cur.execute(f"SELECT * from monsters WHERE Name = \"{name}\" COLLATE NOCASE")
        data_values = results.fetchall()

        if len(data_values) == 0:
            await ctx.send(f"{name} does not exist in my database.")

        else:
            data_keys = ["Name", "Size", "Type", "Alignment", "AC", "HP", "Speeds", "STR", "DEX", "CON", "INT", "WIS",
                         "CHA", "Saving Throws", "Skills", "WRI", "Senses", "Languages", "CR", "Additional", "Font", "Additional Info", "Author"]
            data_values = data_values[0]

            # Make three embeds
            embedOne = discord.Embed(title=f"Data for {data_values[0]}")
            for i in range(1, 15):
                embedOne.add_field(name=data_keys[i], value=data_values[i])

            embedTwo = discord.Embed(title=f"Even more data for {data_values[0]}")
            for i in range(15, 23):
                if data_keys[i] != "Additional Info":
                    embedTwo.add_field(name=data_keys[i], value=data_values[i])

            await ctx.send(embed=embedOne)
            await ctx.send(embed=embedTwo)


async def setup(bot):
    await bot.add_cog(Mobs(bot))
