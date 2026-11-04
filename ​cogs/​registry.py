import discord
from discord.ext import commands
from ui.embeds import create_base_embed

class NickModal(discord.ui.Modal):
    def __init__(self, action_type: str):
        super().__init__(title="Registro de Nick - CEx System")
        self.action_type = action_type
        
        self.roblox_nick = discord.ui.InputText(
            label="Nick do Roblox",
            placeholder="Digite o seu nick exato no Roblox...",
            required=True
        )
        self.discord_nick = discord.ui.InputText(
            label="Nick / ID do Discord",
            placeholder="Digite o seu nick no Discord...",
            required=True
        )
        
        self.add_item(self.roblox_nick)
        self.add_item(self.discord_nick)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        # Aqui entra a lógica de salvamento no Supabase
        titulo = "Registro Realizado" if self.action_type == "registrar" else "Cadastro Atualizado"
        
        embed = create_base_embed(
            title=titulo,
            description=f"As suas informações foram processadas com sucesso pelo sistema.",
            category="Registro de Nick"
        )
        embed.add_field(name="Roblox", value=self.roblox_nick.value, inline=True)
        embed.add_field(name="Discord", value=self.discord_nick.value, inline=True)
        
        await interaction.followup.send(embed=embed, ephemeral=True)

class NickView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Registrar", style=discord.ButtonStyle.success, custom_id="btn_registrar_nick")
    async def registrar_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = NickModal(action_type="registrar")
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Atualizar", style=discord.ButtonStyle.primary, custom_id="btn_atualizar_nick")
    async def atualizar_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = NickModal(action_type="atualizar")
        await interaction.response.send_modal(modal)

class RegisterNickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="registrar_nick", description="Publica o painel de registro de nick do Roblox e Discord")
    async def registrar_nick(self, ctx: discord.ApplicationContext):
        embed = create_base_embed(
            title="Registro de Nick",
            description="Clique em **Registrar** para inserir os seus dados pela primeira vez ou em **Atualizar** para alterar o seu cadastro existente[span_7](start_span)[span_7](end_span).",
            category="Registro de Nick"
        )
        view = NickView()
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(RegisterNickCog(bot))
