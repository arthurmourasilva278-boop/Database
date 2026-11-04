import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from config.settings import DISCORD_TOKEN

# Inicializa o Flask para manter o bot ativo no Render (health-check)
app = Flask('')

@app.route('/')
def home():
    return "CEx System Online e Operacional!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Configuração dos Intents do Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot CEx System iniciado com sucesso como {bot.user}")

# Carrega automaticamente todos os módulos da pasta cogs/
if os.path.exists('./cogs'):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"📦 Módulo carregado: {filename[:-3]}")
            except Exception as e:
                print(f"❌ Erro ao carregar o módulo {filename[:-3]}: {e}")

if __name__ == "__main__":
    # Inicia o servidor Flask em uma thread separada
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Inicia o bot do Discord
    bot.run(DISCORD_TOKEN)
