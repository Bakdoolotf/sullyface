from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

import random, json, logging, hashlib, requests

from config import config
from data.functions.db import get_user, add_stat, select_buy_stat, update_balance, delete_stat, get_now_qiwi_settings,add_deposit
from keyboards.inline.other_keyboards import check_menu, back_to_personal_account, cabinet_keyboard, support_button
from loader import dp, bot
from handlers.users.freekassa import FreeKassa
from states.states import balance_states
from texts import cabinet_text

from glQiwiApi import QiwiWrapper
from glQiwiApi import QiwiP2PClient
from glQiwiApi.qiwi.clients.p2p.types import Bill
qiwi_p2p_client = QiwiP2PClient(secret_p2p=config('p2p_qiwi_key'))



payok_api_id = '2558'
payok_api_key = '3AB290AF37B3BE46DD824859C5F39BC3-F8E76B99704F20C5A870E5D863C6FE3E-79FC115CFCFBFC2602D170B8B566B41D'
payok_shop_id = '3092'
payok_secret = '61f81425214eac249de3420327cf7bc9'
# # # Создание счета PayOK
async def createPay_payok(amount: float, payment: str, desc: str, shop: int, currency: str,) -> str:
    try:
        data = [amount, payment, shop, currency, desc, payok_secret]
        sign = hashlib.md5("|".join(map(str, data)).encode("utf-8")).hexdigest()
        url = f"https://payok.io/pay?amount={amount}&payment={payment}&desc={desc}&shop={shop}&sign={sign}"
        return url
    except:
        logging.exception('message')

# # # Получение транзакции PayOK
async def getTransaction_payok(shop: int, payment: int, offset: int = None) -> dict:
    try:
        url = "https://payok.io/api/transaction"
        data = {"API_ID": payok_api_id, "API_KEY": payok_api_key, "shop": shop, "payment": payment, "offset": offset}
        response = requests.post(url, data).json()
        return response
    except:
        logging.exception('message')

# # # Создание выплаты PayOK
async def createPayout_payok(amount: float, method: str, reciever: str, comission_type: str, webhook_url: str = None) -> dict:
    try:
        url = "https://payok.io/api/payout_create"
        data = {"API_ID": payok_api_id, "API_KEY": payok_api_key, "amount": amount, "method": method, "reciever": reciever, "comission_type": comission_type, "webhook_url": webhook_url}
        response = requests.post(url, data).json()
        return response

    except:
        logging.exception('message')

# # # Получение баланса PayOK
async def getBalance_payok() -> dict:
    try:
        url = "https://payok.io/api/balance"
        data = {"API_ID": payok_api_id, "API_KEY": payok_api_key}
        response = requests.post(url, data).json()
        balance = float(response["balance"])
        return balance
    except:
        logging.exception('message')


@dp.callback_query_handler(text="back_to_main_menu", state="*")
async def back_to_main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(cabinet_text(get_user(call.from_user.id),call.message),
                                 reply_markup=cabinet_keyboard())


@dp.callback_query_handler(text_startswith="method_balance", state="*")
async def add_balance_main(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Напишите сумму, которую вы хотите пополнить."
                                 "\n❗️*Внимание*❗️\n`Минимальная сумма пополнения - 10₽`",
                                 parse_mode="MarkDown", reply_markup=back_to_personal_account)
    await state.update_data(call_data=call.data)
    await balance_states.Main.set()


@dp.message_handler(state=balance_states.Main)
async def add_balance_2(message: Message, state: FSMContext):
    amount = message.text
    if int(amount) >= 10:
        data = await state.get_data()
        if "qiwi" in data['call_data']:
            comment = str(message.from_user.id)+"_"+str(random.randint(1000,9999))
            async with qiwi_p2p_client:
                bill = await qiwi_p2p_client.create_p2p_bill(amount=amount,comment=comment)
            payment_link = bill.pay_url
            order_id = bill.id
        elif "freekassa" in data['call_data']:
                order_id = int(message.from_user.id)+int(random.randint(1,9999))
                if "sbp" in data['call_data']:
                    if int(amount) < 300:
                        await message.answer("СБП пополнение от 300 RUB, попробуйте еще раз :)")
                    else:
                        payment_link = await FreeKassa().create_payment_link(order_id,amount,sbp=True)
                else:
                    payment_link = await FreeKassa().create_payment_link(order_id,amount)
        elif "payok" in data['call_data']:
            order_id = random.randint(11111111111, 99999999999)
            desc = str(message.from_user.id)
            payment_link = await createPay_payok(amount, order_id, desc, payok_shop_id, 'RUB')
        if payment_link:
            
            await bot.send_message(message.chat.id,f'''
*Для того, чтобы пополнить свой баланс на* `{amount}` *RUB вам нужно:*

💰 Оплатить - `{amount}` RUB
🔗 По ссылке - `{payment_link}`''',parse_mode="MarkDown",reply_markup=await check_menu(payment_link,amount,order_id,data['call_data']))
            await state.finish()
        else:
            await message.answer("🚫 Ошибка. Обратитесь к администратору")
            await state.finish()
    else:
        await message.answer("Неверное количество, попробуйте еще раз :)")


@dp.callback_query_handler(text_startswith="check",state="*")
async def add_balance_main(call: CallbackQuery, state: FSMContext):
    bill_id = call.data.split(":")[2]
    amount = call.data.split(":")[1]
    service = call.data.split(":")[3]
    if "qiwi" in service:
        w = QiwiWrapper(secret_p2p=config('p2p_qiwi_key'))
        check = await w.check_p2p_bill_status(bill_id=bill_id)
    elif "freekassa" in service:
        check1 = await FreeKassa().get_orders()
        check2 = await FreeKassa().find_order_by_merchant_id(check1,bill_id)
        check = json.loads(check2)
    elif "payok" in service:
        check = await getTransaction_payok(payok_shop_id, bill_id)
        print(check)
    if check is not None and (check == 'PAID' or (check.get('orders') and check['orders'][0]['status'] == 1) or check.get("status") == "success" and check.get("1", {}).get("transaction_status") == "1"):
        update_balance(call.from_user.id, int(amount))
        await call.message.edit_text(f"✅ <b>Готово, платеж получен, баланс начислен(<code>{amount}руб</code>)</b>", parse_mode="HTML")
        user = get_user(call.from_user.id)
        if user[5]:
            ref_pay = float(amount) * (float(config('ref_percent')) / 100)
            update_balance(user[5], ref_pay)
            await bot.send_message(user[5],f'Выш баланс пополнен на {round(ref_pay, 2)} RUB за пополнение вашего реферала')
        await bot.send_message(chat_id=config("chat_id"),text=f"⭐️ Пополнение от @{call.from_user.username} на сумму <code>{amount}руб</code>", parse_mode="HTML")
    else:
        await call.answer("Вы не оплатили счёт", show_alert=True)