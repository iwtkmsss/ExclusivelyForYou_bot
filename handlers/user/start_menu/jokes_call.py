from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from keyboards import (jokes_kb, good_mood_kb, tarological_kb, recipes_kb, reminder_kb, \
                       support_kb, games_kb, premium_recipes_kb, back_to_premium_recipes_kb)
from misc import get_random_recipe

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
async def food_recipe_call(callback_query: CallbackQuery):
    pass


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

    data = await get_random_recipe(recipe_id)

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
    