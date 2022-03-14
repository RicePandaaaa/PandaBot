import character
import pandas as pd

class Processor():
    def __init__(self):
        self.characters = {}
        self.load_data()

    def load_data(self):
        # Dictionaries to hold the data
        attributes = {"Class & Level": "", "Name": "", "Background": "",
                    "Race": "", "Alignment": "", "Experience Points": ""}
        skill_points = {"Strength": 0, "Dexterity": 0, "Constitution": 0,
                        "Intelligence": 0, "Wisdom": 0, "Charisma": 0}
        dm_optionals = {"Passive Wisdom (Perception)": 0, 
                        "Inspiration": 0, "Proficiency Bonus": 0}
        health_and_armor = {"Armor Class": "", "Initiative": 0, "Speed": 0,
                            "Max HP": 0, "Current HP": 0, "Temporary HP": 0,
                            "Hit Dice": 0, "Death Save Successes": 0, "Death Save Fails": 0}
        saving_throws = {"Strength (Save)": 0, "Dexterity (Save)": 0, "Constitution (Save)": 0,
                         "Intelligence (Save)": 0, "Wisdom (Save)": 0, "Charisma (Save)": 0}
        character_skills = {"Acrobatics": 0, "Animal Handling": 0, "Arcana": 0,
                            "Athletics": 0, "Deception": 0, "History": 0, "Insight": 0,
                            "Intimidation": 0, "Investigation": 0, "Medicine": 0,
                            "Nature": 0, "Perception": 0, "Performance": 0, "Persuasion": 0,
                            "Religion": 0, "Slight of Hand": 0, "Stealth": 0, "Survival": 0}

        # Create the character object for each character in the file
        df = pd.read_csv("cogs/characterList.csv")

        for index in df.index:
            dnd_character = character.Character()

            for attribute in attributes:
                attributes[attribute] = df.loc[index, attribute]

            for skill in skill_points:
                skill_points[skill] = df.loc[index, skill]

            for optional in dm_optionals:
                dm_optionals[optional] = df.loc[index, optional]

            for attribute in health_and_armor:
                health_and_armor[attribute] = df.loc[index, attribute]

            for throw in saving_throws:
                saving_throws[throw] = df.loc[index, throw]

            for character_skill in character_skills:
                character_skills[character_skill] = df.loc[index, character_skill]

            owner = df.loc[index, "Owner"]

            # Update the character from default values
            dnd_character.set_attributes(attributes)
            dnd_character.set_skill_points(skill_points)
            dnd_character.set_dm_optionals(dm_optionals)
            dnd_character.set_health_and_armor(health_and_armor)
            dnd_character.set_saving_throws(saving_throws)
            dnd_character.set_character_skills(character_skills)
            dnd_character.set_owner(owner)

            self.characters[attributes["Name"]] = dnd_character

        # Change the dictionary into a DataFrame
        self.characters = pd.DataFrame([self.characters])

        print(self.characters)

    def character_exists(self, name):
        return name in self.characters.columns

    def get_character(self, name):
        return self.characters.loc[0, name]