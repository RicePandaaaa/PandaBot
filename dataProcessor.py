import csv

class FileEditor():
    def load_data(self, name):
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
        with open("./cogs/characterList.csv") as csvfile:
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