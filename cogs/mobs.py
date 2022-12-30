import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

import page_flip

class Mobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Connect to the databse
        self.db_file = "Mon.db"
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()

        # List of keys for ease of accessibility
        self.data_keys = ["Name", "Size", "Type", "Alignment", "AC", "HP", "Speeds", "STR", "DEX", "CON", "INT", "WIS",
                         "CHA", "Saving Throws", "Skills", "WRI", "Senses", "Languages", "CR", "Additional", "Font", "Additional Info", "Author"]

    @commands.hybrid_command(brief="Mob information",
                      description="Get information on a specific mob")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def mobinfo(self, ctx: commands.Context, name: str):
        results = self.cur.execute(f"SELECT * from monsters WHERE Name = \"{name}\" COLLATE NOCASE")
        data_values = results.fetchall()

        if len(data_values) == 0:
            await ctx.send(f"{name} does not exist in my database.")

        else:
            data_values = data_values[0]

            # Make three embeds
            embedOne = discord.Embed(title=f"Data for {data_values[0]}")
            for i in range(1, 15):
                embedOne.add_field(name=self.data_keys[i], value=data_values[i])

            embedTwo = discord.Embed(title=f"Even more data for {data_values[0]}")
            for i in range(15, 23):
                if self.data_keys[i] != "Additional Info":
                    embedTwo.add_field(name=self.data_keys[i], value=data_values[i])

            await ctx.send(embed=embedOne)
            await ctx.send(embed=embedTwo)
    
    @commands.hybrid_command(brief="Get mobs after filter",
                      description="Get names of all mobs whose stats match the given filters")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def filtermobs(self, ctx: commands.Context, *, args):
        # Split up the arguments
        args = [x for x in args.split(" ") if x != ""]
        print(args)

        # Need a non zero, even amount of strings
        if len(args) % 2 != 0 or len(args) == 0:
            await ctx.send("Missing filter data. Please try again.")
        # Can't be more than the maximum amount of fields though
        elif len(args) > len(self.data_keys) * 2:
            await ctx.send("Too many filters asked for. Please try again.")
        else:
            command = "SELECT * FROM monsters WHERE "
            
            # Put everything into a dictionary
            filters = {}
            for index in range(0, len(args)-1, 2):
                filters[args[index]] = args[index+1]

            filter_fields = list(filters.keys())
            # Check if the given fields are valid
            command_filters = []
            for filter_field in filter_fields:
                found = False
                for data_field in self.data_keys:
                    if filter_field.lower() == data_field.lower():
                        found = True

                if not found:
                    await ctx.send(f"{filter_field} is not a valid field.")
                    return

                field_value = filters[filter_field]
                if not field_value.isnumeric():
                    field_value = f'"{field_value}"'
                command_filters.append(f"{filter_field}={field_value}")

            # Create the full command
            command += " AND ".join(command_filters) + " COLLATE NOCASE"

            # Execute the command
            results = self.cur.execute(command)
            data_values = results.fetchall()
            
            # Create the embed
            items = [monster[0] for monster in data_values]
            page_flip_view = page_flip.PageFlip("Results after Filtering", "Names", items)
            
            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(name="Results after Filtering")
            embed.add_field(name="Names", value="\n".join(items[0 : min(15, len(items))]))

            await ctx.send(embed=embed, view=page_flip_view)


    @commands.hybrid_command(brief="Get attributes",
                      description="Get all attributes a mob can have")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def getattributes(self, ctx: commands.Context):
        await ctx.send(", ".join(self.data_keys))


async def setup(bot):
    await bot.add_cog(Mobs(bot))
