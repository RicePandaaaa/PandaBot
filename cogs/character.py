import discord
from discord.ext import commands
import csv
import dataProcessor

class Character(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.MAX_INDEX = 3
        self.file_editor = dataProcessor.FileEditor()

    """
    Loads a character from the characterList.csv file given a name from the user
    """
    @commands.command(brief="Shows all or some of the data for a character", 
                description="""
                Accepted arguments:
                - name: Case-sensitive name of your character
                - indices: List indices corresponding to specific data you want to look at

                Indices are to be separated by a space. Valid usage examples:
                !showchar Tony
                !showchar Tony 0
                !showchar Tony 0 1 2
                !showchar Tony 2 0 1

                Indices:
                0) General Attributes
                1) Skill Points
                2) Dungeon Master Optional Points
                3) Defensive Attributes
                """)
    async def showchar(self, ctx, name, *indices):
        character_data = self.file_editor.load_data(name)

        data_indices = []
        if len(indices) > 0:
            try:
                for index in indices:
                    data_index = int(index)
                    if data_index > self.MAX_INDEX:
                        raise Exception("Invalid argument", "Invalid indices given.")
                    data_indices.append(data_index)
            except:
                await ctx.send("Invalid indices given.")
                return


        # Character was not found with the given name
        if character_data is None:
            await ctx.send(f"No character was found with the name \"{name}\"")
        
        # Create embeds for each type of data
        else:
            await ctx.send(f"Data for \"{name}\"")
            types_of_data = ["General Attributes", "Skill Points", "Dungeon Master Optional Points", "Defensive Attributes"]

            for index in range(len(types_of_data)):
                if len(data_indices) == 0 or (len(data_indices) > 0 and index in data_indices):
                    embed = discord.Embed(title=types_of_data[index])

                    for key in character_data[index]:
                        embed.add_field(name=key, value=character_data[index][key])

                    await ctx.send(embed=embed)

    """
    If the user forgot to enter a name, catch the error and remind them
    """
    @showchar.error
    async def showchar_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Please add the character's name after the command!")
        else:
            await ctx.send("Unknown error caught.")
    


def setup(bot):
    bot.add_cog(Character(bot))