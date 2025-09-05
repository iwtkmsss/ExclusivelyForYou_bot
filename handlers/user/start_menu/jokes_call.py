import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards import (jokes_kb, good_mood_kb, tarological_kb, recipes_kb, reminder_kb, \
                       support_kb, games_kb, premium_recipes_kb, back_to_premium_recipes_kb, food_recipe_kb,
                       all_horoscope_kb, back_to_all_horoscope_kb, matrix_destiny_kb, back_to_m_d_personal_kb,
                       matrix_destiny_personal_kb, matrix_paginatios_kb)
from misc import get_random_premium_recipe, get_random_json_food, T, DEFAULT_PHOTO_FOR_RECIPE, Paginations, \
    loading_message, get_scraping_zodiac_sign, t_zodiac_signs, MatrixOfDestiny

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


@router.callback_query(F.data == "back_to_m_d_personal", MatrixOfDestiny.Personal)
async def back_to_m_d_personal_call(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text=T.MatrixOfDestinyChoiceSex,
                                           reply_markup=await matrix_destiny_personal_kb())


@router.callback_query(F.data.startswith("page:"), Paginations.PaginationPersonalMatrix)
async def matrix_personal_page_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        state_data = await state.get_data()

        try:
            page = int(callback_query.data.split(":")[1])
        except Exception:
            await callback_query.answer("Некоректний номер сторінки", show_alert=True)
            return

        recipe = await state.get_data()

        # Захист від виходу за межі
        page = max(0, min(page, 2))

        if page == 0:
            await callback_query.message.delete()
            await callback_query.message.answer_photo(photo=state_data.get("photo"),
                                                      reply_markup=await matrix_paginatios_kb(page, 2))
        elif page == 1:
            await callback_query.message.delete()
            await callback_query.message.answer(text=state_data.get("text"),
                                                reply_markup=await matrix_paginatios_kb(page, 2))
        elif page == 2:
            await callback_query.message.delete()

            data = state_data["data"][0]["result"]
            title = state_data["data"][0].get("title")

            def text_to_norm(t):
                t = re.sub(r'</?p\b[^>]*>', '', t, flags=re.I)
                return t

            text = T.MATRIX_SPECIAL_QUALITIES.format(
                title=title,
                intro_text=text_to_norm(data["intro"].get("text")),

                positive_title=data["positive"].get("title"),
                positive_text=text_to_norm(data["positive"].get("text")),
                negative_title=data["negative"].get("title"),
                negative_text=text_to_norm(data["negative"].get("text")),
                communication_title=data["communication"].get("title"),
                communication_text=text_to_norm(data["communication"].get("text")),
            )
            await callback_query.message.answer(text=text,
                                                reply_markup=await matrix_paginatios_kb(page, 2))
        await callback_query.answer()
    except Exception as e:
        print("Error in FoodRecipes_page_call:", e)
        await callback_query.message.answer("Вибач, сталася помилка при завантаженні сторінки. Спробуй ще раз.")
