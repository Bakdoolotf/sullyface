from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from config import config
from data.functions.Banker import checked_btc
from data.functions.db import update_balance, get_user,enter_promo,exists_promo,info_participate,check_participate,add_participate
from filters.filters import IsPrivate, IsPrivateCall
from keyboards.inline.games_keyboard import understand_keyboard
from keyboards.inline.other_keyboards import deposit_keyboard, output_keyboard, participate
from loader import dp, bot
from states.states import OutputState, Money
import re



# Колесо фортуны
@dp.callback_query_handler(text="wheel_of_fortune", state="*")
async def wheel_fortune(call: CallbackQuery, state: FSMContext):
    amount_wheel = open("wheel_of_fortune.txt","r").readline()
    print(amount_wheel)
    c_participate = await info_participate()
    check = await check_participate(call.message.chat.id)
    info = 'Не учавствуешь'
    keyboard_get = participate()
    
    if(check):
        c_participate = await info_participate()
        veroyatnost = 1/int(len(c_participate))*100
        info = f'Участвуешь. Твой шанс на победу {veroyatnost}%'
        keyboard_get= None
    await call.message.edit_text(f'''
🏵 Колесо фортуны - рулетка, где победитель может выйграть деньги на баланс бота!

🚀 Колесо делает свою прокрутку каждый день в 12:00 по мск и выбирает рандомного победителя среди всех участников.

🔥 Участие в игре составляет {amount_wheel} RUB

👤 Участников: {len(c_participate)}
⚡️ Твой статус: {info}
''', reply_markup=keyboard_get)

@dp.callback_query_handler(text_startswith="confirm", state="*")
async def c_message(call: CallbackQuery, state: FSMContext):
    amount_wheel = open("wheel_of_fortune.txt","r").readline()
    print(amount_wheel)
    user_balance = get_user(call.message.chat.id)[1]
    if int(user_balance) >= int(amount_wheel):
        update_balance(call.message.chat.id, -int(amount_wheel))
        await add_participate(call.message.chat.id)
        participate = await info_participate()
        veroyatnost = 1/int(len(participate))*100
        countpart  = re.findall(r'Участников: ([0-9]+)',call.message.text)[0]
        s = call.message.text.replace(f"Участников: {countpart}",f"Участников: {len(participate)}")
        await call.message.edit_text(text=s.replace('Не учавствуешь', f'Участвуешь. Твой шанс на победу {veroyatnost}%'))
    else:
        await call.message.answer("❌ На вашем балансе нет данной суммы.")

@dp.callback_query_handler(text_startswith="promocode",state="*")
async def promocode_message(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"Введите промокод")
    await Money.promocode.set()


@dp.message_handler(IsPrivate(), state=Money.promocode)
async def promocode(message: Message, state: FSMContext):
    if(await enter_promo(message.chat.id,message.text)):
        price = await exists_promo(message.text)
        await message.answer( f'💸 Вы активировали промокод на сумму <b>{price}</b> ₽')
    else:
        await message.answer(f'💁🏻‍♀️ Промокод <code>{message.text}</code> не найден')
    await state.finish()


@dp.callback_query_handler(text_startswith="send_money",state="*")
async def send_money(call: CallbackQuery, state: FSMContext):
    user_balance = get_user(call.message.chat.id)[1]
    await call.message.answer(f"Введите сумму подарка в рублях до {user_balance} RUB")
    await Money.send_money_user.set()

@dp.message_handler(IsPrivate(), state=Money.send_money_user)
async def send_money_user(message: Message, state: FSMContext):
    user_balance = get_user(message.chat.id)[1]
    try:
        if int(message.text) <= user_balance:
            if message.text.isdigit():
                await state.update_data(amount=message.text)
                await message.answer(f"🆔 Пришли мне ID пользователя котому надо отправить {message.text} RUB")
                await Money.send_money_finish.set()
            else:
                await message.answer(f"❌ Неверный ввод")
                await state.finish()
        else:
            await message.answer(f"❌ На вашем балансе нет данной суммы.")
            await state.finish()
    except:
        await message.answer(f"❌ Неверный ввод")
        await state.finish()
@dp.message_handler(IsPrivate(), state=Money.send_money_finish)
async def send_money_finish(message: Message, state: FSMContext):
    try:
        user_id_send = get_user(message.text)[0]
        print(user_id_send)
        data = await state.get_data()
        amount = int(data['amount'])
    
        print(user_id_send)
        update_balance(message.chat.id, -amount)
        update_balance(message.text, amount)
        await message.answer(f"✅ Сумма {amount} RUB успешно отправлена пользователю")
        await bot.send_message(message.text,f"⭐️ Вам пришел подарок в размере {amount} RUB от пользователя {message.chat.id}")
        await state.finish()
    except Exception as err:
        await message.answer(f"❌ Неправильно введен ID пользователя!")

@dp.callback_query_handler(IsPrivateCall(), text="deposit")
async def admin_settings(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(text="Выберите систему пополнения.",
                            reply_markup=deposit_keyboard())


@dp.callback_query_handler(IsPrivateCall(), text="deposit:banker")
async def admin_settings(call: CallbackQuery):
    await call.message.answer("Для оплаты чеком, просто отправьте его в чат.")


@dp.message_handler(IsPrivate())
async def deposit_btc(message: Message):
    if re.search(r'BTC_CHANGE_BOT\?start=', message.text):
        code = re.findall(r'c_\S+', message.text)[0]
        msg =  await checked_btc(message.chat.id, code)
        await message.answer(msg, reply_markup=understand_keyboard())

@dp.callback_query_handler(IsPrivateCall(), text="output")
async def output_1(call: CallbackQuery):
    user_balance = get_user(call.message.chat.id)[1]
    if user_balance >= 100:
        await call.message.answer(f"Введите сумму вывода от 100 до {user_balance} RUB")
        await OutputState.amount.set()
    else:
        await call.message.answer(f"Ваш баланс меньше 100 RUB")


@dp.message_handler(IsPrivate(), state=OutputState.amount)
async def output_2(message: Message, state: FSMContext):
    if message.text.isdigit():
        user_balance = get_user(message.chat.id)[1]
        if 100 <= int(message.text):
            if int(message.text) <= user_balance:
                async with state.proxy() as data:
                    data["amount"] = int(message.text)
                await message.answer(f"Куда вы хотите вывести баланс.",
                                     reply_markup=output_keyboard())
                await OutputState.next()
            else:
                await message.answer(f"❗ На вашем балансе нет данной суммы.")
        else:
            await message.answer(f"❗ Минимальная сумма вывода 100 RUB.")
    else:
        await message.answer(f"❗ Неверный ввод.")

@dp.callback_query_handler(IsPrivateCall(), state=OutputState.place)
async def output_3(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == "output:qiwi":
        async with state.proxy() as data:
            data["place"] = "qiwi"
        await call.message.answer(f"Укажите реквезиты для вывода.")
        await OutputState.next()
    elif call.data == "output:banker":
        async with state.proxy() as data:
            amount = data["amount"]
            data["place"] = "banker"
        await call.message.answer(f"💰 Сумма вывода: <b>{amount}</b>\n\n"
                                  f"ℹ️Площадка: <b>Banker</b>\n\n"
                                  f"Для подтверждения отправьте <b>+</b>")
        await OutputState.confirm.set()
    elif call.data == "output:cancel":
        await call.message.answer(f"Вывод успешно отменён.")
        await state.finish()


@dp.message_handler(IsPrivate(), state=OutputState.requesites)
async def output_4(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["requesites"] = message.text
        amount = data["amount"]
    await message.answer(f"💰 Сумма вывода: <b>{amount}</b>\n\n"
                         f"📱 Реквезиты:<b>{message.text}</b>\n\n"
                              f"ℹ️Площадка: <b>QIWI</b>\n\n"
                              f"Для подтверждения отправьте <b>+</b>")
    await OutputState.confirm.set()


@dp.message_handler(IsPrivate(), state=OutputState.confirm)
async def output_4(message: Message, state: FSMContext):
    if message.text == "+":
        async with state.proxy() as data:
            if data["place"] == "qiwi":
                requesites = data["requesites"]
            amount = data["amount"]
            place = data["place"]
        update_balance(message.chat.id, -amount)
        await message.answer("Заявка на вывод успешно сформирована")

        text = f"""⭐️ Новая заявка на вывод!
Telegram ID: {message.chat.id}
@{message.from_user.username} | <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>
Сумма: {amount}
Площадка: {place}\n"""
        if place == "qiwi":
            text += f"Реквезиты: {requesites}"
        #for admin in config("admin_id").split(":"):
        #    await bot.send_message(chat_id=admin, text=text)
        await bot.send_message(chat_id=config("admin_chat"), text=text)
        await bot.send_message(chat_id=config("chat_id"), text=f"⭐️ Новая заявка на вывод!\nПользователь <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выводит {amount} рублей")
    await state.finish()