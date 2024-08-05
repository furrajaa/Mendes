import config
import re

from pyrogram import Client, enums, types
from plugins import Database, Helper

async def bf_rent_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)
    bf_rent = db.get_data_bot(client.id_bot).bfrent
    
    if not bf_rent:
        return await msg.reply('<b>Saat ini tidak ada Bf rent yang tersedia.</b>', True, enums.ParseMode.HTML)
    
    top_rate = [(bf_rent[uid]['rate'], uid) for uid in bf_rent if bf_rent[uid]['rate'] >= 0]
    top_rate.sort(reverse=True)

    pesan = "<b>Daftar Bf rent trusted</b>\n\n" + "No — Bf rent — Rating\n"
    index = 1
    
    for rate, uid in top_rate:
        if index > config.batas_bfrent:
            break
        username = bf_rent[uid]['username']
        pesan += f"<b> {index}.</b> {username} ➜ {rate} 👓\n"
        index += 1

    pesan += f"\nmenampilkan Real BF Rent fwb"
    await msg.reply(pesan, True, enums.ParseMode.HTML)

async def tambah_bf_rent_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    
    if re.search(r"^[\/]addbf(\s|\n)*$", msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Bf rent</b>\n\n<code>/addbf id_user</code>\n\nContoh :\n<code>/addbf 121212021</code>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    match = re.search(r"^[\/]addbf(\s|\n)*(\d+)$", msg.text or msg.caption)
    if not match:
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Bf rent</b>\n\n<code>/addbf id_user</code>\n\nContoh :\n<code>/addbf 121212021</code>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    target = match[2]
    db = Database(int(target))
    
    if target in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan boyfriend rent", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target}'>user</a> tidak terdaftar di database</i>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    status = [
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    ]
    member = db.get_data_pelanggan()
    
    if member.status in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={target}'>user</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi Boyfriend rent</i>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    try:
        a = await client.get_chat(target)
        nama = await helper.escapeHTML(
            f'{a.first_name} {a.last_name}' if a.last_name else a.first_name
        )
        await client.send_message(
            int(target),
            text=f"<i>Kamu telah menjadi Boyfriend rent</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.tambah_bf_rent(int(target), client.id_bot, nama)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={target}'>User</a> <i>berhasil menjadi Bf rent</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
