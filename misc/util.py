import asyncio, json, os
from aiogram.types import Message
from datetime import datetime
from misc import DEFAULT_TZ, BASE_DIR
from pathlib import Path


async def loading_message(message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    
    msg = await message.answer("Loading...")

    return msg


async def reminder_loop(bot, path=Path(BASE_DIR, "misc", "jokes_util", "reminders.json")):
    while True:
        # гарантируем наличие файла
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"one": [], "daily": []}, f, ensure_ascii=False, indent=4)

        # читаем
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        now = datetime.now(DEFAULT_TZ)
        changed = False

        # --- разовые напоминания ("one") ---
        # отправляем один раз, если дата уже наступила и last_action ещё нет
        for item in data.get("one", []):
            try:
                due = datetime.fromisoformat(item["date"])
            except Exception:
                continue
            last = item.get("last_action")
            if last is None and due <= now:
                await bot.send_message(item["tg_id"], item["text"])
                item["last_action"] = now.isoformat()
                changed = True

        # --- ежедневные ("daily") ---
        # отправляем сегодня один раз после наступления времени HH:MM,
        # если last_action не сегодня
        for item in data.get("daily", []):
            try:
                t = datetime.fromisoformat(item["date"]).timetz()  # берём только время (и tz)
            except Exception:
                continue

            scheduled_today = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
            last = item.get("last_action")
            sent_today = False
            if last:
                try:
                    last_dt = datetime.fromisoformat(last).astimezone(DEFAULT_TZ)
                    sent_today = (last_dt.date() == now.date())
                except Exception:
                    sent_today = False

            if not sent_today and now >= scheduled_today:
                await bot.send_message(item["tg_id"], item["text"])
                item["last_action"] = now.isoformat()
                changed = True

        # сохраняем, если что-то поменяли
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        await asyncio.sleep(60)
