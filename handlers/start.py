import re
import os
from aiogram import types, Router, F, Bot
from aiogram.types import FSInputFile
from aiogram.filters import Command
from handlers.download import download_video
from utils.check_subscription import (
    check_subscriptions,
    get_subscription_message,
    get_check_subscription_button,
    escape_markdown
)

router = Router()

# Регулярное выражение для ссылки на YouTube
YOUTUBE_REGEX = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+')


@router.message(Command("start"))
async def start_command(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    is_subscribed = await check_subscriptions(user_id, bot)

    if not is_subscribed:
        text = get_subscription_message()
        await message.answer(
            text,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
            reply_markup=get_check_subscription_button()
        )
        return

    await message.answer(escape_markdown("✅ Добро пожаловать! Отправьте ссылку на видео YouTube для скачивания."))


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    is_subscribed = await check_subscriptions(user_id, bot)

    if is_subscribed:
        await callback.message.edit_text(
            escape_markdown("✅ Вы успешно подписаны! Теперь вы можете скачивать видео.\n\n"
                            "🔗 Отправьте ссылку на видео YouTube для скачивания:"),
            parse_mode="MarkdownV2"
        )
    else:
        text = get_subscription_message()
        await callback.message.edit_text(
            text,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
            reply_markup=get_check_subscription_button()
        )


@router.message(F.text)
async def handle_message(message: types.Message, bot: Bot):
    url = message.text.strip()
    user_id = message.from_user.id

    is_subscribed = await check_subscriptions(user_id, bot)
    if not is_subscribed:
        text = get_subscription_message()
        await message.answer(
            text,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
            reply_markup=get_check_subscription_button()
        )
        return

    if YOUTUBE_REGEX.match(url):
        await message.answer(escape_markdown(f"🔗 Получена ссылка: {url}\n\n⏳ Начинаю скачивание видео..."))

        file_path = download_video(url)

        if file_path:
            try:
                file = FSInputFile(file_path)
                await message.answer("✅ Скачивание завершено! Отправляю файл...")
                await message.answer_video(file)
                os.remove(file_path)  # Удаляем файл после отправки
            except Exception as e:
                await message.answer(escape_markdown(f"❌ Ошибка при отправке видео: {e}"))
        else:
            await message.answer(escape_markdown("❌ Не удалось скачать видео. Попробуйте другую ссылку."))
    else:
        await message.answer(escape_markdown("❌ Введите корректную ссылку на YouTube."))


def register_start_handler(dp):
    dp.include_router(router)