import discord
from discord.ext import commands
import csv

bot = commands.Bot(command_prefix="!")

# Constants
MAX_INDEX = 3

"""
Just a cute message to let me know the bot is on
"""
@bot.event
async def on_ready():
    channel = bot.get_channel(READY_CHANNEL_ID)

    await channel.send("Hey Tony, I'm all ready to go! o7")


"""
Loads a character from the characterList.csv file given a name from the user
"""
@bot.command(brief="Shows all or some of the data for a character", 
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
async def showchar(ctx, name, *indices):
    character_data = load_data(name)

    data_indices = []
    if len(indices) > 0:
        try:
            for index in indices:
                data_index = int(index)
                if data_index > MAX_INDEX:
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


def load_data(name):
    # Dictionaries to hold the data
    attributes = {"Class & Level": "", "Name": "", "Background": "",
                  "Race": "", "Alignment": "", "Experience Points": ""}
    skill_points = {"Strength": 0, "Dexterity": 0, "Constitution": 0,
                    "Intelligence": 0, "Wisdom": 0, "Charisma": 0}
    dm_optionals = {"Inspiration": 0, "Proficiency Bonus": 0}
    health_and_armor = {"Armor Class": "", "Initiative": 0, "Speed": 0,
                        "Max HP": 0, "Current HP": 0, "Temporary HP": 0,
                        "Hit Dice": 0, "Death Save Successes": 0, "Death Save Fails": 0}

    # Validate name exists and if so, update the dictionaries
    name_found = False;
    with open("characterList.csv") as csvfile:
        reader = csv.DictReader(csvfile)

        name_found = False
        for row in reader:
            if (row["Name"] == name):
                name_found = True
                for attribute in attributes:
                    attributes[attribute] = row[attribute]

                for skill in skill_points:
                    skill_points[skill] = row[skill]

                for optional in dm_optionals:
                    dm_optionals[optional] = row[optional]

                for attribute in health_and_armor:
                    health_and_armor[attribute] = row[attribute]

        if not name_found:
            return None;

    return attributes, skill_points, dm_optionals, health_and_armor


"""
If the user forgot to enter a name, catch the error and remind them
"""
@showchar.error
async def showchar_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Please add the character's name after the command!")
    else:
        await ctx.send("Unknown error caught.")
    


bot.run(TOKEN)