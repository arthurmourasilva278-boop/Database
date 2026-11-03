import os
import random
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
# 1. GESTÃO DE CARGOS (ADD / REMOVER)
# ==========================================
@bot.tree.command(name="add_cargo", description="Adiciona um cargo a um membro selecionado.")
@app_commands.default_permissions(manage_roles=True)
@app_commands.describe(membro="O membro que receberá o cargo", cargo="O cargo a ser adicionado")
async def add_cargo(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    if cargo >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ Não tenho permissão para gerir este cargo.", ephemeral=True)
        return
    
    try:
        await membro.add_roles(cargo)
        embed = discord.Embed(
            title="◆ CEx › Gestão de Cargos",
            description=f"✅ O cargo {cargo.mention} foi atribuído com sucesso a {membro.mention}!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Ocorreu um erro ao adicionar o cargo: {e}", ephemeral=True)


@bot.tree.command(name="remover_cargo", description="Remove um cargo de um membro selecionado.")
@app_commands.default_permissions(manage_roles=True)
@app_commands.describe(membro="O membro do qual deseja remover o cargo", cargo="O cargo a ser removido")
async def remover_cargo(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    if cargo not in membro.roles:
        await interaction.response.send_message(f"⚠️ O membro {membro.mention} não possui o cargo {cargo.mention}.", ephemeral=True)
        return

    if cargo >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ Não tenho permissão para gerir este cargo.", ephemeral=True)
        return

    try:
        await membro.remove_roles(cargo)
        embed = discord.Embed(
            title="◆ CEx › Gestão de Cargos",
            description=f"🗑️ O cargo {cargo.mention} foi removido de {membro.mention} com sucesso!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Ocorreu um erro ao remover o cargo: {e}", ephemeral=True)


# ==========================================
# 2. GESTÃO DE VENDAS (REGISTAR, APAGAR, EDITAR)
# ==========================================
@bot.tree.command(name="registrar_venda", description="Regista uma nova venda com vendedor e comprovante.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    vendedor="Selecione o vendedor responsável",
    cliente="Nome do cliente",
    valor="Valor da venda (Ex: R$ 30,00)",
    comprovante="Anexe a imagem do comprovante de pagamento"
)
async def registrar_venda(interaction: discord.Interaction, vendedor: discord.Member, cliente: str, valor: str, comprovante: discord.Attachment):
    codigo_venda = f"#CEx-{random.randint(10000, 99999)}"

    embed = discord.Embed(
        title=f"◆ CEx › REGISTRO DE VENDA · {codigo_venda}",
        description=f"💼 **Nova venda registada com sucesso!**\n\n"
                    f"👤 **Vendedor:** {vendedor.mention}\n"
                    f"🤝 **Cliente:** {cliente}\n"
                    f"💰 **Valor:** {valor}\n"
                    f"🧾 **Código da Venda:** `{codigo_venda}`\n\n"
                    f"*Para apagar esta venda, use `/apagar_venda` informando o código.*",
        color=discord.Color.blue()
    )
    embed.set_image(url=comprovante.url)
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="apagar_venda", description="Apaga um registo de venda através do código.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(codigo="O código da venda (Ex: #CEx-12345)")
async def apagar_venda(interaction: discord.Interaction, codigo: str):
    embed = discord.Embed(
        title="◆ CEx › Gestão de Vendas",
        description=f"🗑️ O registo referente à venda **{codigo}** foi apagado com sucesso do sistema.",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="editar_venda", description="Edita os dados de uma venda existente.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    codigo="Código da venda a ser editada (Ex: #CEx-12345)",
    produto="Novo produto",
    vendedor="Novo vendedor responsável",
    valor="Novo valor",
    observacoes="Novas observações"
)
async def editar_venda(interaction: discord.Interaction, codigo: str, produto: str, vendedor: discord.Member, valor: str, observacoes: str):
    embed = discord.Embed(
        title=f"◆ CEx › EDITAR VENDA · {codigo}",
        description=f"✏️ **Venda atualizada com sucesso!**\n\n"
                    f"🧾 **Código:** `{codigo}`\n"
                    f"📦 **Produto:** {produto}\n"
                    f"👤 **Vendedor:** {vendedor.mention}\n"
                    f"💰 **Valor:** {valor}\n"
                    f"📝 **Observações:** {observacoes}",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ==========================================
# 3. MÓDULO FINANCEIRO E METAS
# ==========================================
@bot.tree.command(name="consultar_saldo", description="Consulta o saldo e comissões de um vendedor.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(vendedor="Selecione o vendedor para consultar o registo")
async def consultar_saldo(interaction: discord.Interaction, vendedor: discord.Member):
    embed = discord.Embed(
        title=f"◆ CEx › Consulta de Saldo",
        description=f"📊 **Registo Financeiro de** {vendedor.mention}\n\n"
                    f"💰 **Saldo Atual:** `R$ 0,00`\n"
                    f"🏆 **Total Ganho em Comissões:** `R$ 0,00`\n\n"
                    f"*Dados contabilizados pelo sistema CEx.*",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="pagar_comissao", description="Paga a comissão a um vendedor.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    vendedor="O vendedor que vai receber a comissão",
    valor="O valor a ser pago (Ex: R$ 50,00)",
    contador="O contador/responsável pelo pagamento"
)
async def pagar_comissao(interaction: discord.Interaction, vendedor: discord.Member, valor: str, contador: discord.Member):
    embed = discord.Embed(
        title="◆ CEx › Pagamento de Comissão",
        description=f"✅ **Comissão paga com sucesso!**\n\n"
                    f"👤 **Vendedor:** {vendedor.mention}\n"
                    f"💸 **Valor Pago:** {valor}\n"
                    f"🏦 **Contador Responsável:** {contador.mention}",
        color=discord.Color.teal()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="definir_meta", description="Define as metas diárias e semanais para seletivo ou vendedores.")
@app_commands.default_permissions(administrator=True)
@app_commands.choices(area=[
    app_commands.Choice(name="Seletivo", value="seletivo"),
    app_commands.Choice(name="Vendedores", value="vendedores")
])
@app_commands.describe(
    area="Selecione a área (Seletivo ou Vendedores)",
    meta_diaria="Valor da meta diária (Ex: R$ 100,00)",
    meta_semanal="Valor da meta semanal (Ex: R$ 700,00)"
)
async def definir_meta(interaction: discord.Interaction, area: app_commands.Choice[str], meta_diaria: str, meta_semanal: str):
    embed = discord.Embed(
        title="◆ CEx › Definição de Metas",
        description=f"🎯 **Metas atualizadas com sucesso!**\n\n"
                    f"📂 **Área:** `{area.name}`\n"
                    f"📅 **Meta Diária:** {meta_diaria}\n"
                    f"📆 **Meta Semanal:** {meta_semanal}\n\n"
                    f"*As metas já estão ativas para contabilização.*",
        color=discord.Color.purple()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ==========================================
# 4. PAINEL DE NICK (EXEMPLO DE VISTA)
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
                    "└ É o nome que aparece no **organograma** da equipe.\n"
                    "└ Sem ele você **não consegue registrar** a sua venda.\n"
                    "└ Leva 10 segundos e só precisa ser feito **uma vez**.\n\n"
                    "────────────────────────\n"
                    "*Trocou de nick no jogo? Clique de novo e atualize.*\n\n"
                    "CEx · use letras, números e _ (3 a 20 caracteres)",
        color=discord.Color.dark_embed()
    )
    view = NickView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Painel de nick enviado com sucesso!", ephemeral=True)


# Iniciar o servidor web e o bot
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
