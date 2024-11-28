
from pyrogram import filters
from pyrogram.types import *
from config import *
from core.bot import Bot
from core.func import *

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(c: Bot, message: Message):
    # Meminta pesan pertama
    await message.reply_text(
        "Teruskan pesan pertama atau paste link post dari CHANNEL_DB.",
        reply_markup=ReplyKeyboardRemove(),
    )
    try:
        first_message = await c.listen(message.chat.id, timeout=60)
        f_msg_id = await get_message_id(c, first_message)
        if not f_msg_id:
            await first_message.reply_text("Pesan pertama tidak valid.", quote=True)
            return  # Akhiri fungsi jika pesan pertama tidak valid
    except TimeoutError:
        return await message.reply_text("Waktu habis. Silakan coba lagi.", quote=True)
    
    # Meminta pesan akhir
    await message.reply_text(
        "Teruskan pesan akhir atau paste link post dari CHANNEL_DB.",
        reply_markup=ReplyKeyboardRemove(),
    )
    try:
        second_message = await c.listen(message.chat.id, timeout=60)
        s_msg_id = await get_message_id(c, second_message)
        if not s_msg_id:
            await second_message.reply_text("Pesan akhir tidak valid.", quote=True)
            return  # Akhiri fungsi jika pesan akhir tidak valid
    except TimeoutError:
        return await message.reply_text("Waktu habis. Silakan coba lagi.", quote=True)

    # Membuat link
    string = f"get-{f_msg_id * abs(c.db_channel.id)}-{s_msg_id * abs(c.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{c.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Bagikan Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )
    await second_message.reply_text(
        f"Link: {link}",
        quote=True,
        reply_markup=reply_markup,
    )
