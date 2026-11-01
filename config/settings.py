import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

COLOR_PRIMARY = 0xD4AF37  # Dourada
COLOR_BACKGROUND = 0x0F172A
COLOR_DETAILS = 0x24185E

