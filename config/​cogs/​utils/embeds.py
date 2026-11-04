import discord
from datetime import datetime
from config.settings import EMBED_COLOR, BOT_FOOTER_TEXT

def create_base_embed(title: str, description: str = None, category: str = None) -> discord.Embed:
    embed = discord.Embed(
        title=f"🟢 CEx │ {title}",
        description=description,
        color=EMBED_COLOR,
        timestamp=datetime.utcnow()
    )
    footer_text = f"{BOT_FOOTER_TEXT} • {category}" if category else BOT_FOOTER_TEXT
    embed.set_footer(text=footer_text)
    return embed
