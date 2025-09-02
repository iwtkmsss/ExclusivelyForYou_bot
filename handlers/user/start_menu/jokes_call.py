from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from keyboards import (jokes_kb, good_mood_kb, tarological_kb, recipes_kb, reminder_kb, \
                       support_kb, games_kb, premium_recipes_kb, back_to_premium_recipes_kb, food_recipe_kb)
from misc import get_random_premium_recipe, get_random_recipe, T, DEFAULT_PHOTO_FOR_RECIPE, Paginations, loading_message

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


# ----- recipes_kb ----- recipes_kb ----- recipes_kb ----- recipes_kb ----- recipes_kb -----

@router.callback_query(F.data == "food_recipe") # віддати рецепт їжі
async def food_recipe_call(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    msg = await loading_message(callback_query.message)
    recipe = await get_random_recipe()

    await state.set_state(Paginations.FoodRecipes)
    await state.update_data(data=recipe)

    text = T.FOOD_RECIPE.format(name=recipe.get("name", ""),
                                ingredients=recipe.get("ingredients", ""),
                                description=recipe.get("description", ""))

    

    await callback_query.message.answer_photo(caption=text.replace("None", ""),
                                              photo=recipe.get("photo", DEFAULT_PHOTO_FOR_RECIPE),
                                              reply_markup=await food_recipe_kb(0, len(recipe["cooking_instructions"]["steps"])))
    await msg.delete()


@router.callback_query(F.data.startswith("page:"), Paginations.FoodRecipes)
async def FoodRecipes_page_call(callback_query: CallbackQuery, state: FSMContext):
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
    text = T.FOOD_RECIPE_STEP.format(step=step["step"],
                                     max_step=pages,
                                     text=step["text"])
    
    images = step.get("images") or [DEFAULT_PHOTO_FOR_RECIPE]
    media = [InputMediaPhoto(media=i) for i in images]
    
    msgs = await callback_query.message.answer_media_group(media=media)
    await msgs[0].edit_caption(
        caption=text.replace("None", ""),
        reply_markup=await food_recipe_kb(page, pages)
    )

    await msg.delete()
    await callback_query.answer()


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
    