import os
import config

from pyrogram import filters
from pyrogram.types import Message
from dotenv import load_dotenv

from core.bot import Bot



@Bot.on_message(filters.command("env") & filters.user(config.ADMINS) & filters.private)
async def show_env_info(client: Bot, message: Message):
    env_vars_to_show = [
        "APP_ID",
        "API_HASH",
        "BOT_TOKEN",
        "ADMINS",
        "OWNER",
        "CHANNEL_DB",
        "DATABASE_TYPE",
        "DB_URL",
        "MONGO_NAME",
        "MONGO_URL",
    ]
    for key in os.environ:
        if key.startswith("FORCE_SUB_"):
            env_vars_to_show.append(key)
    env_info_text = "\n".join([f"<b>{var}:</b> <code>{os.getenv(var)}</code>" for var in env_vars_to_show])
    await message.reply(f"<b>Variabel Lingkungan:</b>\n\n{env_info_text}")
