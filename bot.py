import os
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask
from supabase import create_client, Client

# 1. Inicializa o servidor web Flask para satisfazer o requisito de portas da Render
app = Flask("")

@app.route("/")
def home():
    return "Bot online, integrado com Supabase e ativo!"

def run_flask():
    # A Render atribui dinamicamente a porta através da variável de ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# 2. Configuração da ligação ao Supabase utilizando a variável de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("Aviso: Variáveis do Supabase não encontradas nas variáveis de ambiente.")

# 3. Configuração do Bot de Discord
intents = discord.Intents.default()
intents.message_content = True  # Ativa intents essenciais para leitura de mensagens

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

# Exemplo de comando simples integrado com o Supabase (opcional)
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! O bot está ativo e operacional na Render.")

if __name__ == "__main__":
    # Inicia o servidor Flask em segundo plano para manter o Web Service ativo
    keep_alive()

    # Inicia o bot do Discord utilizando o token seguro
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("Erro crítico: A variável de ambiente DISCORD_TOKEN não foi configurada.")
