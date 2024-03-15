from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config


def cabinet_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="💵 Пополнить счет", callback_data="deposit")
    button2 = InlineKeyboardButton(text="Заказать вывод 💸", callback_data="output")
    button5 = InlineKeyboardButton(text="🎢 Колесо Фортуны ", callback_data="wheel_of_fortune")
    button3 = InlineKeyboardButton(text="🎁 Сделать подарок", callback_data="send_money")
    button4 = InlineKeyboardButton(text="🍀 Промокод", callback_data="promocode")
    keyboard.row(button1, button2)
    keyboard.row(button5)
    keyboard.row(button3,button4)
    return keyboard


def participate():
    participate = InlineKeyboardMarkup(row_width=2)
    amount_wheel = open("wheel_of_fortune.txt","r").readline()
    participate.row(InlineKeyboardButton(text=f"✅ Учавствовать [{amount_wheel}₽]",callback_data=f"confirm"))
    return participate


def deposit_keyboard():
    keyboard = InlineKeyboardMarkup()
    button0 = InlineKeyboardButton(text="🎡 СБП", callback_data="method_balance_freekassasbp")
    button1 = InlineKeyboardButton(text="🎡 FreeKassa", callback_data="method_balance_freekassa")
    #button2 = InlineKeyboardButton(text="⚜️ CryptoBot", callback_data="method_crypto_bot_pay")
    button3 = InlineKeyboardButton(text="👨🏻‍💻Через поддержку", url="t.me/mabysov_official")
    #button1 = InlineKeyboardButton(text="₿ Banker", callback_data="deposit:banker")
    button1 = InlineKeyboardButton(text="⚜️ Payok", callback_data="method_balance_payok")
    keyboard.row(button0)
    keyboard.row(button1)
    keyboard.row(button3)
    #keyboard.row(button2)

    return keyboard


def output_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🥝 Qiwi/карта", callback_data="output:qiwi")
    #button3 = InlineKeyboardButton(text="₿ Banker", callback_data="output:banker")
    button4 = InlineKeyboardButton(text="❌ Отмена", callback_data="output:cancel")
    keyboard.row(button1)
    keyboard.row(button4)

    return keyboard

def p2p_deposit_keyboard(bill_id, url):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text='💸 Оплатить 💸', url=url))
    keyboard.add(
        InlineKeyboardButton(text='🔁 Проверить платёж', callback_data=f'check_p2p_deposit:{bill_id}'),
        InlineKeyboardButton(text='❌ Отменить', callback_data=f'reject_p2p_payment')
        )
    return keyboard



async def check_menu(url,amount,bill_id, service):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="↗️ Перейти к оплате", url=url)
            ],
            [
                InlineKeyboardButton(text="✅ Проверить оплату", callback_data=f"check:{amount}:{bill_id}:{service}")
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main_menu")
            ]
        ]
    )
    return markup


back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_personal_account")
        ]
    ]
)

rate_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🤩Отзывы🤩", url="https://t.me/+K0sVRqEHCE9hNmMx")
        ]
    ]
)

support_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🧑‍💻 Админ", url="https://t.me/mabysov_official")
        ]
    ]
)

chat_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💬CHAT💬", url="https://t.me/+UB4p4odHo0pkYTYy")
        ]
    ]
)

