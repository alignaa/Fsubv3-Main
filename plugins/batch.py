from config import *
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from core.bot import Bot
from core.func import *

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(client: Client, message: Message):
    # Minta pengguna mengirim pesan pertama
    await message.reply(
        "<b>Silahkan Forward Pesan/File Pertama dari Channel DataBase. (Forward with Qoute)</b>\n\n<b>atau Kirim Link Postingan dari Channel Database</b>",
        quote=True
    )
    # Tunggu pesan dari pengguna
    first_message = await client.listen(
        message.chat.id,
        filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
        timeout=60
    )
    f_msg_id = await get_message_id(client, first_message)
    if not f_msg_id:
        await first_message.reply(
            "❌ <b>ERROR</b>\n\n<b>Postingan yang Diforward ini bukan dari Channel Database saya</b>",
            quote=True,
        )
        return  # Kembali jika pesan tidak valid

    # Minta pengguna mengirim pesan kedua
    await message.reply(
        "<b>Silahkan Forward Pesan/File Terakhir dari Channel DataBase. (Forward with Qoute)</b>\n\n<b>atau Kirim Link Postingan dari Channel Database</b>",
        quote=True
    )
    # Tunggu pesan dari pengguna
    second_message = await client.listen(
        message.chat.id,
        filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
        timeout=60
    )
    s_msg_id = await get_message_id(client, second_message)
    if not s_msg_id:
        await second_message.reply(
            "❌ <b>ERROR</b>\n\n<b>Postingan yang Diforward ini bukan dari Channel Database saya</b>",
            quote=True,
        )
        return  # Kembali jika pesan tidak valid

    # Generate link dengan ID pesan yang diperoleh
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    
    # Kirimkan hasil dan tombol untuk membagikan link
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔁 Share Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )
    await second_message.reply_text(
        f"<b>Link Sharing File Berhasil Di Buat:</b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup,
    )
    
