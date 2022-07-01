import character
import csv
import pandas as pd

class Processor():
    def __init__(self):
        self.characters = {}
        self.stats_names = ["Name", "Class & Level", "Background", "Race", "Alignment", "Experience Points",
                            "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma",
                            "Passive Wisdom (Perception)", "Inspiration", "Proficiency Bonus", "Armor Class",
                            "Initiative", "Speed", "Max HP", "Current HP", "Temporary HP", "Hit Dice",
                            "Death Save Successes", "Death Save Fails", "Strength (Save)", "Dexterity (Save)",
                            "Constitution (Save)", "Intelligence (Save)", "Wisdom (Save)", "Charisma (Save)",
                            "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History",
                            "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception",
                            "Performance", "Persuasion", "Religion", "Slight of Hand", "Stealth", "Survival",
                            "Owner"]
        self.load_data()

    def load_data(self):
        # Dictionaries to hold the data
        attributes = {"Name": "", "Class & Level": "", "Background": "",
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

        self.save_data()


    def save_data(self):
        with open("cogs/characterList.csv", "w", newline='') as file:
            csvWriter = csv.writer(file, delimiter=",")
            csvWriter.writerow(self.stats_names)

            # Write each character's data into a csv row
            for character_name in self.characters.keys():
                charData = self.get_character(character_name).get_all_data()
                dataRow = [list(l.values()) for l in charData]
                dataRow = [item for sublist in dataRow for item in sublist]

                csvWriter.writerow(dataRow)

    def character_exists(self, name):
        return name in self.characters.keys()

    def get_character(self, name):
        return self.characters[name]

    def get_characters_by_id(self, id):
        if id in self.characters:
            return self.characters[id]

        return None