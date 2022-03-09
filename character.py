class Character:
    def __init__(self):
        self.attributes = {"Class & Level": "", "Name": "", "Background": "",
                    "Race": "", "Alignment": "", "Experience Points": ""}
        self.skill_points = {"Strength": 0, "Dexterity": 0, "Constitution": 0,
                        "Intelligence": 0, "Wisdom": 0, "Charisma": 0}
        self.dm_optionals = {"Passive Wisdom (Perception)": 0, 
                        "Inspiration": 0, "Proficiency Bonus": 0}
        self.health_and_armor = {"Armor Class": "", "Initiative": 0, "Speed": 0,
                            "Max HP": 0, "Current HP": 0, "Temporary HP": 0,
                            "Hit Dice": 0, "Death Save Successes": 0, "Death Save Fails": 0}
        self.saving_throws = {"Strength (Save)": 0, "Dexterity (Save)": 0, "Constitution (Save)": 0,
                         "Intelligence (Save)": 0, "Wisdom (Save)": 0, "Charisma (Save)": 0}
        self.character_skills = {"Acrobatics": 0, "Animal Handling": 0, "Arcana": 0,
                            "Athletics": 0, "Deception": 0, "History": 0, "Insight": 0,
                            "Intimidation": 0, "Investigation": 0, "Medicine": 0,
                            "Nature": 0, "Perception": 0, "Performance": 0, "Persuasion": 0,
                            "Religion": 0, "Slight of Hand": 0, "Stealth": 0, "Survival": 0}

    def get_attributes(self):
        return self.attributes

    def get_skill_points(self):
        return self.skill_points

    def get_dm_optionals(self):
        return self.dm_optionals

    def get_health_and_armor(self):
        return self.health_and_armor

    def get_saving_throws(self):
        return self.saving_throws

    def get_character_skills(self):
        return self.character_skills

    def get_data(self, indices):
        data = []

        if 0 in indices:
            data.append(self.attributes)
        if 1 in indices:
            data.append(self.skill_points)
        if 2 in indices:
            data.append(self.dm_optionals)
        if 3 in indices:
            data.append(self.health_and_armor)
        if 4 in indices:
            data.append(self.saving_throws)
        if 5 in indices:
            data.append(self.character_skills)

        return data

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_skill_points(self, skill_points):
        self.skill_points = skill_points

    def set_dm_optionals(self, dm_optionals):
        self.dm_optionals = dm_optionals

    def set_health_and_armor(self, health_and_armor):
        self.health_and_armor = health_and_armor

    def set_saving_throws(self, saving_throws):
        self.saving_throws = saving_throws

    def set_character_skills(self, character_skills):
        self.character_skills = character_skills
