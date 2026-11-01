import discord
from discord.ext import commands
from utils.embeds import CExEmbed

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="painel", description="Acessa o Painel Administrativo CEx")
    async def painel(self, ctx):
        embed = CExEmbed(
            title="Painel Administrativo - CEx System",
            description="Selecione uma opção administrativa no menu abaixo."
        )
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(AdminCog(bot))
