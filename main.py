import discord
from discord.ext import commands
import csv

bot = commands.Bot(command_prefix="!")


"""
Just a cute message to let me know the bot is on
"""
@bot.event
async def on_ready():
    channel = bot.get_channel()

    await channel.send("Hey Tony, I'm all ready to go! o7")


"""
Loads a character from the characterList.csv file given a name from the user
"""
@bot.command()
async def showchar(ctx, name):
    character_data = load_data(name)

    if character_data is None:
        await ctx.send(f"No character was found with the name \"{name}\"")
    
    else:
        await ctx.send(f"Data for \"{name}\"")
        types_of_data = ["Attributes", "Skill Points"]

        for index in range(len(types_of_data)):
            embed = discord.Embed(title=types_of_data[index])

            for key in character_data[index]:
                embed.add_field(name=key, value=character_data[index][key])

            await ctx.send(embed=embed)


def load_data(name):
    attributes = {"Class & Level": "", "Name": "", "Background": "",
                  "Race": "", "Alignment": "", "Experience Points": ""}
    skill_points = {"Strength": 0, "Dexterity": 0, "Constitution": 0,
                    "Intelligence": 0, "Wisdom": 0, "Charisma": 0}

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

        if not name_found:
            return None;

    return attributes, skill_points


"""
If the user forgot to enter a name, catch the error and remind them
"""
@showchar.error
async def showchar_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Please add the character's name after the command!")
    else:
        await ctx.send("Unknown error caught.")
    


bot.run("")