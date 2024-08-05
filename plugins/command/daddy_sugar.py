import config
import re

from pyrogram import Client, enums, types
from plugins import Database, Helper

async def daddy_sugar_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)
    daddy_sugar = db.get_data_bot(client.id_bot).daddy_sugar
    
    if not daddy_sugar:
        return await msg.reply('<b>Saat ini tidak ada daddy sugar yang tersedia.</b>', True, enums.ParseMode.HTML)
    
    # Sorting daddy_sugar based on rating in descending order
    sorted_daddy_sugar = sorted(
        ((uid, data['rate']) for uid, data in daddy_sugar.items() if data['rate'] >= 0),
        key=lambda x: x[1],
        reverse=True
    )

    pesan = "<b>Daftar Daddy Sugar Trusted</b>\n\nNo — Daddy Sugar — Rating\n"
    for index, (uid, rate) in enumerate(sorted_daddy_sugar[:config.batas_daddy_sugar], start=1):
        username = daddy_sugar[uid]['username']
        pesan += f"<b>{index}.</b> {username} ➜ {rate} 🥂\n"
    
    pesan += "\nMenampilkan Real Daddy Sugar yang trusted membiayai wanita-wanita di FWB."
    await msg.reply(pesan, True, enums.ParseMode.HTML)

async def tambah_sugar_daddy_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    command_pattern = r"^/addsugar\s*(\d+)?$"
    
    if not re.match(command_pattern, msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Daddy Sugar</b>\n\n<code>/addsugar id_user</code>\n\nContoh:\n<code>/addsugar 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    target = re.search(command_pattern, msg.text or msg.caption).group(1)
    
    if not target:
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Daddy Sugar</b>\n\n<code>/addsugar id_user</code>\n\nContoh:\n<code>/addsugar 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    db = Database(int(target))
    
    if target in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan Daddy Sugar",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target}'>User</a> tidak terdaftar di database</i>",
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
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={target}'>User</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi daddy sugar</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    try:
        a = await client.get_chat(target)
        nama = await helper.escapeHTML(f'{a.first_name} {a.last_name}' if a.last_name else a.first_name)
        await client.send_message(
            int(target),
            text=f"<i>Kamu telah menjadi daddy sugar</i>\n└Diangkat oleh: <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.tambah_sugar_daddy(int(target), client.id_bot, nama)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={target}'>User</a> <i>berhasil menjadi daddy sugar</i>\n└Diangkat oleh: <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
