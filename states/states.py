from aiogram.dispatcher.filters.state import StatesGroup, State


class OtherGameState(StatesGroup):
    bet_amount = State()
    otvet_chat = State()


class BlackjackGameState(StatesGroup):
    bet_amount = State()


class SlotsGameState(StatesGroup):
    bet_amount = State()

class AdminPromoState(StatesGroup):
    create = State()

class AdminSearchUserState(StatesGroup):
    user_id = State()


class DepositQiwiState(StatesGroup):
    amount = State()


class BakkaraGameState(StatesGroup):
    bet_amount = State()

class Money(StatesGroup):
    promocode = State()
    send_money_user = State()
    send_money_finish = State()

class OutputState(StatesGroup):
    amount = State()
    place = State()
    requesites = State()
    confirm = State()


class JackpotGameState(StatesGroup):
    bet_amount = State()


class AdminChangeBalance(StatesGroup):
    amount = State()
    confitm = State()


class AdminChangeComission(StatesGroup):
    percent = State()
    confitm = State()


class AdminPictureMailing(StatesGroup):
    text = State()
    picture = State()
    confirm = State()


class AdminWithoutPictureMailing(StatesGroup):
    text = State()
    confirm = State()


class balance_states(StatesGroup):
    BS1 = State()