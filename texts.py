from data.functions.db import get_all_users, get_all_games, get_all_slots_bets_sum, get_all_today_users, \
    get_all_today_games, get_all_bets_sum, get_all_slots_games, get_all_today_slots_games, get_all_today_slots_bets_sum, \
    get_all_today_bets_sum,profit_all, profit_day

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def cabinet_text(user,message):
    print(user)
    text = f'''
👤Профиль
                                                                                                        
🆔 Ваш ID
└ <code>{user[0]}</code>

🏦 Ваш баланс
└ <code>{toFixed(float(user[1]),1)}₽</code>

🔤 - Никнейм
└ <code>{message.from_user.first_name}</code>

🔣 - Юзернейм
└ @{message.from_user.username}

🕒Дата регистрации
└ <code>{user[4]}</code>

    '''

    return text


def statistic_text(games_amount, win_amount, lose_amount, win, lose, profit):
    text = """
📜Всего игр: {}

📈Всего игр выиграно: {}
📉Всего игр проиграно: {}

▪️Выигрыш: {}₽
▪️Проигрыш: {}₽
▪️Профит: {}₽
    """.format(games_amount, win_amount, lose_amount, int(win), int(lose), int(profit))
    return text

def admin_search_user_text(user):
    text = """
<b>Информация о <a href='tg://user?id={}'>пользователе</a>:

🆔 Telegram ID: <code>{}</code>

💳 Баланс: {}₽

📅 Дата регистрации: {}
</b>
    """.format(
        user[0],
        user[0],
        user[1],
        user[4],
    )
    return text


def admin_statistic_text():
    text = """
Статистика за все время:

Всего пользователей: {}
Всего игр: {}
Всего прокрутов в слотах: {}
Ставок на сумму: {} RUB
Прокрутов на сумму: {} RUB
Чистых профитов: {} RUB

Статистика за сегодня:

Новых пользователей за сегодня: {}
Игр за сегодня: {}
Прокрутов в слотах за сегодня: {}
Ставок за сегодня на сумму: {} RUB
Прокрутов за сегодня на сумму: {} RUB
Чистых профитов за сегодня на сумму: {} RUB
    """.format(
        len(get_all_users()),
        len(get_all_games()),
        len(get_all_slots_games()),
        get_all_bets_sum(),
        get_all_slots_bets_sum() if get_all_slots_bets_sum() != None else 0,
        profit_all(),
        len(get_all_today_users()),
        len(get_all_today_games()),
        len(get_all_today_slots_games()),
        get_all_today_bets_sum() if get_all_today_bets_sum() != None else 0,
        get_all_today_slots_bets_sum() if get_all_today_slots_bets_sum() != None else 0,
        profit_day())
    return text


def jackpot_statistic_text(win_amount, win):
    text = """
📜Всего побед: {}
▪️Выигрыш: {}₽
    """.format(win_amount,
               int(win) if win != None else 0
               )
    return text


def slots_statistic_text(games_amount, bet_sum, win_sim, lose_sum):
    text = """
➖ Количество игр: {}
➖ Сумма ставок: {}₽
➖ Выиграно: {}₽
➖ Проиграно: {}₽
    """.format(games_amount,
               bet_sum if win_sim != None else 0,
               win_sim if win_sim != None else 0,
               lose_sum if lose_sum != None else 0
               )
    return text