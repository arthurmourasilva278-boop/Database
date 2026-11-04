import discord
from discord.ext import commands
from ui.embeds import create_base_embed

class AdminPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Início", style=discord.ButtonStyle.secondary, custom_id="admin_inicio", row=0)
    async def inicio_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = create_base_embed(
            title="Painel Administrativo",
            description="**Central Administrativa**\nGerenciamento e configuração geral do sistema.",
            category="Painel Administrativo"
        )
        embed.add_field(name="📊 Início", value="Visão geral do sistema.", inline=True)
        embed.add_field(name="📜 Logs", value="Canais de registros.", inline=True)
        embed.add_field(name="⚙️ Sistema", value="Status, backup e reset.", inline=True)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Comandos", style=discord.ButtonStyle.secondary, custom_id="admin_comandos", row=0)
    async def comandos_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = create_base_embed(
            title="Gerenciamento de Comandos",
            description="Configure as permissões individuais de cada comando do bot.",
            category="Painel Administrativo"
        )
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Logs", style=discord.ButtonStyle.secondary, custom_id="admin_logs", row=0)
    async def logs_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = create_base_embed(
            title="Configuração de Logs",
            description="Defina os canais de destino para cada tipo de registro do sistema.",
            category="Painel Administrativo"
        )
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Metas", style=discord.ButtonStyle.secondary, custom_id="admin_metas", row=1)
    async def metas_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = create_base_embed(
            title="Configuração de Metas",
            description="Gerencie as metas diárias e semanais dos vendedores e seletiva.",
            category="Painel Administrativo"
        )
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Medalhas", style=discord.ButtonStyle.secondary, custom_id="admin_medalhas", row=1)
    async def medalhas_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = create_base_embed(
            title="Gerenciamento de Medalhas",
            description="Análise e aprovação de solicitações de medalhas.",
            category="Painel Administrativo"
        )
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Cargos Especiais", style=discord.ButtonStyle.secondary, custom_id="admin_cargos", row=1)
    async def cargos_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = create_base_embed(
            title="Cargos Especiais",
            description="Visualização e configuração de cargos do sistema.",
            category="Painel Administrativo"
        )
        await interaction.message.edit(embed=embed, view=self)

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="painel", description="Abre a Central Administrativa do CEx System")
    async def painel(self, ctx: discord.ApplicationContext):
        embed = create_base_embed(
            title="Painel Administrativo",
            description="**Central Administrativa**\nGerenciamento e configuração geral do sistema.",
            category="Painel Administrativo"
        )
        view = AdminPanelView()
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(AdminCog(bot))
