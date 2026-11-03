import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

# Configuração do Flask para manter o bot ativo na Render
app = Flask('')

@app.route('/')
def home():
    return "Bot de Vendas CEx está ativo e operacional na Render."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f'Comandos sincronizados: {len(synced)}')
    except Exception as e:
        print(e)

# Comando de Teste / Ping
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! O bot está ativo e operacional no servidor web.")

# ==========================================
# 1. MÓDULO DE REGISTRO DE NICK
# ==========================================
class NickModal(discord.ui.Modal, title="Registro de Nick Roblox"):
    nick_roblox = discord.ui.TextInput(
        label="Seu nick exato no Roblox",
        placeholder="Ex: seu_nick_aqui",
        min_length=3,
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="◆ CEx > Registro",
            description=f"✅ Nick **{self.nick_roblox.value}** cadastrado com sucesso!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class NickView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Cadastrar meu nick", style=discord.ButtonStyle.green, emoji="👤")
    async def cadastrar_nick(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NickModal())

@bot.tree.command(name="painel_nick", description="Envia o painel de registro de nick do Roblox.")
@app_commands.default_permissions(administrator=True)
async def painel_nick(interaction: discord.Interaction):
    embed = discord.Embed(
        title="◆ CEx > Registro",
        description="👤 **REGISTRO DE NICK ROBLOX**\n\n⭐ Cadastre aqui o seu **nick do Roblox**.\n\n"
                    "────────────────────────\n"
                    "└ É o nome que aparece no **organograma** da equipe[span_0](start_span)[span_0](end_span).\n"
                    "└ Sem ele você **não consegue registrar** a sua venda[span_1](start_span)[span_1](end_span).\n"
                    "└ Leva 10 segundos e só precisa ser feito **uma vez**[span_2](start_span)[span_2](end_span).\n\n"
                    "────────────────────────\n"
                    "*Trocou de nick no jogo? Clique de novo e atualize*[span_3](start_span)[span_3](end_span).\n\n"
                    "CEx · use letras, números e _ (3 a 20 caracteres)[span_4](start_span)[span_4](end_span)",
        color=discord.Color.dark_embed()
    )
    view = NickView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Painel de nick enviado com sucesso!", ephemeral=True)


# ==========================================
# 2. MÓDULO DE TABELA DE PREÇOS
# ==========================================
class PrecosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Calcular desconto", style=discord.ButtonStyle.primary, emoji="🧮")
    async def calcular_desconto(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🧮 Funcionalidade de cálculo de desconto acionada!", ephemeral=True)

@bot.tree.command(name="painel_precos", description="Envia a tabela oficial de preços.")
@app_commands.default_permissions(administrator=True)
async def painel_precos(interaction: discord.Interaction):
    embed = discord.Embed(
        title="◆ CEx › Tabela de preços",
        description="◆ **Dono de Divisão**\n\n"
                    "┗ BPE — **R$ 850** · mín R$ 700[span_5](start_span)[span_5](end_span)\n"
                    "┗ CIE — **R$ 850** · mín R$ 700[span_6](start_span)[span_6](end_span)\n"
                    "┗ BAC — **R$ 1.000** · mín R$ 850[span_7](start_span)[span_7](end_span)\n"
                    "┗ BFE — **R$ 1.000** · mín R$ 850[span_8](start_span)[span_8](end_span)\n"
                    "┗ Criar Divisão — **R$ 8.000** · preço único[span_9](start_span)[span_9](end_span)\n\n"
                    "────────────────────────\n"
                    "ℹ️ **mín** = o mínimo que você pode cobrar[span_10](start_span)[span_10](end_span)\n"
                    "5 produtos · preço oficial CEx · atualiza sozinha[span_11](start_span)[span_11](end_span)\n\n"
                    "Sistema CEx · tabela de preços",
        color=discord.Color.purple()
    )
    view = PrecosView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Tabela de preços enviada com sucesso!", ephemeral=True)


# ==========================================
# 3. MÓDULO DE AVAL
# ==========================================
class AvalModal(discord.ui.Modal, title="Solicitar Aval"):
    prazo = discord.ui.TextInput(label="Prazo (em dias)", placeholder="Ex: 15", max_length=3)
    motivo = discord.ui.TextInput(label="Motivo do afastamento", style=discord.TextStyle.paragraph, placeholder="Explique o motivo...")

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="◆ CEx › Aval",
            description=f"⏳ **Solicitação de Aval enviada!**\n\n"
                        f"👤 **Quem:** {interaction.user.mention}\n"
                        f"📅 **Prazo:** {self.prazo.value} dia(s)\n"
                        f"📝 **Motivo:** {self.motivo.value}\n\n"
                        f"*Aguardando aprovação da administração.*",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class AvalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Pedir aval", style=discord.ButtonStyle.primary, emoji="📥")
    async def pedir_aval(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AvalModal())

    @discord.ui.button(label="Voltei", style=discord.ButtonStyle.green, emoji="✅")
    async def voltei(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Seu aval foi encerrado com sucesso. Bem-vindo de volta!", ephemeral=True)

@bot.tree.command(name="painel_aval", description="Envia o painel de solicitação de aval.")
@app_commands.default_permissions(administrator=True)
async def painel_aval(interaction: discord.Interaction):
    embed = discord.Embed(
        title="◆ CEx › Aval",
        description="⏳ **SOLICITAR AVAL**\n\n"
                    "Vai ficar um tempo sem conseguir vender? Peça seu aval aqui[span_12](start_span)[span_12](end_span).\n\n"
                    "────────────────────────\n"
                    "└ Enquanto o aval estiver ativo **você não é cobrado** pela meta[span_13](start_span)[span_13](end_span).\n"
                    "└ As semanas de aval **não contam** como falha[span_14](start_span)[span_14](end_span).\n"
                    "└ Um administrador precisa **aprovar** o pedido[span_15](start_span)[span_15](end_span).\n\n"
                    "────────────────────────\n"
                    "**Voltou antes do prazo?** Use o botão **Voltei** — não precisa pedir a ninguém[span_16](start_span)[span_16](end_span).\n\n"
                    "CEx · até 30 dias por pedido[span_17](start_span)[span_17](end_span)",
        color=discord.Color.dark_embed()
    )
    view = AvalView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Painel de aval enviado com sucesso!", ephemeral=True)


# ==========================================
# 4. MÓDULO DE VENDAS E ENTREGAS
# ==========================================
class EntregaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Adicionando o botão de link de forma programática para evitar incompatibilidades de versão no decorador
        self.add_item(discord.ui.Button(label="Ver venda", style=discord.ButtonStyle.link, url="https://discord.com", emoji="🔗"))

    @discord.ui.button(label="Eu entrego", style=discord.ButtonStyle.green, emoji="📦")
    async def eu_entrego(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"📦 {interaction.user.mention} assumiu a entrega deste pedido!", ephemeral=False)

@bot.tree.command(name="simular_venda", description="Simula um pedido de venda pendente de entrega.")
@app_commands.default_permissions(administrator=True)
async def simular_venda(interaction: discord.Interaction):
    embed = discord.Embed(
        title="◆ CEx › PEDIDO DE ENTREGA · #CEx-X5WPHQ",
        description="⚠️ **Aguardando entrega · ninguém assumiu ainda**[span_18](start_span)[span_18](end_span)\n\n"
                    "`@Venda Patente` · pedido aberto há 2 dias[span_19](start_span)[span_19](end_span)\n"
                    "────────────────────────\n"
                    "📦 **Produto** · Patente · Elite Secreta [ES] · Patente Elite[span_20](start_span)[span_20](end_span)\n"
                    "🤝 **Entregar para** · Souza[span_21](start_span)[span_21](end_span)\n"
                    "👤 **Vendedor** · `@SOUZA` · Roblox CEARENSE_BRO[span_22](start_span)[span_22](end_span)\n"
                    "💰 **Valor** · R$ 30,00[span_23](start_span)[span_23](end_span)\n"
                    "🧾 **Venda** · #CEx-X5WPHQ · registrada há 2 dias[span_24](start_span)[span_24](end_span)\n\n"
                    "────────────────────────\n"
                    "└ Vai entregar? Clique em **Eu entrego** — o pedido fecha no seu nome. Só quem tem o cargo consegue[span_25](start_span)[span_25](end_span).\n\n"
                    "CEx · entregas",
        color=discord.Color.gold()
    )
    view = EntregaView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Simulação de venda enviada!", ephemeral=True)


# Iniciar o servidor web e o bot
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
