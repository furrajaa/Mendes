import config
import re

from pyrogram import Client, enums, types
from plugins import Database


async def tambah_admin_handler(client: Client, msg: types.Message):
    usage_text = (
        "<b>Cara penggunaan tambah admin</b>\n\n"
        "<code>/admin id_user</code>\n\nContoh :\n"
        "<code>/admin 121212021</code>"
    )

    match = re.search(r"^/admin\s+(\d+)$", msg.text)
    if not match:
        return await msg.reply_text(text=usage_text, quote=True, parse_mode=enums.ParseMode.HTML)

    target_id = int(match.group(1))
    db = Database(target_id)

    if target_id in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target_id}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan user admin",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target_id}'>user</a> tidak terdaftar di database</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    status = {
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    }

    member = db.get_data_pelanggan()
    if member.status in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={target_id}'>user</a> adalah seorang {member.status.upper()}</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    try:
        await client.send_message(
            target_id,
            text=f"<i>Kamu telah menjadi admin bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.update_admin(target_id, client.id_bot)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={target_id}'>User</a> <i>berhasil menjadi admin bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )


async def hapus_admin_handler(client: Client, msg: types.Message):
    usage_text = (
        "<b>Cara penggunaan mencabut status admin</b>\n\n"
        "<code>/unadmin id_user</code>\n\nContoh :\n"
        "<code>/unadmin 121212021</code>"
    )

    match = re.search(r"^/unadmin\s+(\d+)$", msg.text)
    if not match:
        return await msg.reply_text(text=usage_text, quote=True, parse_mode=enums.ParseMode.HTML)

    target_id = int(match.group(1))
    db = Database(target_id)

    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target_id}'>user</a> tidak terdaftar di database</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    status = {
        'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    }

    member = db.get_data_pelanggan()
    if member.status in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={target_id}'>user</a> adalah seorang {member.status.upper()}</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    if member.status != 'admin':
        return await msg.reply_text(
            text=f"<i><a href='tg://openmessage?user_id={target_id}'>User</a> bukan seorang admin</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    try:
        await client.send_message(
            target_id,
            text=f"<i>Sayangnya owner telah mencabut jabatanmu sebagai admin</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.hapus_admin(target_id, client.id_bot)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={target_id}'>User</a> <i>berhasil diturunkan menjadi member</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
