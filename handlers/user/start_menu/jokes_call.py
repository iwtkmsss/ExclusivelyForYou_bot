import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards import (jokes_kb, good_mood_kb, tarological_kb, recipes_kb, reminder_kb, \
                       support_kb, games_kb, premium_recipes_kb, back_to_premium_recipes_kb, food_recipe_kb,
                       all_horoscope_kb, back_to_all_horoscope_kb, matrix_destiny_kb, back_to_m_d_personal_kb,
                       matrix_destiny_personal_kb, personal_data_display_kb, dd_personal_qualities_kb,
                       back_to_personal_qualities_kb, compatibility_data_display_kb)
from misc import get_random_premium_recipe, get_random_json_food, T, DEFAULT_PHOTO_FOR_RECIPE, Paginations, \
    loading_message, get_scraping_zodiac_sign, t_zodiac_signs, MatrixOfDestiny
from misc.jokes_util.util import chakra_matrix_html, get_personal_matrix_data, get_compatibility_matrix_data

router = Router()

@router.callback_query(F.data == "jokes")
async def jokes_call(callback_query: CallbackQuery):
    text = "JOKES TEXT"

    await callback_query.message.edit_text(text=text,
                                reply_markup=jokes_kb)


@router.callback_query(F.data == "good_mood")
async def good_mood_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "good_mood TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await good_mood_kb(user_id))


@router.callback_query(F.data == "tarological")
async def tarological_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "tarological TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await tarological_kb(user_id))


@router.callback_query(F.data == "recipes")
async def recipes_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "recipes TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await recipes_kb(user_id))


@router.callback_query(F.data == "reminder")
async def reminder_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "reminder TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await reminder_kb(user_id))


@router.callback_query(F.data == "support")
async def support_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "support TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await support_kb(user_id))


@router.callback_query(F.data == "games")
async def games_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "games TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await games_kb(user_id))


# ----- recipes_call ----- recipes_call ----- recipes_call ----- recipes_call ----- recipes_call -----

@router.callback_query(F.data == "food_recipe") # віддати рецепт їжі
async def food_recipe_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_id = callback_query.from_user.id
        msg = await loading_message(callback_query.message)
        recipe = await get_random_json_food("food_recipe.json")

        await state.set_state(Paginations.FoodRecipes)
        await state.update_data(data=recipe)

        text = T.FOOD_RECIPE.format(name=recipe.get("name", ""),
                                    ingredients=recipe.get("ingredients", ""),
                                    description=recipe.get("description", ""))

        await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                photo=recipe.get("photo", DEFAULT_PHOTO_FOR_RECIPE),
                                                reply_markup=await food_recipe_kb(0, len(recipe["cooking_instructions"]["steps"])))
        await msg.delete()
    except Exception as e:
        print("Error in food_recipe_call:", e)
        await callback_query.message.answer("Вибач, сталася помилка при завантаженні рецепту. Спробуй ще раз.")


@router.callback_query(F.data.startswith("page:"), Paginations.FoodRecipes)
async def food_recipes_page_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        msg = await loading_message(callback_query.message)
        try:
            page = int(callback_query.data.split(":")[1])
        except Exception:
            await callback_query.answer("Некоректний номер сторінки", show_alert=True)
            return

        recipe = await state.get_data()

        # Захист від виходу за межі
        pages = len(recipe["cooking_instructions"]["steps"])
        page = max(0, min(page, pages))
        
        if page == 0:
            msg = await loading_message(callback_query.message)
            text = T.FOOD_RECIPE.format(name=recipe.get("name", ""),
                                    ingredients=recipe.get("ingredients", ""),
                                    description=recipe.get("description", ""))
            await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                photo=recipe.get("photo", DEFAULT_PHOTO_FOR_RECIPE),
                                                reply_markup=await food_recipe_kb(0, len(recipe["cooking_instructions"]["steps"])))
            await msg.delete()
            return

        step = recipe["cooking_instructions"]["steps"][page - 1]
        text = T.RECIPE_STEP.format(step=step["step"],
                                        max_step=pages,
                                        text=step["text"])
        
        image = step.get("images") or [DEFAULT_PHOTO_FOR_RECIPE]
        await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                  photo=image[0],
                                                  reply_markup=await food_recipe_kb(page, pages))

        await msg.delete()
        await callback_query.answer()
    except Exception as e:
        print("Error in FoodRecipes_page_call:", e)
        await callback_query.message.answer("Вибач, сталася помилка при завантаженні сторінки. Спробуй ще раз.")


@router.callback_query(F.data == "back_to_recipes")
async def back_to_recipes_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "recipes TEXT"

    await callback_query.message.delete()
    await callback_query.message.answer(text=text,
                                        reply_markup=await recipes_kb(user_id))


@router.callback_query(F.data == "premium_recipes") # віддати преміум рецепт
async def premium_recipes_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "premium_recipes TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await premium_recipes_kb(user_id))


@router.callback_query(F.data == "back_to_recipes")
async def back_to_recipes_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "recipes TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await recipes_kb(user_id))


@router.callback_query(F.data.startswith("recipe_"))
async def recipe_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    recipe_id = callback_query.data.split("_")[1]

    data = await get_random_premium_recipe(recipe_id)

    text = data['content']
    video = FSInputFile(data['video'])

    await callback_query.message.delete()

    await callback_query.message.answer_video(caption=text,
                                              video=video,
                                              reply_markup=back_to_premium_recipes_kb)


@router.callback_query(F.data == "back_to_premium_recipes")
async def back_to_premium_recipes_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "premium_recipes TEXT"

    await callback_query.message.delete()

    await callback_query.message.answer(text=text,
                                        reply_markup=await premium_recipes_kb(user_id))


@router.callback_query(F.data == "cocktail_recipe")
async def cocktail_recipes_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_id = callback_query.from_user.id
        msg = await loading_message(callback_query.message)
        recipe = await get_random_json_food("cocktail_recipe.json")

        await state.set_state(Paginations.CocktailRecipes)
        await state.update_data(data=recipe)

        text = T.COCKTAIL_RECIPES.format(name=recipe.get("name", ""),
                                    ingredients=recipe.get("ingredients", ""),
                                    description=recipe.get("description", ""))

        await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                  photo=recipe.get("photo", DEFAULT_PHOTO_FOR_RECIPE),
                                                  reply_markup=await food_recipe_kb(0, len(
                                                      recipe["cooking_instructions"]["steps"])))
        await msg.delete()
    except Exception as e:
        print("Error in food_recipe_call:", e)
        await callback_query.message.answer("Вибач, сталася помилка при завантаженні рецепту. Спробуй ще раз.")


@router.callback_query(F.data.startswith("page:"), Paginations.CocktailRecipes)
async def cocktail_recipes_page_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        msg = await loading_message(callback_query.message)
        try:
            page = int(callback_query.data.split(":")[1])
        except Exception:
            await callback_query.answer("Некоректний номер сторінки", show_alert=True)
            return

        recipe = await state.get_data()

        # Захист від виходу за межі
        pages = len(recipe["cooking_instructions"]["steps"])
        page = max(0, min(page, pages))

        if page == 0:
            msg = await loading_message(callback_query.message)
            text = T.FOOD_RECIPE.format(name=recipe.get("name", ""),
                                        ingredients=recipe.get("ingredients", ""),
                                        description=recipe.get("description", ""))
            await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                      photo=recipe.get("photo", DEFAULT_PHOTO_FOR_RECIPE),
                                                      reply_markup=await food_recipe_kb(0, len(
                                                          recipe["cooking_instructions"]["steps"])))
            await msg.delete()
            return

        step = recipe["cooking_instructions"]["steps"][page - 1]
        text = T.RECIPE_STEP.format(step=step["step"],
                                         max_step=pages,
                                         text=step["text"])

        image = step.get("images") or [DEFAULT_PHOTO_FOR_RECIPE]
        await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                  photo=image[0],
                                                  reply_markup=await food_recipe_kb(page, pages))

        await msg.delete()
        await callback_query.answer()
    except Exception as e:
        print("Error in FoodRecipes_page_call:", e)
        await callback_query.message.answer("Вибач, сталася помилка при завантаженні сторінки. Спробуй ще раз.")


@router.callback_query(F.data == "sweets_recipe")
async def sweets_recipes_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_id = callback_query.from_user.id
        msg = await loading_message(callback_query.message)
        recipe = await get_random_json_food("sweets_recipe.json")

        await state.set_state(Paginations.SweetsRecipe)
        await state.update_data(data=recipe)

        text = T.SWEETS_RECIPE.format(name=recipe.get("name", ""),
                                    ingredients=recipe.get("ingredients", ""),
                                    description=recipe.get("description", ""))

        await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                  photo=recipe.get("photo", DEFAULT_PHOTO_FOR_RECIPE),
                                                  reply_markup=await food_recipe_kb(0, len(
                                                      recipe["cooking_instructions"]["steps"])))
        await msg.delete()
    except Exception as e:
        print("Error in food_recipe_call:", e)
        await callback_query.message.answer("Вибач, сталася помилка при завантаженні рецепту. Спробуй ще раз.")


@router.callback_query(F.data.startswith("page:"), Paginations.SweetsRecipe)
async def sweets_recipe_page_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        msg = await loading_message(callback_query.message)
        try:
            page = int(callback_query.data.split(":")[1])
        except Exception:
            await callback_query.answer("Некоректний номер сторінки", show_alert=True)
            return

        recipe = await state.get_data()

        # Захист від виходу за межі
        pages = len(recipe["cooking_instructions"]["steps"])
        page = max(0, min(page, pages))

        if page == 0:
            msg = await loading_message(callback_query.message)
            text = T.FOOD_RECIPE.format(name=recipe.get("name", ""),
                                        ingredients=recipe.get("ingredients", ""),
                                        description=recipe.get("description", ""))
            await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                      photo=recipe.get("photo", DEFAULT_PHOTO_FOR_RECIPE),
                                                      reply_markup=await food_recipe_kb(0, len(
                                                          recipe["cooking_instructions"]["steps"])))
            await msg.delete()
            return

        step = recipe["cooking_instructions"]["steps"][page - 1]
        text = T.RECIPE_STEP.format(step=step["step"],
                                         max_step=pages,
                                         text=step["text"])

        image = step.get("images") or [DEFAULT_PHOTO_FOR_RECIPE]
        await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                                  photo=image[0],
                                                  reply_markup=await food_recipe_kb(page, pages))

        await msg.delete()
        await callback_query.answer()
    except Exception as e:
        print("Error in FoodRecipes_page_call:", e)
        await callback_query.message.answer("Вибач, сталася помилка при завантаженні сторінки. Спробуй ще раз.")


# ----- tarological_call ----- tarological_call ----- tarological_call ----- tarological_call ----- tarological_call -----


@router.callback_query(F.data == "horoscope")
async def horoscope_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "horoscope TEXT"

    await callback_query.message.edit_text(text, reply_markup=await all_horoscope_kb())


@router.callback_query(F.data == "back_to_tarological")
async def back_to_tarological_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "tarological TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=await tarological_kb(user_id))


@router.callback_query(F.data.startswith("zodiac_"))
async def zodiac_call(callback_query: CallbackQuery):
    zodiac = callback_query.data.split("zodiac_")[1]
    data = await get_scraping_zodiac_sign(t_zodiac_signs[zodiac]["name"])

    text = T.ZODIAC.format(title=t_zodiac_signs[zodiac]["sign"] + " " + data.get("title", ""),
                                     text=data.get("text", ""))

    await callback_query.message.edit_text(text=text, reply_markup=back_to_all_horoscope_kb)


@router.callback_query(F.data == "back_to_all_horoscope")
async def back_to_all_horoscope_call(callback_query: CallbackQuery):
    await horoscope_call(callback_query)


@router.callback_query(F.data == "matrix_destiny")
async def matrix_destiny_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()

    text = "TEXT matrix_destiny"

    await callback_query.message.edit_text(text=text,
                                            reply_markup=await matrix_destiny_kb())


@router.callback_query(F.data.startswith("matrix_destiny_"))
async def matrix_destiny__call(callback_query: CallbackQuery, state: FSMContext):
    matrix_destiny = callback_query.data.split("matrix_destiny_")[1]

    if matrix_destiny == "personal":
        await state.set_state(MatrixOfDestiny.Personal)

        await callback_query.message.edit_text(text=T.MatrixOfDestinyChoiceSex,
                                               reply_markup=await matrix_destiny_personal_kb())
    elif matrix_destiny == "compatibility":
        await state.set_state(MatrixOfDestiny.Compatibility)
        await state.update_data(message_id=callback_query.message.message_id)

        await callback_query.message.edit_text(text=T.MatrixOfDestinyCompatibility,
                                               reply_markup=back_to_all_horoscope_kb)
    else:
        pass


@router.callback_query(F.data == "back_to_matrix_destiny")
async def back_to_matrix_destiny_call(callback_query: CallbackQuery, state: FSMContext):
    await matrix_destiny_call(callback_query, state)


@router.callback_query(F.data.startswith("m_d_personal_"), MatrixOfDestiny.Personal)
async def m_d_personal_call(callback_query: CallbackQuery, state: FSMContext):
    m_d_personal = callback_query.data.split("m_d_personal_")[1]

    if m_d_personal == "man":
        await state.update_data(gender="m")
    elif m_d_personal == "woman":
        await state.update_data(gender="f")

    await callback_query.message.edit_text(text=T.MatrixOfDestinyPersonal,
                                           reply_markup=back_to_m_d_personal_kb)
    await state.update_data(msg_id=callback_query.message.message_id)


@router.callback_query(F.data == "back_to_m_d_personal",
                       StateFilter(MatrixOfDestiny.Personal, MatrixOfDestiny.DataDisplay))
async def back_to_m_d_personal_call(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()

    await callback_query.message.answer(text=T.MatrixOfDestinyChoiceSex,
                                           reply_markup=await matrix_destiny_personal_kb())


def text_to_norm(t):
    t = re.sub(r'</?p\b[^>]*>', '', t, flags=re.I)
    return t


@router.callback_query(F.data.startswith("pdd:"), MatrixOfDestiny.DataDisplay)
async def matrix_personal_page_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        page = callback_query.data.split(":")[1]

        state_data = await state.get_data()
        position = state_data.get("position")
        if page == position:
            return

        await callback_query.message.delete()
        msg = await loading_message(callback_query.message)

        await state.update_data(position=page)

        response = await get_personal_matrix_data(state_data.get("body"))
        result_data = response["data"][0]["result"]

        if page == "photo":
            await callback_query.message.answer_photo(photo=state_data.get("photo"),
                                                      reply_markup=await personal_data_display_kb())
        elif page == "table":
            text = await chakra_matrix_html(response)

            await callback_query.message.answer(text=text,
                                                reply_markup=await personal_data_display_kb())
        elif page == "personal_qualities":
            text = "<b>{title}</b>\n\n{text}".format(title=response["data"][0].get("title"),
                                                     text=text_to_norm(result_data["intro"].get("text")))

            await callback_query.message.answer(text=(text + "\n\n⬇️ Обери знизу :)"),
                                                reply_markup=await personal_data_display_kb())
        elif page == "positive":
            text = "<b>{title}</b>\n\n{text}"

            await callback_query.message.answer(text=text.format(
                title=result_data["positive"].get("title"),
                text=text_to_norm(result_data["positive"].get("text"))),
                reply_markup=back_to_personal_qualities_kb)
        elif page == "negative":
            text = "<b>{title}</b>\n\n{text}"

            await callback_query.message.answer(text=text.format(
                title=result_data["negative"].get("title"),
                text=text_to_norm(result_data["negative"].get("text"))),
                reply_markup=back_to_personal_qualities_kb)
        elif page == "communication":
            text = "<b>{title}</b>\n\n{text}"

            await callback_query.message.answer(text=text.format(
                title=result_data["communication"].get("title"),
                text=text_to_norm(result_data["communication"].get("text"))),
                reply_markup=back_to_personal_qualities_kb)
        elif page == "health":
            text = text_to_norm(response["data"][1]["result"]["sahasrara"].get("text"))

            await callback_query.message.answer(text=text,
                                                reply_markup=await personal_data_display_kb())
        elif page == "past_life":
            text = text_to_norm(response["data"][2]["result"][0].get("text"))

            await callback_query.message.answer(text=text,
                                                reply_markup=await personal_data_display_kb())
        elif page == "appointment":
            text = text_to_norm(response["data"][3]["result"]["intro"].get("text"))

            await callback_query.message.answer(text=text,
                                                reply_markup=await personal_data_display_kb())
        elif page == "forecast_year":
            text_data = response["data"][12]["result"]["20"]

            title = text_to_norm(text_data.get("title"))
            text = text_to_norm(text_data.get("text"))

            await callback_query.message.answer(text=f"<b>{title}</b>\n\n{text}",
                                                reply_markup=await personal_data_display_kb())

        await msg.delete()
        await callback_query.answer()
    except Exception as e:
        print("Error in FoodRecipes_page_call:", e)
        await callback_query.message.answer(
            "😥 Вибач, сталася помилка. Спробуй ще раз.")


@router.callback_query(F.data == "back_to_data_display", MatrixOfDestiny.DataDisplay)
async def back_to_data_display_call(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    state_data = await state.get_data()

    await callback_query.message.answer_photo(photo=state_data.get("photo"),
                                              reply_markup=await personal_data_display_kb())


@router.callback_query(F.data == "back_to_personal_qualities", MatrixOfDestiny.DataDisplay)
async def back_to_personal_qualities_call(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    state_data = await state.get_data()
    response = await get_personal_matrix_data(state_data.get("body"))
    result_data = response["data"][0]["result"]

    text = "<b>{title}</b>\n\n{text}".format(title=response["data"][0].get("title"),
                                             text=text_to_norm(result_data["intro"].get("text")))

    await callback_query.message.answer(text=(text + "\n\n⬇️ Обери знизу :)"),
                                        reply_markup=await dd_personal_qualities_kb())


@router.callback_query(F.data.startswith("cdd:"), MatrixOfDestiny.DataDisplay)
async def matrix_compatibility_page_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        page = callback_query.data.split(":")[1]

        state_data = await state.get_data()
        position = state_data.get("position")
        if page == position:
            return

        await callback_query.message.delete()
        msg = await loading_message(callback_query.message)

        await state.update_data(position=page)

        response = await get_compatibility_matrix_data(state_data.get("body"))

        if page == "photo":
            await callback_query.message.answer_photo(photo=state_data.get("photo"),
                                                      reply_markup=await compatibility_data_display_kb())
        elif page == "positive":
            text_data = response["data"][0]["result"]["for"]
            title = text_to_norm(text_data.get("title"))
            text = text_to_norm(text_data.get("text"))

            await callback_query.message.answer(text=f"<b>{title}</b>\n\n{text}",
                                                reply_markup=await compatibility_data_display_kb())
        elif page == "cc_zone":
            text_data = response["data"][2]

            title = text_to_norm(text_data.get("title"))
            text = text_to_norm(text_data["result"]["intro"].get("text"))

            await callback_query.message.answer(text=f"<b>{title}</b>\n\n{text}",
                                                reply_markup=await compatibility_data_display_kb())

        await msg.delete()
        await callback_query.answer()
    except Exception:
        await callback_query.message.answer(
            "😥 Вибач, сталася помилка. Спробуй ще раз.")


# ----- reminder_call ----- reminder_call ----- reminder_call ----- reminder_call ----- reminder_call -----


@router.callback_query(F.data == "daily_reminder")
async def daily_reminder_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "TEXT"

    await callback_query.message.edit_text(text=text,
                                reply_markup=await  kb(user_id))


@router.callback_query(F.data == "one_reminder")
async def one_reminder_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = "TEXT"

    await callback_query.message.edit_text(text=text,
                                reply_markup=await  kb(user_id))

