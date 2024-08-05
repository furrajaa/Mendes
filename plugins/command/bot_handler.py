import re
import config
from pyrogram import Client, enums, types
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from plugins import Database

async def send_notification(client: Client, text: str):
    """Function to send notification to config.channel_1"""
    try:
        await client.send_message(config.channel_1, text)
    except Exception as e:
        print("Error sending notification:", str(e))

async def bot_handler(client: Client, msg: Message):
    """Handle /bot command to activate or deactivate the bot"""
    match = re.match(r"^\/bot\s*(on|off)$", msg.text)
    if not match:
        return await msg.reply(
            "*Cara penggunaan command*\n\nEX : `/bot <on|off>`\nContoh : `/bot on`",
            quote=True, parse_mode=enums.ParseMode.MARKDOWN
        )
    
    status = match.group(1)
    my_db = Database(msg.from_user.id)
    db_bot = my_db.get_data_bot(client.id_bot)

    if status == 'on' and db_bot.bot_status:
        return await msg.reply(
            text='❌<i>Terjadi kesalahan, bot saat ini dalam kondisi aktif</i>',
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    elif status == 'off' and not db_bot.bot_status:
        return await msg.reply(
            text='❌<i>Terjadi kesalahan, bot saat ini dalam kondisi tidak aktif</i>',
            quote=True, parse_mode=enums.ParseMode.HTML
        )
    
    await my_db.bot_handler(status)
    status_text = "🔔 Bot telah diaktifkan." if status == 'on' else "🔔 Bot telah dinonaktifkan."
    await send_notification(client, status_text)
    status_message = 'Saat ini status bot telah <b>AKTIF</b> ✅' if status == 'on' else 'Saat ini status bot telah <b>TIDAK AKTIF</b> ❌'
    return await msg.reply(
        text=status_message, quote=True, parse_mode=enums.ParseMode.HTML
    )

async def setting_handler(client: Client, msg: types.Message):
    """Send bot settings to user with inline buttons to change settings"""
    db = Database(msg.from_user.id).get_data_bot(client.id_bot)
    
    def status_text(active: bool) -> str:
        return "AKTIF" if active else "TIDAK AKTIF"
    
    pesan = (
        "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
        + "______________________________\n\n"
        + f"📸 Foto = <b>{status_text(db.kirimchannel.photo)}</b>\n"
        + f"🎥 Video = <b>{status_text(db.kirimchannel.video)}</b>\n"
        + f"🎤 Voice = <b>{status_text(db.kirimchannel.voice)}</b>\n\n"
        + f'🔰Status bot: <b>{status_text(db.bot_status)}</b>'
    )

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('📸', callback_data='photo')],
        [InlineKeyboardButton('🎥', callback_data='video')],
        [InlineKeyboardButton('🎤', callback_data='voice')],
        [InlineKeyboardButton(status_text(db.bot_status), callback_data='status_bot')]
    ])
    
    await msg.reply(pesan, quote=True, parse_mode=enums.ParseMode.HTML, reply_markup=markup)

async def update_message(client: Client, msg: types.Message, db: Database):
    """Update message with current settings"""
    db_data = db.get_data_bot(client.id_bot)
    
    def status_text(active: bool) -> str:
        return "AKTIF" if active else "TIDAK AKTIF"
    
    pesan = (
        "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
        + "______________________________\n\n"
        + f"📸 Foto = <b>{status_text(db_data.kirimchannel.photo)}</b>\n"
        + f"🎥 Video = <b>{status_text(db_data.kirimchannel.video)}</b>\n"
        + f"🎤 Voice = <b>{status_text(db_data.kirimchannel.voice)}</b>\n\n"
        + f'🔰Status bot: <b>{status_text(db_data.bot_status)}</b>'
    )

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('📸', callback_data='photo')],
        [InlineKeyboardButton('🎥', callback_data='video')],
        [InlineKeyboardButton('🎤', callback_data='voice')],
        [InlineKeyboardButton(status_text(db_data.bot_status), callback_data='status_bot')]
    ])
    
    await msg.edit(pesan, parse_mode=enums.ParseMode.HTML, reply_markup=markup)

async def handle_inline_query(client: Client, query: CallbackQuery, type_: str):
    """Handle inline queries for changing settings"""
    msg = query.message
    db = Database(query.from_user.id)
    current_status = msg.reply_markup.inline_keyboard[int(type_[-1])][0].text

    if current_status in ['✅', '❌']:
        handler_map = {
            'photo': db.photo_handler,
            'video': db.video_handler,
            'voice': db.voice_handler
        }
        await handler_map[type_](current_status, client.id_bot)
        
        await update_message(client, msg, db)

async def photo_handler_inline(client: Client, query: CallbackQuery):
    await handle_inline_query(client, query, 'photo')

async def video_handler_inline(client: Client, query: CallbackQuery):
    await handle_inline_query(client, query, 'video')

async def voice_handler_inline(client: Client, query: CallbackQuery):
    await handle_inline_query(client, query, 'voice')

async def status_handler_inline(client: Client, query: CallbackQuery):
    """Handle status button clicks"""
    msg = query.message
    db = Database(query.from_user.id)
    current_status = msg.reply_markup.inline_keyboard[3][0].text
    new_status = 'off' if current_status == 'AKTIF' else 'on'
    await db.bot_handler(new_status)
    await update_message(client, msg, db)
