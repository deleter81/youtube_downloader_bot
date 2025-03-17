from aiogram import types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import re

# Список каналов для проверки подписки
CHANNELS = ["@deleter81"]

# Логирование
logging.basicConfig(level=logging.INFO)

# Функция для экранирования символов в MarkdownV2
def escape_markdown(text):
    escape_chars = r'_*\[\]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# Функция проверки подписки
async def check_subscriptions(user_id: int, bot: Bot):
    results = []
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['member', 'administrator', 'creator']:
                results.append(True)
            else:
                results.append(False)
        except Exception as e:
            logging.error(f"Ошибка при проверке подписки на {channel}: {e}")
            results.append(False)

    return all(results)

# Формируем текст с запросом на подписку
def get_subscription_message():
    text = "❌ *Пожалуйста, подпишитесь на следующие каналы, чтобы получить доступ:*\\n\\n"
    text += "\\n".join([
        f"➡️ [{escape_markdown(channel)}](https://t.me/{escape_markdown(channel.replace('@', ''))})"
        for channel in CHANNELS
    ])
    return text

# Создаём inline-кнопку для проверки подписки
def get_check_subscription_button():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_subscription")]
    ])
    return markup