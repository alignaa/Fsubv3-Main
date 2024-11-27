import config
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from core.bot import Bot
from core import func

async def get_valid_message(c, user_id, prompt_text):
    """
    Fungsi untuk meminta pesan yang valid dari pengguna.
    """
    try:
        user_message = await c.ask(
            text=prompt_text,
            chat_id=user_id,
            filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
            timeout=60,
        )
        msg_id = await get_message_id(c, user_message)
        if not msg_id:
            await user_message.reply("Error! Pesan tidak valid. Silakan coba lagi.", quote=True)
            return None
        return msg_id
    except Exception:
        return None


@Bot.on_message(filters.command("batch"))
async def generate_link_handler(c, message):
    """
    Handler utama untuk menghasilkan link berdasarkan dua pesan.
    """
    user_id = message.from_user.id

    # Meminta pesan pertama
    first_prompt = "Teruskan pesan pertama atau paste link post dari CHANNEL_DB:"
    f_msg_id = await get_valid_message(c, user_id, first_prompt)
    if not f_msg_id:
        return await message.reply("Gagal mendapatkan pesan pertama. Proses dihentikan.")

    # Meminta pesan kedua
    second_prompt = "Teruskan pesan akhir atau paste link post dari CHANNEL_DB:"
    s_msg_id = await get_valid_message(c, user_id, second_prompt)
    if not s_msg_id:
        return await message.reply("Gagal mendapatkan pesan kedua. Proses dihentikan.")

    # Membuat string dan encoding ke Base64
    try:
        string = f"get-{f_msg_id * abs(c.db_channel.id)}-{s_msg_id * abs(c.db_channel.id)}"
        base64_string = await encode(string)
        link = f"https://t.me/{c.username}?start={base64_string}"
    except Exception as e:
        return await message.reply(f"Terjadi kesalahan saat membuat link: {e}")

    # Mengirimkan link ke pengguna
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Bagikan Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )
    await message.reply_text(
        f"Link: {link}",
        quote=True,
        reply_markup=reply_markup,
    )