import discord
from discord import app_commands
from discord.ext import commands

import dataProcessor

class CharacterStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.types_of_data = ["General Attributes", "Skill Points", "Dungeon Master Optional Points", 
                             "Defensive Attributes", "Saving Throws", "Character Skills"]
        self.processor = dataProcessor.Processor()


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
    async def showcharstats(self, ctx, name: str, *indices):
        # Character was not found with the given name
        if not self.processor.character_exists(name):
            await ctx.send(f"No character was found with the name \"{name}\"")
            return

        character = self.processor.get_character(name)

        # Grab all valid data indices
        data_indices = []
        if len(indices) > 0:
            for index in indices:
                data_index = int(index)
                if data_index > len(self.types_of_data) or 0 > data_index:
                    await ctx.send(f"Invalid index found: {data_index}")
                    return
                data_indices.append(data_index)

        # Grab all data if no index argument is given
        else:
            data_indices = [index for index in range(len(self.types_of_data))]
        
        # Create embeds for each type of data
        await ctx.send(f"Data for \"{name}\"")

        # Sort indices and create the embed
        data_indices.sort()
        character_data = character.get_data(data_indices)
        for index in range(len(data_indices)):
            embed = discord.Embed(title=self.types_of_data[data_indices[index]])

            for key in character_data[index]:
                embed.add_field(name=key, value=character_data[index][key])

            await ctx.send(embed=embed)

    @commands.hybrid_command(brief="Claim a character",
                      description="Claim a character by name if it exists, making you its owner")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def claim(self, ctx, name: str):
        # Check that the character exists
        if self.processor.character_exists(name):
            character = self.processor.get_character(name)
            owner_id = character.get_owner()

            # If the character is already owned, warn the user
            if owner_id != 0:
                owner = await self.bot.fetch_user(owner_id)
                await ctx.send(f"\"{name}\" is already claimed by {owner}!")

            # If the character has no owner, claim it
            else:
                character.set_owner(ctx.author.id)
                await ctx.send(f"You now own \"{name}\"!")
                self.processor.save_data()

    @commands.hybrid_command(brief="Unclaim a character",
                      description="Unclaim a character that you own, setting its owner to no one")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def unclaim(self, ctx, name: str):
        # Check if the character exists
        if self.processor.character_exists(name):
            character = self.processor.get_character(name)
            owner_id = character.get_owner()

            # If the user requesting the unclaim is not the owner, warn them
            if owner_id != ctx.author.id:
                await ctx.send(f"\"{name}\" is not claimed by you!")

            # Otherwise, remove the user as the owner
            else:
                character.remove_owner()
                await ctx.send(f"You now no longer own \"{name}\"!")
                self.processor.save_data()

    @commands.hybrid_command(brief="Check your characters",
                      description="Retrieve a list of characters that you own, if any")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def checkchars(self, ctx: str):
        characters = self.processor.get_characters_by_id(ctx.author.id)
        if len(characters) > 0:
            for char in characters:
                await ctx.send(repr(char))
        else:
            await ctx.send("You don't own anyone.")        

    @commands.hybrid_command(brief="Alter stats of a character")
    @app_commands.guilds(discord.Object(id=824092658574032907))
    async def changecharhp(self, ctx, owner: int, name: str, damage: int):
        # Check for non positive damage
        if damage == 0:
            await ctx.send(f"Damage cannot be less or equal than zero!")
            return

        # Verify owner has characters
        characters = self.processor.get_characters_by_id(int(owner[3:-1]))
        if len(characters) == 0:
            await ctx.send(f"{owner} does not have a character!")
            return
            
        messages = []
        # Verify character exists
        found = False
        for character in characters:
            # Change health accordingly
            if character.get_attributes()["Name"] == name:
                found = True
                charPoints = character.get_health_and_armor()
                
                # Get health points
                overshield = int(charPoints["Temporary HP"])
                health = int(charPoints["Current HP"])
                remaining_damage = damage

                # Shield hit
                if overshield > 0:
                    overshield, remaining_damage = min(damage, overshield), min(damage, overshield)
                    messages.append(f"The overshield took {damage} points of damage and now has {overshield} points left.")

                # Health hit
                if remaining_damage > 0:
                    health, remaining_damage = min(remaining_damage, health), min(remaining_damage, health)
                    messages.append(f"{name} took {remaining_damage} points of damage and now has {health} points left.")

                # Update the character
                
                
                output_message = "\n".join(messages)
                await ctx.send(output_message)

        if not found:
            await ctx.send(f"{name} could not be found! Are you sure {owner} owns this character?")
 
async def setup(bot):
    await bot.add_cog(CharacterStats(bot))
