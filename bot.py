
import os
import datetime
import discord
from discord.ext import commands

class CExEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(color=0xD4AF37, **kwargs)
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)
        self.set_footer(text=f"CEx System • {self.timestamp.strftime('%d/%m/%Y %H:%M')}")

class CExBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        extensions = [
            "cogs.admin",
            "cogs.registry",
            "cogs.sales",
            "cogs.wallet"
        ]
        
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f"Extension {ext} loaded successfully.")
            except Exception as e:
                print(f"Erro ao carregar {ext}: {e}")
                
        await self.tree.sync()

    async def on_ready(self):
        print(f"Bot online como {self.user} (ID: {self.user.id})")

if __name__ == "__main__":
    bot = CExBot()
    bot.run(os.getenv("DISCORD_TOKEN"))
