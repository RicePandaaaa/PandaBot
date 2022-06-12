from ast import alias
import discord
from discord.ext import commands

import dataProcessor

class CharacterStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.types_of_data = ["General Attributes", "Skill Points", "Dungeon Master Optional Points", 
                             "Defensive Attributes", "Saving Throws", "Character Skills"]
        self.processor = dataProcessor.Processor()

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
                4) Saving Throws
                5) Character Skills
                """, aliases=["stats", "scs"])
    async def showcharstats(self, ctx, name, *indices):
        # Character was not found with the given name
        if not self.processor.character_exists(name):
            await ctx.send(f"No character was found with the name \"{name}\"")
            return

        character = self.processor.get_character(name)

        data_indices = []
        if len(indices) > 0:
            for index in indices:
                data_index = int(index)
                if data_index > len(self.types_of_data) or 0 > data_index:
                    await ctx.send(f"Invalid index found: {data_index}")
                    return
                data_indices.append(data_index)

        else:
            data_indices = [index for index in range(len(self.types_of_data))]
        
        # Create embeds for each type of data
        await ctx.send(f"Data for \"{name}\"")

        data_indices.sort()
        character_data = character.get_data(data_indices)
        for index in range(len(data_indices)):
            embed = discord.Embed(title=self.types_of_data[data_indices[index]])

            for key in character_data[index]:
                embed.add_field(name=key, value=character_data[index][key])

            await ctx.send(embed=embed)

    @commands.command(brief="Claim a character")
    async def claim(self, ctx, name):
        if self.processor.character_exists(name):
            character = self.processor.get_character(name)
            owner_id = character.get_owner()

            if owner_id != 0:
                owner = await self.bot.fetch_user(owner_id)
                await ctx.send(f"\"{name}\" is already claimed by {owner}!")

            else:
                character.set_owner(ctx.author.id)
                await ctx.send(f"You now own \"{name}\"!")
                self.processor.save_data()

    @commands.command(brief="Unclaim a character")
    async def unclaim(self, ctx, name):
        if self.processor.character_exists(name):
            character = self.processor.get_character(name)
            owner_id = character.get_owner()

            if owner_id != ctx.author.id:
                await ctx.send(f"\"{name}\" is not claimed by you!")

            else:
                character.remove_owner()
                await ctx.send(f"You now no longer own \"{name}\"!")
                self.processor.save_data()

    @showcharstats.error
    @claim.error
    @unclaim.error
    async def error_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Please add the character's name after the command!")
        else:
            await ctx.send(error)           
    


def setup(bot):
    bot.add_cog(CharacterStats(bot))
