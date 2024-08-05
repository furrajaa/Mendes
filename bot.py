import config, sys, os, requests

from plugins import Database
from pyrogram import Client, enums
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats

data = []

class Bot(Client):
    def __init__(self):
        super().__init__(
            'alterbase_bot',
            api_id=config.api_id,
            api_hash=config.api_hash,
            plugins={
                "root": "plugins"
            },
            bot_token=config.bot_token
        )
    
    async def start(self):
        await super().start()
        bot_me = await self.get_me()

        db = Database(bot_me.id)
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/Mac
            os.system('clear')
        
        if not await db.cek_user_didatabase():
            print('[!] Menambahkan data bot ke database...')
            await db.tambah_databot()
        print("[!] Database telah ready")
        print(f"[!] Link Database Kamu : {config.db_url}")
        print("================")

        channels = [config.channel_1, config.channel_2, config.channel_log]
        for idx, channel in enumerate(channels, 1):
            if channel:
                try:
                    await self.export_chat_invite_link(channel)
                except Exception as e:
                    print(f'Harap periksa kembali ID [ {channel} ] pada channel {idx}')
                    print(f'Error: {str(e)}')
                    print('Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                    print('-> Bot terpaksa dihentikan')
                    sys.exit()
        
        self.username = bot_me.username
        self.id_bot = bot_me.id
        data.append(self.id_bot)
        await self.set_bot_commands([
            BotCommand('status', '🍃 check status'), 
            BotCommand('talent', '👙 talent konten / vcs'),
            BotCommand('daddysugar', '👔 daddy sugar trusted'), 
            BotCommand('moansgirl', '🧘‍♀️ moans girl'),
            BotCommand('moansboy', '🧘 moans boy'), 
            BotCommand('gfrent', '🤵 girl friend rent'),
            BotCommand('bfrent', '🤵 boy friend rent')
        ], BotCommandScopeAllPrivateChats())

        print('BOT TELAH AKTIF')
    
    async def stop(self):
        await super().stop()
        print('BOT BERHASIL DIHENTIKAN')
    
    async def kirim_pesan(self, x: str):
        db = Database(config.id_admin).get_pelanggan()
        pesan = f'<b>TOTAL USER ( {db.total_pelanggan} ) PENGGUNA 📊</b>\n'
        pesan += f'➜ <i>Total user yang mengirim menfess hari ini adalah {x}/{db.total_pelanggan} user</i>\n'
        pesan += '➜ <i>Berhasil direset menjadi 0 menfess</i>'
        url = f'https://api.telegram.org/bot{config.bot_token}'
        try:
            response = requests.get(f'{url}/sendMessage', params={
                'chat_id': config.channel_log,
                'text': pesan,
                'parse_mode': 'HTML'
            }).json()
            message_id = response['result']['message_id']
            requests.post(f'{url}/pinChatMessage', params={
                'chat_id': config.channel_log,
                'message_id': message_id
            })
            requests.post(f'{url}/deleteMessage', params={
                'chat_id': config.channel_log,
                'message_id': message_id + 1
            })
        except requests.RequestException as e:
            print(f'Error saat mengirim pesan: {str(e)}')
