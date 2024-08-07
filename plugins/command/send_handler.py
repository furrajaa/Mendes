import config
import re

from pyrogram import Client, types, enums
from plugins import Database, Helper

async def send_with_pic_handler(client: Client, msg: types.Message, key: str, hastag: list):
    db = Database(msg.from_user.id)
    helper = Helper(client, msg)
    user = db.get_data_pelanggan()
    
    if msg.from_user.is_bot:
        return await msg.reply('Anda tidak diizinkan mengirimkan pesan sebagai bot.', quote=True)
    
    if msg.text or msg.photo or msg.video or msg.voice:
        menfess = user.menfess
        all_menfess = user.all_menfess
        coin = user.coin

        if menfess >= config.batas_kirim and user.status in ['member', 'talent']:
            if coin >= config.biaya_kirim:
                coin -= config.biaya_kirim
            else:
                return await msg.reply(
                    f'🙅🏻‍♀️ Post gagal terkirim. Kamu hari ini telah mengirim {menfess}/{config.batas_kirim} kali. Coin mu kurang untuk mengirim menfess di luar batas harian. Kamu dapat mengirim menfess kembali pada hari esok. Waktu reset jam 1 pagi.\n\nInfo: Topup Coin Hanya ke @kucingssbaikss',
                    quote=True
                )
        
        picture = None
        if key == hastag[0]:
            picture = config.pic_girl
        elif key == hastag[1]:
            picture = config.pic_boy
            
        if user.status == 'talent':
            picture = config.pic_talentgirl
        elif user.status == 'owner':
            picture = config.pic_owner
        elif user.status == 'admin':
            picture = config.pic_admingirl if key == hastag[0] else config.pic_adminboy
        elif user.status == 'daddy sugar':
            picture = config.pic_daddysugar
        elif user.status == 'boyfriend rent':
            picture = config.pic_bfrent
        elif user.status == 'moans boy':
            picture = config.pic_moansboy
        
        link = await get_link()
        caption = msg.text or msg.caption
        entities = msg.entities or msg.caption_entities

        kirim = await client.send_photo(config.channel_1, picture, caption, caption_entities=entities)
        await helper.send_to_channel_log(type="log_channel", link=link + str(kirim.id))
        await db.update_menfess(coin, menfess, all_menfess)
        await msg.reply(
            f"Pesan telah berhasil terkirim. Hari ini kamu telah mengirim menfess sebanyak {menfess + 1}/{config.batas_kirim}. Kamu dapat mengirim menfess sebanyak {config.batas_kirim} kali dalam sehari.\n\nWaktu reset setiap jam 1 pagi.\n<a href='{link + str(kirim.id)}'>Check pesan kamu</a>.\n\nInfo: Topup Coin Hanya ke @kucingssbaikss"
        )
    else:
        await msg.reply('Media yang didukung: photo, video, dan voice.')

async def send_menfess_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    db = Database(msg.from_user.id)
    db_user = db.get_data_pelanggan()
    db_bot = db.get_data_bot(client.id_bot).kirimchannel
    
    if msg.from_user.is_bot:
        return await msg.reply('Anda tidak diizinkan mengirimkan pesan sebagai bot.', quote=True)
    
    if msg.text or msg.photo or msg.video or msg.voice:
        if msg.photo and not db_bot.photo and db_user.status in ['member', 'talent']:
            return await msg.reply('Tidak bisa mengirim photo, karena sedang dinonaktifkan oleh admin.', True)
        elif msg.video and not db_bot.video and db_user.status in ['member', 'talent']:
            return await msg.reply('Tidak bisa mengirim video, karena sedang dinonaktifkan oleh admin.', True)
        elif msg.voice and not db_bot.voice and db_user.status in ['member', 'talent']:
            return await msg.reply('Tidak bisa mengirim voice, karena sedang dinonaktifkan oleh admin.', True)

        menfess = db_user.menfess
        all_menfess = db_user.all_menfess
        coin = db_user.coin

        if menfess >= config.batas_kirim and db_user.status in ['member', 'talent']:
            if coin >= config.biaya_kirim:
                coin -= config.biaya_kirim
            else:
                return await msg.reply(
                    f'🙅🏻‍♀️ Post gagal terkirim. Kamu hari ini telah mengirim {menfess}/{config.batas_kirim} kali. Coin mu kurang untuk mengirim menfess di luar batas harian. Kamu dapat mengirim menfess kembali pada hari esok. Waktu reset jam 1 pagi.\n\nInfo: Topup Coin Hanya ke @kucingssbaikss',
                    quote=True
                )

        link = await get_link()
        kirim = await client.copy_message(config.channel_1, msg.from_user.id, msg.id)
        await helper.send_to_channel_log(type="log_channel", link=link + str(kirim.id))
        await db.update_menfess(coin, menfess, all_menfess)
        await msg.reply(
            f"Pesan telah berhasil terkirim. Hari ini kamu telah mengirim menfess sebanyak {menfess + 1}/{config.batas_kirim}. Kamu dapat mengirim menfess sebanyak {config.batas_kirim} kali dalam sehari.\n\nWaktu reset setiap jam 1 pagi.\n<a href='{link + str(kirim.id)}'>Check pesan kamu</a>."
        )
    else:
        await msg.reply('Media yang didukung: photo, video, dan voice.')

async def get_link():
    anu = str(config.channel_1).split('-100')[1]
    return f"https://t.me/c/{anu}/"

async def transfer_coin_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]tf_coin(\s|\n)*$", msg.text or msg.caption):
        err = "<i>Perintah salah /tf_coin [jumlah_coin]</i>" if msg.reply_to_message else "<i>Perintah salah /tf_coin [id_user] [jumlah_coin]</i>"
        return await msg.reply(err, True)
    
    helper = Helper(client, msg)
    
    if re.search(r"^[\/]tf_coin\s(\d+)(\s(\d+))?", msg.text or msg.caption):
        match = re.search(r"^[\/]tf_coin\s(\d+)(\s(\d+))$", msg.text or msg.caption)
        if match:
            target = match[1]
            coin = match[3]
        else:
            match = re.search(r"^[\/]tf_coin\s(\d+)$", msg.text or msg.caption)
            if not msg.reply_to_message:
                return await msg.reply('Harap reply ke pesan user yang akan menerima coin.', True)
            if msg.reply_to_message.from_user.is_bot:
                return await msg.reply('🤖 Bot tidak dapat menerima transfer coin.', True)
            elif msg.reply_to_message.sender_chat:
                return await msg.reply('Channel tidak dapat menerima transfer coin.', True)
            target = msg.reply_to_message.from_user.id
            coin = match[1]
        
        if msg.from_user.id == int(target):
            return await msg.reply('<i>Tidak dapat transfer coin untuk diri sendiri.</i>', True)

        user_db = Database(msg.from_user.id)
        user_data = user_db.get_data_pelanggan()
        my_coin = user_data.coin
        if my_coin < int(coin):
            return await msg.reply(f'<i>Coin kamu ({my_coin}) tidak cukup untuk transfer.</i>', True)
        
        target_db = Database(int(target))
        if not await target_db.cek_user_didatabase():
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={target}'>User</a> tidak terdaftar di database.</i>", 
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        
        target_data = target_db.get_data_pelanggan()
        updated_my_coin = my_coin - int(coin)
        updated_target_coin = target_data.coin + int(coin)
        sender_name = "Admin" if user_data.status in ['owner', 'admin'] else msg.from_user.first_name
        sender_name = await helper.escapeHTML(sender_name)
        
        try:
            await client.send_message(
                target,
                f"Coin berhasil ditambahkan senilai {coin} coin. Cek /status\n└Oleh <a href='tg://user?id={msg.from_user.id}'>{sender_name}</a>"
            )
            await user_db.transfer_coin(updated_my_coin, updated_target_coin, target_data.coin_full, int(target))
            await msg.reply(f'<i>Berhasil transfer coin sebesar {coin} coin💰</i>', True)
        except Exception as e:
            return await msg.reply_text(
                text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot.</i>\n\n{e}", 
                quote=True,
                parse_mode=enums.ParseMode.HTML
        )
