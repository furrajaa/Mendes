import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import Bot, data, Database

async def reset_menfess():
    db = Database(data[0])
    x = await db.reset_menfess()
    bot = Bot()  
    await bot.kirim_pesan(x=str(x))
    print('BOT BERHASIL DIRESET')

async def main():
    bot = Bot()
    scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
    scheduler.add_job(reset_menfess, trigger="cron", hour=1, minute=0)
    scheduler.start()
    
    await bot.start()
    
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
