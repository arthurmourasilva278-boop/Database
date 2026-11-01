import discord
from discord.ext import commands
from utils.embeds import CExEmbed

class WalletCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="carteira", description="Consulta os dados da sua carteira e comissões")
    async def carteira(self, ctx):
        embed = CExEmbed(
            title="Carteira do Vendedor",
            description="**Saldo Disponível:** R$ 0.00\n**Total Vendido:** R$ 0.00"
        )
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(WalletCog(bot))
