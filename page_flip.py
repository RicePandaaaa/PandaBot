import discord

class PageFlip(discord.ui.View):
    def __init__(self, embed_title, category, items):
        super().__init__()
        self.value = None
        self.color = discord.Color.random()

        self.embed_title = embed_title
        self.category = category
        self.items = items
        self.index = 0
        self.PAGE_SIZE = 15

    @discord.ui.button(label="Prev")
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = max(0, self.index - self.PAGE_SIZE)
        end = min(len(self.items), self.index + self.PAGE_SIZE)

        embed = discord.Embed(color=self.color())
        embed.set_author(name=self.embed_title)
        embed.add_field(name=self.category, value="\n".join(self.items[self.index : end]))

        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Next")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = min(len(self.items)-1, self.index + self.PAGE_SIZE)
        end = min(len(self.items), self.index + self.PAGE_SIZE)

        embed = discord.Embed(color=self.color)
        embed.set_author(name=self.embed_title)
        embed.add_field(name=self.category, value="\n".join(self.items[self.index : end]))

        await interaction.response.edit_message(embed=embed)
