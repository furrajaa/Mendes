from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from pyrogram import idle

from bot import Bot, Database, data


async def reset_menfess(bot):
    db = Database(data[0])
    try:
        x = await db.reset_menfess()
        await bot.kirim_pesan(x=str(x))
        print("BOT BERHASIL DIRESET")
    except Exception as e:
        print(f"Error during reset: {str(e)}")


async def main():
    bot = Bot()
    
    scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
    scheduler.add_job(reset_menfess, args=[bot], trigger="cron", hour=1, minute=0)
    scheduler.start()
    
    await bot.start()
    print(f"{bot.username} BOT TELAH AKTIF")
    
    try:
        await idle()  # Pyrogram idle to keep the bot running
    finally:
        scheduler.shutdown()
        await bot.stop()
        print("BOT BERHASIL DIHENTIKAN")

if __name__ == "__main__":
    asyncio.run(main())
