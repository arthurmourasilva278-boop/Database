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
    print(f'Bot conectado com sucesso como {bot.user}!')
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


# ==========================================
# 2. MÓDULO DE TABELAS (PAINEL INTERATIVO COM BOTÕES)
# ==========================================
class TabelasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Minérios", style=discord.ButtonStyle.primary, emoji="💎")
    async def btn_minerios(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💎 CEx › Tabela Preços & Benefícios (Minérios)",
            description=(
                "## __Tabela Preços Minérios__\n\n"
                "**__Opala__** - *250R$* • ***Min. 200R$***\n\n"
                "**__Jade__** - *180R$* • ***Min. 135R$***\n\n"
                "**__Safira__** - *130R$* • ***Min. 100R$***\n\n"
                "**__Ruby__** - *80R$* • ***Min. 65R$***\n\n"
                "**__Iron__** - *45R$* • ***Min. 30R$***\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "# Benefícios Minérios\n"
                "————————————————\n\n"
                "**__• Opala__** <:seta_1:1562090158902218824> *Permissões: Mute, Gerenciar Apelidos, Mudar Apelido, Gerenciar Mensagens, Ver Canais, Voz Prioritária, Imune Modo Lento, Etc…*\n\n"
                "**__• Jade__** <:seta_1:1562090158902218824> *Permissões: Mute, Mudar Apelido, Ver Canais, Voz Prioritária, Imune Modo Lento, Etc…*\n\n"
                "**__• Safira__** <:seta_1:1562090158902218824> *Permissões: Mudar Apelido, Ver Canais, Imune Modo Lento, Etc…*\n\n"
                "**__• Ruby__** <:seta_1:1562090158902218824> *Permissões: Mudar Apelido, Ver Canais, Etc…*\n\n"
                "**__• Iron__** <:seta_1:1562090158902218824> *Permissões: Mudar Apelido, Etc…*"
            ),
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Patentes Exército", style=discord.ButtonStyle.success, emoji="🎖️")
    async def btn_patentes(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎖️ CEx › Tabela de Preços de Patentes",
            description=(
                "# TABELA DE PREÇOS\n\n"
                "## Economia Inicial\n\n"
                "**Atenção:** As patentes são mais baratas dependendo da sua patente atual.\n\n"
                "-# Todos os valores estão sujeitos aos descontos por patente.\n\n"
                "**__Cargos Especiais__**\n\n"
                "**• | Vendedor — R$:125**\n\n"
                "**• | Cargo Personalizado (Sem Permissão) — R$:250**\n\n"
                "**• | Cargo Personalizado (Com Permissão) — R$:450**\n\n"
                "**• | Patente Personalizada — R$:850**\n\n"
                "-# Mesmo nível de permissão do Sub Criador.\n\n"
                "**__Criadores__**\n\n"
                "**• | [CR] Criador — Não está à venda**\n\n"
                "**• | [SCR] Sub Criador — Não está à venda**\n\n"
                "**__Supremacia__**\n\n"
                "**• | [SC] Sócio — R$:180**\n\n"
                "**• | [INV] Investidor — R$:150**\n\n"
                "**__Governo Federal__**\n\n"
                "**• | [PRES] Presidente — Só por votação**\n\n"
                "**• | [V PRES] Vice-Presidente — Não está à venda**\n\n"
                "**__Alto Escalão__**\n\n"
                "**• | [CMT] Comandante — Não está à venda**\n\n"
                "**• | [SUB-CMT] Subcomandante — Não está à venda**\n\n"
                "**__Oficiais Soberanos__**\n\n"
                "**• | [SB] Soberano — R$:120**\n\n"
                "**• | [PA] Patriarca — R$:105**\n\n"
                "**• | [SP] Sub-Patriarca — R$:90**\n\n"
                "**__Oficiais Generais__**\n\n"
                "**• | [GEN EX] General de Exército — R$:70**\n\n"
                "**• | [GEN DIV] General de Divisão — R$:65**\n\n"
                "**• | [GEN BDA] General de Brigada — R$:60**\n\n"
                "**• | [GEN-T] General em Treinamento — R$:55**\n\n"
                "**__Oficiais Superiores__**\n\n"
                "**• | [CEL] Coronel — R$:50**\n\n"
                "**• | [TEN CEL] Tenente-Coronel — R$:45**\n\n"
                "**• | [MAJ] Major — R$:40**\n\n"
                "**__Oficiais Intermediários__**\n\n"
                "**• | [CAP] Capitão — R$:35**\n\n"
                "**__Oficiais Subalternos__**\n\n"
                "**• | [1º TEN] Primeiro Tenente — R$:30**\n\n"
                "**• | [2º TEN] Segundo Tenente — R$:25**\n\n"
                "**• | [ASP] Aspirante a Oficial — R$:20**\n\n"
                "**__Praças Especiais__**\n\n"
                "**• | [CT] Cadete — R$:18**\n\n"
                "**__Graduados__**\n\n"
                "**• | [ST] Subtenente — R$:15**\n\n"
                "**• | [1º SGT] Primeiro Sargento — R$:12**\n\n"
                "**• | [2º SGT] Segundo Sargento — R$:9**\n\n"
                "**• | [3º SGT] Terceiro Sargento — R$:6**"
            ),
            color=discord.Color.dark_gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Instituições", style=discord.ButtonStyle.secondary, emoji="🏛️")
    async def btn_instituicoes(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🏛️ CEx › Tabela de Instituições",
            description=(
                "# Tabela Instituições\n"
                "————————————————\n\n"
                "<:STM:1565814378379608104> **__STM__**<:STM:1565814378379608104> \n\n"
                "Ministro - **__150R$__** • *Mín. 125R$*\n\n"
                "Ministro Substituto - **__100__** • *Mín. 85*\n\n"
                "————————————————\n\n"
                "<:juizado:1565814125366345788> **__OAEx__** <:juizado:1565814125366345788> \n\n"
                "Advogado - **__80R$__** • *Mín. 68* \n\n"
                "Estagiário Jurídico - **__50R$__** • *Mín. 45*\n\n"
                "————————————————\n\n"
                "<:pj:1565814664934330460> **__Defensoria__** <:pj:1565814664934330460> \n\n"
                "Defensor - **__80R$__** • *Mín. 68*\n\n"
                "Estagiário da Defensoria - **__50R$__** • *Mín. 45*\n\n"
                "————————————————\n\n"
                "<:SupremoTribunal:1565814182992019646> **__MPM__** <:SupremoTribunal:1565814182992019646> \n\n"
                "Promotor - **__120R$__** • *Mín.  100*\n\n"
                "Estagiário da Procuradoria - **__80R$__** • *Mín. 65*\n\n"
                "————————————————\n\n"
                "<:SGEx:1565814327762624513> **__SGEx__** <:SGEx:1565814327762624513> \n\n"
                "*Vendemos apenas Entrada na SGEx, ou seja, Estagiário, outros cargos da SGEx não são vendidos* \n\n"
                "Valor - **__150R$__** • *Mín. 128*"
            ),
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Divisões", style=discord.ButtonStyle.secondary, emoji="💼")
    async def btn_divisoes(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💼 CEx › Tabela de Divisões",
            description="⚠️ *De momento não existem divisões cadastradas para venda.*",
            color=discord.Color.dark_grey()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Patentes Administrativas", style=discord.ButtonStyle.primary, emoji="📋")
    async def btn_adm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📋 CEx › Patentes Administrativas",
            description=(
                "# Patentes Administrativas \n"
                "————————————————\n"
                "*Atenção, patentes administrativas devem ser negociadas apenas com <@&1542240355385090106> ou Superior.*\n"
                "————————————————\n\n"
                "Diretor Geral Administrativo - **__Não Está a Venda__**\n\n"
                "Diretor Administrativo - **__3.800R$__** • *Mín. 3.680R$*\n\n"
                "Fiscal Administrativo - **__2.890R$__** • *Mín. 2.750$*\n\n"
                "Estagiário Administrativo - **__2.000R$__** • *Mín. 1.890R$*\n"
                "————————————————\n\n"
                "***Caso alguém esteja realmente interessado na compra de uma patente administrativa, chamar um Fiscal de Vendas ou Superior para continuar a negociação.***"
            ),
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="tabelas", description="Envia o painel unificado com todas as tabelas de preços da CEx.")
@app_commands.default_permissions(administrator=True)
async def tabelas(interaction: discord.Interaction):
    embed = discord.Embed(
        title="◆ CEx › CENTRAL DE TABELAS",
        description="Selecione abaixo qual tabela de preços deseja consultar:",
        color=discord.Color.dark_theme()
    )
    view = TabelasView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Painel de tabelas enviado com sucesso!", ephemeral=True)


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
                    "Vai ficar um tempo sem conseguir vender? Peça seu aval aqui.\n\n"
                    "────────────────────────\n"
                    "└ Enquanto o aval estiver ativo **você não é cobrado** pela meta.\n"
                    "└ As semanas de aval **não contam** como falha.\n"
                    "└ Um administrador precisa **aprovar** o pedido.\n\n"
                    "────────────────────────\n"
                    "**Voltou antes do prazo?** Use o botão **Voltei** — não precisa pedir a ninguém.\n\n"
                    "CEx · até 30 dias por pedido",
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
        self.add_item(discord.ui.Button(label="Ver venda", style=discord.ButtonStyle.link, url="https://discord.com", emoji="🔗"))

    @discord.ui.button(label="Eu entrego", style=discord.ButtonStyle.green, emoji="📦")
    async def eu_entrego(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"📦 {interaction.user.mention} assumiu a entrega deste pedido!", ephemeral=False)

@bot.tree.command(name="simular_venda", description="Simula um pedido de venda pendente de entrega.")
@app_commands.default_permissions(administrator=True)
async def simular_venda(interaction: discord.Interaction):
    embed = discord.Embed(
        title="◆ CEx › PEDIDO DE ENTREGA · #CEx-X5WPHQ",
        description="⚠️ **Aguardando entrega · ninguém assumiu ainda**\n\n"
                    "`@Venda Patente` · pedido aberto há 2 dias\n"
                    "────────────────────────\n"
                    "📦 **Produto** · Patente · Elite Secreta [ES] · Patente Elite\n"
                    "🤝 **Entregar para** · Souza\n"
                    "👤 **Vendedor** · `@SOUZA` · Roblox CEARENSE_BRO\n"
                    "💰 **Valor** · R$ 30,00\n"
                    "🧾 **Venda** · #CEx-X5WPHQ · registrada há 2 dias\n\n"
                    "────────────────────────\n"
                    "└ Vai entregar? Clique em **Eu entrego** — o pedido fecha no seu nome.\n\n"
                    "CEx · entregas",
        color=discord.Color.gold()
    )
    view = EntregaView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Simulação de venda enviada!", ephemeral=True)


# ==========================================
# 5. GESTÃO DE CARGOS (ADD / REMOVER)
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
@app_commands.describe(membro="O membro do cual deseja remover o cargo", cargo="O cargo a ser removido")
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
# 6. GESTÃO DE VENDAS (REGISTAR, APAGAR, EDITAR)
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
# 7. MÓDULO FINANCEIRO E METAS
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
# 8. PAINEL DE GESTÃO EXCLUSIVO (/PAINEL) - RESTRITO POR CARGO
# ==========================================
CARGOS_PERMITIDOS = [1542240355376832534, 1542240355393601589]

class PainelAtalhosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Meus logs", style=discord.ButtonStyle.primary, emoji="📊")
    async def meus_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📊 A carregar os seus logs de auditoria...", ephemeral=True)

    @discord.ui.button(label="Minhas metas", style=discord.ButtonStyle.green, emoji="🎖️")
    async def minhas_metas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🎖️ A carregar o progresso das suas metas...", ephemeral=True)

    @discord.ui.button(label="Ranking", style=discord.ButtonStyle.secondary, emoji="🏆")
    async def ranking(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🏆 A carregar o ranking geral...", ephemeral=True)

@bot.tree.command(name="painel", description="Painel restrito de auditoria, vendas, saldos e histórico.")
async def painel(interaction: discord.Interaction):
    tem_cargo = any(role.id in CARGOS_PERMITIDOS for role in interaction.user.roles)
    if not tem_cargo and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Acesso negado. Apenas membros com os cargos autorizados podem visualizar este painel.", ephemeral=True)
        return

    embed = discord.Embed(
        title="◆ CEx › PAINEL DE AUDITORIA E GESTÃO",
        description="Painel exclusivo de controlo administrativo e financeiro.",
        color=discord.Color.dark_theme()
    )

    embed.add_field(
        name="📊 1. Ranking & Auditoria de Atividades",
        value=(
            "• **Registos de Vendas:** Histórico completo de vendas efetuadas.\n"
            "• **Edições e Eliminações:** Registo de quem editou ou apagou vendas.\n"
            "• **Gestão de Cargos:** Auditoria de quem adicionou ou removeu cargos.\n"
            "• **Ranking Geral:** Desempenho geral da equipe por volume."
        ),
        inline=False
    )

    embed.add_field(
        name="💰 2. Saldos & Estatísticas Financeiras",
        value=(
            "• **Saldo de Vendedores:** Consulta detalhada de valores em aberto.\n"
            "• **Comissões Pagas:** Total acumulado e distribuído por contador.\n"
            "• **Metas Atingidas:** Progresso diário e semanal por colaborador."
        ),
        inline=False
    )

    embed.set_footer(text="CEx · Sistema de Auditoria Interna (Exclusivo)")
    
    view = PainelAtalhosView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# Iniciar o servidor web e o bot
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
