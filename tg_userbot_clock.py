"""
Юзербот для Telegram: показывает текущее время в имени профиля.
Формат имени: "Ник | ЧЧ:ММ" (часовой пояс UTC+3)

УСТАНОВКА:
    pip install telethon

НАСТРОЙКА (обязательно перед запуском):
    1. Зайди на https://my.telegram.org -> "API development tools"
    2. Создай приложение и получи api_id и api_hash
    3. Впиши их ниже в переменные API_ID и API_HASH
    4. Впиши свой базовый ник в BASE_NICK

ЗАПУСК:
    python tg_userbot_clock.py

    При первом запуске Telethon попросит ввести номер телефона и код
    из Telegram (и пароль 2FA, если он у тебя включён). После этого
    создастся файл сессии (*.session), и повторный вход не понадобится.
"""

import asyncio
from datetime import datetime, timezone, timedelta

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.account import UpdateProfileRequest

# ==================== НАСТРОЙКИ ====================
API_ID = 12149162                 # <-- твой api_id с my.telegram.org
API_HASH = "c2ea39e521d6690d6ab1524583575d37" # <-- твой api_hash с my.telegram.org
BASE_NICK = "o_x86"          # <-- что будет стоять перед временем
UPDATE_INTERVAL = 60            # секунд между проверками (не ставь меньше 60,
                                 # чтобы не словить FloodWait от Telegram)
SESSION_NAME = "clock_userbot"  # имя файла сессии
# =====================================================

TZ = timezone(timedelta(hours=3))  # UTC+3

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def update_name_loop():
    last_name = None
    while True:
        now_str = datetime.now(TZ).strftime("%H:%M")
        new_name = f"{BASE_NICK} | {now_str}"

        if new_name != last_name:
            try:
                await client(UpdateProfileRequest(first_name=new_name))
                last_name = new_name
                print(f"[{now_str}] Имя обновлено: {new_name}")
            except FloodWaitError as e:
                print(f"FloodWait: жду {e.seconds} сек.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Ошибка при обновлении имени: {e}")

        await asyncio.sleep(UPDATE_INTERVAL)


async def main():
    await client.start()
    me = await client.get_me()
    print(f"Юзербот запущен от имени: {me.first_name} (id={me.id})")
    print(f"Обновляю имя каждые {UPDATE_INTERVAL} сек.")
    await update_name_loop()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
