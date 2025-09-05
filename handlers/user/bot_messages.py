import re
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from keyboards import matrix_paginatios_kb
from misc import MatrixOfDestiny, loading_message, Paginations
from misc.jokes_util.util import get_matrix_data, chakra_matrix_html, svg_b64_to_png_bytes

router = Router()


@router.message(F.text, MatrixOfDestiny.Personal)
async def check_name_date(message: Message, state: FSMContext, bot: Bot):
    name_date_re = re.compile(r"^([A-Za-zА-Яа-яІіЇїЄєҐґ]+)\s+(\d{2}\.\d{2}\.\d{4})$")

    text = message.text.strip()

    m = name_date_re.match(text)
    if not m:
        await message.answer("❌ Формат неправильний. Введи так: <b>Ім'я дд.мм.рррр</b>", parse_mode="HTML")
        return

    msg = await loading_message(message)
    try:
        name, date_str = m.groups()

        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            await message.answer("❌ Невірна дата. Перевір число та місяць.")
            return

        state_data = await state.get_data()

        body = {"date1": date_str, "name1": name, "gender": state_data["gender"]}

        data = await get_matrix_data(body)

        text = await chakra_matrix_html(data)

        svg_bytes = await svg_b64_to_png_bytes(data["svg"])
        photo = BufferedInputFile(svg_bytes, filename="image.png")

        await state.update_data(photo=photo)
        await state.update_data(text=text)
        await state.update_data(data=data)

        await state.set_state(Paginations.PaginationPersonalMatrix)

        msg_id = state_data["msg_id"]
        await bot.delete_message(chat_id=message.from_user.id, message_id=msg_id)
        await msg.delete()
        await message.answer_photo(photo=photo, reply_markup=await matrix_paginatios_kb(0, 2))
    except Exception as e:
        print("Error in FoodRecipes_page_call:", e)
        await message.answer("Вибач, сталася помилка. Спробуй ще раз.")

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