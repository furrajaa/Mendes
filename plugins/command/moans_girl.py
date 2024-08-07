import config
import re

from pyrogram import Client, enums, types
from plugins import Database, Helper

async def moans_girl_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)
    moans_girl = db.get_data_bot(client.id_bot).moansgirl
    if not moans_girl:
        return await msg.reply('<b>Saat ini tidak ada Moans girl yang tersedia.</b>', True, enums.ParseMode.HTML)

    top_rate = []  # total rate moans_girl
    top_id = []  # id moans_girl

    for uid, data in moans_girl.items():
        rate = data['rate']
        if rate >= 0:
            top_rate.append(rate)
            top_id.append(uid)

    top_rate.sort(reverse=True)
    pesan = "<b>Daftar Moans girl trusted</b>\n\n" + "No — Moans girl — Rating\n"

    index = 1
    for rate in top_rate:
        if index > config.batas_moansgirl:
            break
        for uid in top_id:
            if moans_girl[uid]['rate'] == rate:
                pesan += f"<b>{index}.</b> {moans_girl[uid]['username']} ➜ {rate} 🍬\n"
                top_id.remove(uid)
                index += 1

    pesan += "\nMenampilkan Real talent moans girl fwb"
    await msg.reply(pesan, True, enums.ParseMode.HTML)

async def tambah_moans_girl_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    command_pattern = r"^[\/]addgirl(?:\s+|[\n])(\d+)?$"

    match = re.search(command_pattern, msg.text or msg.caption)
    if not match or not match.group(1):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Moans girl</b>\n\n<code>/addgirl id_user</code>\n\nContoh :\n<code>/addgirl 121212021</code>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    target = match.group(1)
    db = Database(int(target))

    if target in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan Moans girl", 
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
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={target}'>user</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi Moans girl</i>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    try:
        user = await client.get_chat(target)
        nama = await helper.escapeHTML(
            f'{user.first_name} {user.last_name}' if user.last_name else user.first_name
        )
        await client.send_message(
            int(target),
            text=f"<i>Kamu telah menjadi Moans girl</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.tambah_moans_girl(int(target), client.id_bot, nama)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={target}'>User</a> <i>berhasil menjadi Moans girl</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
