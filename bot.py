import discord
from discord.ext import commands
import os
from config.settings import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot CEx System iniciado com sucesso como {bot.user}")

# Carrega automaticamente os cogs criados
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('__'):
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
