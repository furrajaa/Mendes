import config
import re
from pyrogram import Client, enums, types
from plugins import Database, Helper

async def gf_rent_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)
    gf_rent = db.get_data_bot(client.id_bot).gfrent
    
    if not gf_rent:
        return await msg.reply('<b>Saat ini tidak ada GF rent yang tersedia.</b>', True, enums.ParseMode.HTML)
    
    # Sorting gf_rent based on rating in descending order
    sorted_gf_rent = sorted(
        ((uid, data['rate']) for uid, data in gf_rent.items() if data['rate'] >= 0),
        key=lambda x: x[1],
        reverse=True
    )

    pesan = "<b>Daftar GF Rent Trusted</b>\n\nNo — GF Rent — Rating\n"
    
    for index, (uid, rate) in enumerate(sorted_gf_rent[:config.batas_gfrent], start=1):
        username = gf_rent[uid]['username']
        pesan += f"<b>{index}.</b> {username} ➜ {rate} 🌸\n"
    
    pesan += "\nMenampilkan Real GF Rent FWB."
    await msg.reply(pesan, True, enums.ParseMode.HTML)

async def tambah_gf_rent_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    command_pattern = r"^/addgf\s*(\d+)?$"
    
    if not re.match(command_pattern, msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah GF Rent</b>\n\n<code>/addgf id_user</code>\n\nContoh:\n<code>/addgf 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    target = re.search(command_pattern, msg.text or msg.caption).group(1)
    
    if not target:
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah GF Rent</b>\n\n<code>/addgf id_user</code>\n\nContoh:\n<code>/addgf 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    db = Database(int(target))
    
    if target in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={target}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan Girlfriend Rent",
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
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={target}'>User</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi Girlfriend Rent</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    try:
        chat = await client.get_chat(target)
        nama = await helper.escapeHTML(f'{chat.first_name} {chat.last_name}' if chat.last_name else chat.first_name)
        await client.send_message(
            int(target),
            text=f"<i>Kamu telah menjadi Girlfriend Rent</i>\n└Diangkat oleh: <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.tambah_gf_rent(int(target), client.id_bot, nama)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={target}'>User</a> <i>berhasil menjadi GF Rent</i>\n└Diangkat oleh: <a href='tg://openmessage?user_id={config.id_admin}'>Admin</a>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
