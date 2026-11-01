import discord
from discord.ext import commands
from utils.embeds import CExEmbed

class RegistryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="registrar_nick", description="Registra ou atualiza seu nick Roblox/Discord")
    async def registrar_nick(self, ctx, roblox_nick: str, discord_nick: str):
        embed = CExEmbed(
            title="Registro de Nick",
            description=f"**Roblox:** {roblox_nick}\n**Discord:** {discord_nick}\n\nRegistro concluído com sucesso!"
        )
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(RegistryCog(bot))

