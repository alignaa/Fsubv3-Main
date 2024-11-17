from pyrogram import enums
from pyrogram.types import InlineKeyboardButton
from config import FORCE_SUB_, BUTTON_ROW

chat_info_cache = {}


async def get_chat_info(client, chat_id):
    if chat_id in chat_info_cache:
        return chat_info_cache[chat_id]
    chat_info = await client.get_chat(chat_id)
    chat_info_cache[chat_id] = chat_info
    return chat_info


async def start_button(client):
    if not FORCE_SUB_:
        buttons = [
            [
                InlineKeyboardButton(text="ʙᴀɴᴛᴜᴀɴ", callback_data="help"),
                InlineKeyboardButton(text="ᴄʟᴏꜱᴇ", callback_data="close"),
            ],
        ]
        return buttons

    dynamic_button = []
    current_row = []
    for key in FORCE_SUB_.keys():
        chat_id = FORCE_SUB_[key]
        chat_info = await get_chat_info(client, chat_id)
        chat_type = chat_info.type
        button_name = "ᴄʜᴀɴɴᴇʟ" if chat_type == enums.ChatType.CHANNEL else "ᴄʜᴀɴɴᴇʟ"
        current_row.append(InlineKeyboardButton(text=f"·ᴊᴏɪɴ {button_name}·", url=getattr(client, f'invitelink{key}')))
        if len(current_row) == BUTTON_ROW:
            dynamic_button.append(current_row)
            current_row = []

    if current_row:
        dynamic_button.append(current_row)

    buttons = [
        [
            InlineKeyboardButton(text="ʙᴀɴᴛᴜᴀɴ", callback_data="help"),
        ],
    ] + dynamic_button + [
        [InlineKeyboardButton(text="ᴄʟᴏꜱᴇ", callback_data="close")],
    ]
    return buttons


async def fsub_button(client, message):
    if FORCE_SUB_:
        dynamic_button = []
        current_row = []
        for key in FORCE_SUB_.keys():
            chat_id = FORCE_SUB_[key]
            chat_info = await get_chat_info(client, chat_id)
            chat_type = chat_info.type
            button_name = "ᴄʜᴀɴɴᴇʟ" if chat_type == enums.ChatType.CHANNEL else "ɢʀᴏᴜᴘ"
            current_row.append(InlineKeyboardButton(text=f"·ᴊᴏɪɴ {button_name}·", url=getattr(client, f'invitelink{key}')))
            if len(current_row) == BUTTON_ROW:
                dynamic_button.append(current_row)
                current_row = []

        if current_row:
            dynamic_button.append(current_row)

        try:
            dynamic_button.append([
                InlineKeyboardButton(
                    text="ᴄᴏʙᴀ ʟᴀɢɪ",
                    url=f"https://t.me/{client.username}?start={message.command[1]}",
                )
            ])
        except IndexError:
            pass

        return dynamic_button
