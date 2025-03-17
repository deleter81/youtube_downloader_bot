import asyncio
from aiogram import Bot, Dispatcher
from data.config import TOKEN
from handlers.start import register_start_handler
from handlers.download import register_download_handler

async def main():
    # Создаём экземпляр бота
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрируем обработчики
    register_start_handler(dp)
    register_download_handler(dp)

    try:
        print("🚀 Бот запущен и ожидает команды...")
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию при завершении работы
        await bot.session.close()
        print("🛑 Бот остановлен.")

if __name__ == "__main__":
    asyncio.run(main())