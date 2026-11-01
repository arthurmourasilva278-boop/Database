import datetime
import discord

class CExEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(color=kwargs.pop("color", 0xD4AF37), **kwargs)
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)
        self.set_footer(text=f"CEx System • {self.timestamp.strftime('%d/%m/%Y %H:%M')}")
