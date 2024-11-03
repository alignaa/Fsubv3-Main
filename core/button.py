import config

from pyrogram import enums
from pyrogram.types import InlineKeyboardButton

chat_info_cache = {}


async def get_chat_info(client, chat_id):
    if chat_id in chat_info_cache:
        return chat_info_cache[chat_id]
    chat_info = await client.get_chat(chat_id)
    chat_info_cache[chat_id] = chat_info
    return chat_info


async def start_button(client):
    if not config.FORCE_SUB_:
        buttons = [
            [
                InlineKeyboardButton(text="Bantuan", callback_data="help"),
                InlineKeyboardButton(text="Tutup", callback_data="close"),
            ],
        ]
        return buttons

    dynamic_button = []
    current_row = []
    for key in config.FORCE_SUB_.keys():
        chat_id = config.FORCE_SUB_[key]
        chat_info = await get_chat_info(client, chat_id)
        chat_type = chat_info.type
        button_name = "Channel" if chat_type == enums.ChatType.CHANNEL else "Group"
        current_row.append(InlineKeyboardButton(text=f"{button_name}", url=getattr(client, f'invitelink{key}')))
        if len(current_row) == config.BUTTON_ROW:
            dynamic_button.append(current_row)
            current_row = []

    if current_row:
        dynamic_button.append(current_row)

    buttons = [
        [
            InlineKeyboardButton(text="Bantuan", callback_data="help"),
        ],
    ] + dynamic_button + [
        [InlineKeyboardButton(text="Tutup", callback_data="close")],
    ]
    return buttons


async def fsub_button(client, message):
    if config.FORCE_SUB_:
        dynamic_button = []
        current_row = []
        for key in config.FORCE_SUB_.keys():
            chat_id = config.FORCE_SUB_[key]
            chat_info = await get_chat_info(client, chat_id)
            chat_type = chat_info.type
            button_name = "Channel" if chat_type == enums.ChatType.CHANNEL else "Group"
            current_row.append(InlineKeyboardButton(text=f"{button_name}", url=getattr(client, f'invitelink{key}')))
            if len(current_row) == config.BUTTON_ROW:
                dynamic_button.append(current_row)
                current_row = []

        if current_row:
            dynamic_button.append(current_row)

        try:
            dynamic_button.append([
                InlineKeyboardButton(
                    text="Coba Lagi",
                    url=f"https://t.me/{client.username}?start={message.command[1]}",
                )
            ])
        except IndexError:
            pass

        return dynamic_button
