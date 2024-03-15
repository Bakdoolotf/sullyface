from aiogram.types import Message, InputFile

from config import cabinet_photo,config
from data.functions.db import get_user
from filters.filters import IsPrivate
from keyboards.inline.other_keyboards import cabinet_keyboard, rate_button, support_button, chat_button
from loader import dp, bot
from texts import cabinet_text


@dp.message_handler(IsPrivate(), text="🖥 Кабинет‍")
async def game_menu(message: Message):
    if get_user(message.chat.id) != None:
        await message.answer(cabinet_text(get_user(message.chat.id),message),
                             reply_markup=cabinet_keyboard())


@dp.message_handler(IsPrivate(), text="💬CHAT 💬")
async def chat(message: Message):
    await message.answer("<b><i>Игровой чат, с участниками бота🤖</i></b>", reply_markup=chat_button)

@dp.message_handler(IsPrivate(), text="👥 Партнёрка")
async def referals_handler(message: Message):
    me = await bot.get_me()
    await message.answer(
        f"👥 <b>Приглашай других людей и получай {config('ref_percent')}%"
        " от суммы их пополнений</b>\n\n📢 Ваша реферальная ссылка ⬇"
        f"\nhttps://t.me/{me.username}?start={message.from_user.id}",
        parse_mode="HTML")

'''
@dp.message_handler(IsPrivate(), text="📚 Помощь")
async def help(message: Message):
    await message.answer("""
<b><i>Ответь на кнопку помощь: 
Связь с администрацией проекта. Только в данных случаях.
1️⃣Найден баг бота 
2️⃣Есть какие то предложения
3️⃣При обращении указывать свой ID
developer by @deodexcodes
📛Запрещено писать, о выплатах!</i></b>""", reply_markup=support_button, parse_mode="HTML")
'''
'''
@dp.message_handler(IsPrivate(), text="🌴Отзывы🌴")
async def chat(message: Message):
    await message.answer("<i>️<b>Отзывы игрового, проекта вы можете нажав кнопку снизу⤵</b></i>️",
                         parse_mode="HTML", reply_markup=rate_button)
'''

