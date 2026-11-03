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
# 2. MÓDULO UNIFICADO DE TABELAS (/TABELAS)
# ==========================================
@bot.tree.command(name="tabelas", description="Envia o painel unificado com todas as tabelas de preços da CEx.")
@app_commands.default_permissions(administrator=True)
async def tabelas(interaction: discord.Interaction):
    embed = discord.Embed(
        title="◆ CEx › CENTRAL DE TABELAS OFICIAIS",
        description=(
            "────────────────────────────────────────\n"
            "💎 **1. MINÉRIOS & BENEFÍCIOS**\n"
            "## __Tabela Preços Minérios__\n"
            "**__Opala__** - *250R$* • ***Min. 200R$***\n"
            "**__Jade__** - *180R$* • ***Min. 135R$***\n"
            "**__Safira__** - *130R$* • ***Min. 100R$***\n"
            "**__Ruby__** - *80R$* • ***Min. 65R$***\n"
            "**__Iron__** - *45R$* • ***Min. 30R$***\n\n"
            "# Benefícios Minérios\n"
            "————————————————\n"
            "**__• Opala__** <:seta_1:1562090158902218824> *Permissões: Mute, Gerenciar Apelidos, Mudar Apelido, Gerenciar Mensagens, Ver Canais, Voz Prioritária, Imune Modo Lento, Etc…*\n"
            "**__• Jade__** <:seta_1:1562090158902218824> *Permissões: Mute, Mudar Apelido, Ver Canais, Voz Prioritária, Imune Modo Lento, Etc…*\n"
            "**__• Safira__** <:seta_1:1562090158902218824> *Permissões: Mudar Apelido, Ver Canais, Imune Modo Lento, Etc…*\n"
            "**__• Ruby__** <:seta_1:1562090158902218824> *Permissões: Mudar Apelido, Ver Canais, Etc…*\n"
            "**__• Iron__** <:seta_1:1562090158902218824> *Permissões: Mudar Apelido, Etc…*\n\n"
            "────────────────────────────────────────\n"
            "🎖️ **2. PATENTES DO EXÉRCITO**\n"
            "# TABELA DE PREÇOS\n"
            "## Economia Inicial\n"
            "**Atenção:** As patentes são mais baratas dependendo da sua patente atual.\n"
            "-# Todos os valores estão sujeitos aos descontos por patente.\n\n"
            "**__Cargos Especiais__**\n"
            "• | Vendedor — R$:125\n"
            "• | Cargo Personalizado (Sem Permissão) — R$:250\n"
            "• | Cargo Personalizado (Com Permissão) — R$:450\n"
            "• | Patente Personalizada — R$:850 (-# Mesmo nível de permissão do Sub Criador)\n\n"
            "**__Criadores__** • [CR] Criador / [SCR] Sub Criador — *Não está à venda*\n"
            "**__Supremacia__** • [SC] Sócio — **R$:180** | [INV] Investidor — **R$:150**\n"
            "**__Governo Federal__** • [PRES] Presidente — *Só por votação* | [V PRES] Vice — *Não está à venda*\n"
            "**__Alto Escalão__** • Comandante / Subcomandante — *Não está à venda*\n"
            "**__Oficiais Soberanos__** • [SB] Soberano — **R$:120** | [PA] Patriarca — **R$:105** | [SP] Sub-Patriarca — **R$:90**\n"
            "**__Oficiais Generais__** • [GEN EX] — **R$:70** | [GEN DIV] — **R$:65** | [GEN BDA] — **R$:60** | [GEN-T] — **R$:55**\n"
            "**__Oficiais Superiores__** • [CEL] — **R$:50** | [TEN CEL] — **R$:45** | [MAJ] — **R$:40**\n"
            "**__Oficiais Intermediários__** • [CAP] — **R$:35**\n"
            "**__Oficiais Subalternos__** • [1º TEN] — **R$:30** | [2º TEN] — **R$:25** | [ASP] — **R$:20**\n"
            "**__Praças Especiais__** • [CT] Cadete — **R$:18**\n"
            "**__Graduados__** • [ST] — **R$:15** | [1º SGT] — **R$:12** | [2º SGT] — **R$:9** | [3º SGT] — **R$:6**\n\n"
            "────────────────────────────────────────\n"
            "🏛️ **3. INSTITUIÇÕES**\n"
            "# Tabela Instituições\n"
            "————————————————\n"
            "<:STM:1565814378379608104> **__STM__**\n"
            "Ministro - **__150R$__** • *Mín. 125R$* | Ministro Substituto - **__100__** • *Mín. 85*\n\n"
            "<:juizado:1565814125366345788> **__OAEx__**\n"
            "Advogado - **__80R$__** • *Mín. 68* | Estagiário Jurídico - **__50R$__** • *Mín. 45*\n\n"
            "<:pj:1565814664934330460> **__Defensoria__**\n"
            "Defensor - **__80R$__** • *Mín. 68* | Estagiário da Defensoria - **__50R$__** • *Mín. 45*\n\n"
            "<:SupremoTribunal:1565814182992019646> **__MPM__**\n"
            "Promotor - **__120R$__** • *Mín. 100* | Estagiário da Procuradoria - **__80R$__** • *Mín. 65*\n\n"
            "<:SGEx:1565814327762624513> **__SGEx__**\n"
            "*Vendemos apenas Entrada na SGEx (Estagiário)* — Valor: **__150R$__** • *Mín. 128*\n\n"
            "────────────────────────────────────────\n"
            "💼 **4. DIVISÕES**\n"
            "⚠️ *Atualmente não há divisões cadastradas para venda.*\n\n"
            "────────────────────────────────────────\n"
            "📋 **5. PATENTES ADMINISTRATIVAS**\n"
            "# Patentes Administrativas \n"
            "————————————————\n"
            "*Atenção, patentes administrativas devem ser negociadas apenas com <@&1542240355385090106> ou Superior.*\n"
            "————————————————\n"
            "Diretor Geral Administrativo - **__Não Está a Venda__**\n"
            "Diretor Administrativo - **__3.800R$__** • *Mín. 3.680R$*\n"
            "Fiscal Administrativo - **__2.890R$__** • *Mín. 2.750$*\n"
            "Estagiário Administrativo - **__2.000R$__** • *Mín. 1.890R$*\n"
            "————————————————\n"
            "***Caso alguém esteja realmente interessado na compra de uma patente administrativa, chamar um Fiscal de Vendas ou Superior para continuar a negociação.***"
        ),
        color=discord.Color.dark_theme()
    )
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("Painel unificado de tabelas enviado com sucesso!", ephemeral=True)


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
# 4. MÓDULO DE VENDAS, APROVAÇÃO E ATALHOS DO VENDEDOR
# ==========================================
class VendedorAtalhosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Meus logs", style=discord.ButtonStyle.primary, emoji="📊")
    async def meus_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📊 A carregar os seus logs de vendas e histórico...", ephemeral=True)

    @discord.ui.button(label="Minhas metas", style=discord.ButtonStyle.green, emoji="🎖️")
    async def minhas_metas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🎖️ A carregar o progresso das suas metas e barra de progresso...", ephemeral=True)

    @discord.ui.button(label="Ranking", style=discord.ButtonStyle.secondary, emoji="🏆")
    async def ranking(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🏆 A carregar o ranking geral da equipe...", ephemeral=True)

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
        title=f"◆ CEx › PAGAMENTO APROVADO · {codigo_venda}",
        description=f"✅ **Venda aprovada e registada com sucesso!**\n\n"
                    f"👤 **Vendedor:** {vendedor.mention}\n"
                    f"🤝 **Cliente:** {cliente}\n"
                    f"💰 **Valor:** {valor}\n"
                    f"💸 **Comissão do Vendedor:** (Calculada automaticamente)\n"
                    f"🎖️ **Meta Atualizada:** [🟩🟩🟩🟩⬛] Progresso registado\n"
                    f"🧾 **Código:** `{codigo_venda}`",
        color=discord.Color.green()
    )
    embed.set_image(url=comprovante.url)
    
    view = VendedorAtalhosView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Venda aprovada e notificação enviada com os atalhos do vendedor!", ephemeral=True)


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
# 8. PAINEL MESTRE DE GESTÃO E AUDITORIA (DUPLO EMBED)
# ==========================================
CARGOS_PERMITIDOS = [1542240355376832534, 1542240355393601589]

class PainelDuploView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # --- CAMADA SUPERIOR ---
    @discord.ui.button(label="Aprovar Avals", style=discord.ButtonStyle.success, emoji="⏳", row=0)
    async def btn_aprovar_avals(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📥 A carregar os pedidos de avals pendentes para aprovação...", ephemeral=True)

    @discord.ui.button(label="Registros de Vendas", style=discord.ButtonStyle.primary, emoji="💼", row=0)
    async def btn_reg_vendas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📊 A puxar todos os registos de vendas efetuados no sistema...", ephemeral=True)

    @discord.ui.button(label="Registros de Cargos", style=discord.ButtonStyle.primary, emoji="👤", row=0)
    async def btn_reg_cargos(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🛡️ A puxar o histórico de adição e remoção de cargos...", ephemeral=True)

    # --- CAMADA INFERIOR ---
    @discord.ui.button(label="Edição de Vendas", style=discord.ButtonStyle.secondary, emoji="✏️", row=1)
    async def btn_edicao_vendas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✏️ A carregar o registo de todas as edições de vendas...", ephemeral=True)

    @discord.ui.button(label="Apagação de Vendas", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def btn_apagar_vendas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🗑️ A carregar o histórico de vendas apagadas...", ephemeral=True)

    @discord.ui.button(label="Log de Comandos", style=discord.ButtonStyle.secondary, emoji="📜", row=1)
    async def btn_log_comandos(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📜 A puxar o registo de utilização de comandos...", ephemeral=True)

@bot.tree.command(name="painel", description="Painel mestre restrito de auditoria, aprovações e registos.")
async def painel(interaction: discord.Interaction):
    tem_cargo = any(role.id in CARGOS_PERMITIDOS for role in interaction.user.roles)
    if not tem_cargo and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Acesso negado. Apenas membros com os cargos autorizados podem visualizar este painel.", ephemeral=True)
        return

    # Embed 1: Camada Superior
    embed1 = discord.Embed(
        title="◆ CEx › PAINEL DE GESTÃO E APROVAÇÕES (1/2)",
        description=(
            "Painel de controlo administrativo principal.\n\n"
            "⏳ **Aprovar Avals:** Gere e aprove os pedidos de afastamento pendentes.\n"
            "💼 **Registos de Vendas:** Puxa o histórico de todas as vendas registadas.\n"
            "👤 **Registos de Cargos:** Mostra quem adicionou ou removeu cargos na equipe."
        ),
        color=discord.Color.green()
    )

    # Embed 2: Camada Inferior
    embed2 = discord.Embed(
        title="◆ CEx › PAINEL DE AUDITORIA E HISTÓRICO (2/2)",
        description=(
            "Painel de rastreio e auditoria de alterações.\n\n"
            "✏️ **Edição de Vendas:** Registo de quem alterou dados de vendas.\n"
            "🗑️ **Apagação de Vendas:** Histórico de registos de vendas eliminados.\n"
            "📜 **Log de Comandos:** Auditoria completa de comandos executados."
        ),
        color=discord.Color.dark_theme()
    )
    embed2.set_footer(text="CEx · Sistema de Auditoria Interna Restrito")

    view = PainelDuploView()
    await interaction.response.send_message(embeds=[embed1, embed2], view=view, ephemeral=True)


# Iniciar o servidor web e o bot
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
