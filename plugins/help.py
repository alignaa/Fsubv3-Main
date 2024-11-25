from core.bot import Bot

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from pyrogram.types import InlineKeyboardButton


class Data:
    HELP = """
<b>Pengguna Bot</b>
  /start - Mulai Bot
  /about - Tentang Bot
  /help - Bantuan Bot
  /ping - Latensi Bot
  /uptime - Waktu aktif Bot
 
<b>Admin Bot</b>
  /log - Mengambil log Bot
  /users - Statistik pengguna 
  /batch - Multi post dalam satu link
  /broadcast - Pesan siaran
"""

    close = [
        [InlineKeyboardButton("Tutup", callback_data="close")]
    ]

    mbuttons = [
        [
            InlineKeyboardButton("Bantuan", callback_data="help"),
            InlineKeyboardButton("Tutup", callback_data="close")
        ],
    ]

    buttons = [
        [
            InlineKeyboardButton("Tentang", callback_data="about"),
            InlineKeyboardButton("Tutup", callback_data="close")
        ],
    ]

    ABOUT = """
@{} adalah Bot untuk menyimpan postingan atau file yang dapat diakses melalui link khusus.

  Framework: <a href='https://docs.pyrofork.org'>pyrofork</a>
  Re-Code From: <a href='https://github.com/mrismanaziz/File-Sharing-Man'>File-Sharing-Man</a>
  Re-build From: <a href='https://github.com/Ling-ex/File-Haram'>File-Sharing</a>
"""


@Bot.on_message(filters.private & filters.incoming & filters.command("help"))
async def help(c: Bot, m: Message):
    await c.send_message(
        m.chat.id, 
        Data.HELP,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )


@Bot.on_callback_query()
async def handler(c: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        try:
            await query.message.edit_text(
                text=Data.ABOUT.format(c.username),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.mbuttons),
            )
        except Exception:
            pass
    elif data == "help":
        try:
            await query.message.edit_text(
                text=Data.HELP,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
        except Exception:
            pass
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except Exception:
            return
