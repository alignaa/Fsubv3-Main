import config
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from core.bot import Bot
from core import func


@Bot.on_message(filters.private & filters.user(config.ADMINS) & filters.command("batch"))
async def batch(c: Bot, message: Message):
    while True:
        try:
            # Meminta pesan pertama atau tautan
            first_message = await c.ask(
                text="Teruskan pesan pertama atau paste link post dari CHANNEL_DB.",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except Exception:
            await message.reply("Waktu habis. Silakan coba lagi.", quote=True)
            return

        # Mendapatkan ID pesan pertama
        f_msg_id = await func.get_message_id(c, first_message)
        if f_msg_id is not None:
            break

        await first_message.reply(
            "Pesan tidak valid atau tidak berasal dari channel yang sesuai.",
            quote=True,
        )
        continue

    while True:
        try:
            # Meminta pesan terakhir atau tautan
            second_message = await c.ask(
                text="Teruskan pesan akhir atau paste link post dari CHANNEL_DB.",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except Exception:
            await message.reply("Waktu habis. Silakan coba lagi.", quote=True)
            return

        # Mendapatkan ID pesan terakhir
        s_msg_id = await func.get_message_id(c, second_message)
        if s_msg_id is not None:
            break

        await second_message.reply(
            "Pesan tidak valid atau tidak berasal dari channel yang sesuai.",
            quote=True,
        )
        continue

    # Membuat string unik untuk start parameter
    try:
        string = f"get-{f_msg_id * abs(c.db_channel.id)}-{s_msg_id * abs(c.db_channel.id)}"
        base64_string = await func.encode(string)
        link = f"https://t.me/{c.username}?start={base64_string}"

        # Membuat tombol untuk membagikan link
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Bagikan Link", url=f"https://telegram.me/share/url?url={link}"
                    )
                ]
            ]
        )

        # Mengirimkan link ke pengguna
        await second_message.reply_text(
            f"Berikut adalah link Anda: {link}",
            quote=True,
            reply_markup=reply_markup,
        )
    except Exception as e:
        await message.reply(f"Terjadi kesalahan: {e}", quote=True)
