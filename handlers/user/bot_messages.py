import re
from datetime import datetime, timedelta, timezone
from typing import List, Tuple

from aiogram import Router, F, Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from keyboards import personal_data_display_kb, compatibility_data_display_kb
from misc import MatrixOfDestiny, loading_message, T, Reminders, parse_reminder, DEFAULT_TZ
from misc.jokes_util.util import get_personal_matrix_data, svg_b64_to_png_bytes, get_compatibility_matrix_data

router = Router()


@router.message(F.text, MatrixOfDestiny.Personal)
async def personal_message(message: Message, state: FSMContext, bot: Bot):
    name_date_re = re.compile(r"^([A-Za-zА-Яа-яІіЇїЄєҐґ]+)\s+(\d{2}\.\d{2}\.\d{4})$")

    text = message.text.strip()

    m = name_date_re.match(text)
    if not m:
        await message.answer("❌ Формат неправильний. Введи так: <b>Ім'я дд.мм.рррр</b>", parse_mode="HTML")
        return

    msg = await loading_message(message)
    state_data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=state_data["msg_id"])

    try:
        name, date_str = m.groups()

        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            await message.answer("❌ Невірна дата. Перевір число та місяць.")
            return

        body = {"date1": date_str, "name1": name, "gender": state_data["gender"]}

        data = await get_personal_matrix_data(body)

        svg_bytes = await svg_b64_to_png_bytes(data["svg"])
        photo = BufferedInputFile(svg_bytes, filename="image.png")

        await state.update_data(photo=photo)
        await state.update_data(body=body)
        await state.update_data(position="photo")

        await state.set_state(MatrixOfDestiny.DataDisplay)

        await message.answer_photo(photo=photo, reply_markup=await personal_data_display_kb())
        await msg.delete()
    except Exception as e:
        print("Error in FoodRecipes_page_call:", e)
        await message.answer(T.ErrorMessage)


@router.message(F.text, MatrixOfDestiny.Compatibility)
async def compatibility_message(message: Message, state: FSMContext, bot: Bot):
    name_date_re = re.compile(
        r"^([A-Za-zА-Яа-яІіЇїЄєҐґ'’\- ]+?)\s+(\d{1,2}\.\d{1,2}\.\d{4})$"
    )

    text = (message.text or "").strip()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    if len(lines) != 2:
        await message.answer(
            "❌ Формат неправильний.\n"
            "Введи два рядки:\n"
            "<b>Віка 10.08.2007</b>\n"
            "<b>Олег 01.04.2006</b>",
            parse_mode="HTML",
        )
        return

    pairs: List[Tuple[str, str]] = []
    for idx, ln in enumerate(lines, start=1):
        m = name_date_re.match(ln)
        if not m:
            await message.answer(
                f"❌ Рядок {idx} має неправильний формат.\n"
                "Введи так: <b>Ім'я дд.мм.рррр</b>",
                parse_mode="HTML",
            )
            return

        name, date_str = m.groups()

        # Перевіряємо дату + нормалізуємо формат до 2 цифр дня/місяця
        try:
            dt = datetime.strptime(date_str, "%d.%m.%Y")
            date_str = dt.strftime("%d.%m.%Y")
        except ValueError:
            await message.answer(f"❌ Рядок {idx}: невірна дата. Перевір число та місяць.")
            return

        pairs.append((name.strip(), date_str))

    try:
        state_data = await state.get_data()
        await bot.delete_message(chat_id=message.from_user.id, message_id=state_data["message_id"])
        msg = await loading_message(message)

        body = {
            "date1": pairs[0][1],
            "name1": pairs[0][0],
            "date2": pairs[1][1],
            "name2": pairs[1][0]
        }

        data = await get_compatibility_matrix_data(body)
        print(body, data)
        svg_bytes = await svg_b64_to_png_bytes(data.get("svg"))
        photo = BufferedInputFile(svg_bytes, filename="image.png")

        await state.set_state(MatrixOfDestiny.DataDisplay)

        await state.update_data(photo=photo)
        await state.update_data(body=body)
        await state.update_data(position="photo")

        await message.answer_photo(photo=photo, reply_markup=await compatibility_data_display_kb())
        await msg.delete()
    except Exception as e:
        await message.answer(T.ErrorMessage)


def _next_daily_run(now: datetime, hh: int, mm: int) -> datetime:
    # Возвращает ближайший запуск сегодня/завтра с указанным временем (tz берём из now)
    target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target

def _fmt_when(dt: datetime, mode: str) -> str:
    if mode == "daily":
        return f"щодня о {dt:%H:%M} (перше спрацювання {dt:%d.%m.%Y})"
    return f"{dt:%d.%m.%Y о %H:%M}"


@router.message(F.text, Reminders.Setting)
async def reminders_message(message: Message, state: FSMContext):
    try:
        parsed = parse_reminder(message.text)
    except ValueError as e:
        await message.reply(
            "❌ " + str(e) + "\n\nПриклади:\n"
            "• Текст…\\n14:25  (щодня о 14:25)\n"
            "• Текст…\\n09.09 14:25  (9 вересня о 14:25)\n"
            "• Текст…\\n09.09.2025 14:25"
        )
        return  

    state_data = await state.get_data()
    mode =  state_data.get("type")

    now = message.date if message.date.tzinfo else datetime.now(timezone.utc)
    dt = parsed["date"]
    if dt.tzinfo is None:
        # приклеим ту же зону, что у now (чаще всего UTC)
        dt = dt.replace(tzinfo=now.tzinfo)
    if mode == "daily":
        # ежедневное: берём только время и считаем ближайшее срабатывание
        dt = _next_daily_run(now, dt.hour, dt.minute)
    else:
        # разовое: гарантируем будущее; если уже прошло — подсказка
        if dt <= now:
            await message.reply("❌ Дата/час уже минули. Укажіть майбутній момент.")
            return

    item = {
        "text": parsed["text"],
        "run_at": dt.isoformat(),        # хранить удобно в ISO
        "mode": mode,                    # "daily" | "one"
        "created_at": now.isoformat(),
    }
    await message.answer(
        "✅ Нагадування збережено.\n\n"
        f"<b>{parsed['text']}</b>\n{_fmt_when(dt, mode)}",
        parse_mode="HTML"
    )
    await state.clear()


# @router.message(F.photo)
# async def receive_photo(message: Message):
#     photo = message.photo[-1]  # Беремо останнє (найбільше за розміром) фото
#     photo_id = photo.file_id
#
#     print(f"Отримано photo_id: {photo_id}")
#
#     await message.answer(
#         f"🖼 Фото отримано!\nID цього фото:\n<code>{photo_id}</code>",
#         parse_mode="HTML"
#     )
#
#
#
# @router.message(F.video)
# async def receive_video(message: Message):
#     video = message.video
#     video_id = video.file_id
#
#     print(f"Отримано video_id: {video_id}")
#
#     await message.answer(
#         f"🎬 Відео отримано!\nID цього відео:\n<code>{video_id}</code>",
#         parse_mode="HTML"
#     )