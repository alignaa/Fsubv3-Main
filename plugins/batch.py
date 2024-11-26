from config import *
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from core.bot import Bot
from core.func import *

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(client: Client, message: Message):
    # Pesan pertama
    try:
        first_message = await client.ask(
            text="<b>Silahkan Forward Pesan/File Pertama dari Channel DataBase. (Forward with Quote)</b>\n\n<b>atau Kirim Link Postingan dari Channel Database</b>",
            chat_id=message.from_user.id,
            filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
            timeout=60,
        )
        f_msg_id = await get_message_id(client, first_message)
        if not f_msg_id:
            await first_message.reply(
                "❌ <b>ERROR</b>\n\n<b>Postingan yang Diforward ini bukan dari Channel Database saya</b>",
                quote=True,
            )
            return
    except BaseException:
        return

    # Pesan kedua
    try:
        second_message = await client.ask(
            text="<b>Silahkan Forward Pesan/File Terakhir dari Channel DataBase. (Forward with Quote)</b>\n\n<b>atau Kirim Link Postingan dari Channel Database</b>",
            chat_id=message.from_user.id,
            filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
            timeout=60,
        )
        s_msg_id = await get_message_id(client, second_message)
        if not s_msg_id:
            await second_message.reply(
                "❌ <b>ERROR</b>\n\n<b>Postingan yang Diforward ini bukan dari Channel Database saya</b>",
                quote=True,
            )
            return
    except BaseException:
        return

    # Membuat link berbagi
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
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
        f"<b>Link Sharing File Berhasil Dibuat:</b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup,
    )


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("genlink"))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="<b>Silahkan Forward Pesan dari Channel DataBase. (Forward with Qoute)</b>\n\n<b>atau Kirim Link Postingan dari Channel Database</b>",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except BaseException:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        await channel_message.reply(
            "❌ <b>ERROR</b>\n\n<b>Postingan yang Diforward ini bukan dari Channel Database saya</b>",
            quote=True,
        )
        continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔁 Share Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )
    await channel_message.reply_text(
        f"<b>Link Sharing File Berhasil Di Buat:</b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup,
            )
