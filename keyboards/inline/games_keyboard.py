from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

from config import other_games_info
from data.functions.db import get_other_games, get_other_game, get_blackjack_games, get_bakkara_games
from keyboards.inline.callback_datas import game_callback, game_info_callback, other_game_callback


def active_games_chat():
    active_games_chat = InlineKeyboardMarkup()
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()
    result = c.execute(f'SELECT * FROM `other_games_chat` WHERE player_2 IS NULL').fetchall()
    for info in result:
        active_games_chat.add(InlineKeyboardButton(f"#{info[0]} | {info[3]} руб", callback_data = f'join_game:chat:{info[0]}'))
    return active_games_chat

def join_game_chat(game_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(InlineKeyboardButton(text="✅ Присоединиться",callback_data=f"join_game:chat:{game_id}"))
    return keyboard

def join_game_chat_from_bot(game_name,game_id, action):
    print(game_name,game_id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(InlineKeyboardButton(text="✅ Присоединиться к игре",callback_data=game_info_callback.new(game_name=game_name, action=action, game_id=game_id)))
    return keyboard

def games_control_keyboard(game_name):
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    emoji = "✔"

    if game_name == "other":
        games = get_other_games()
        for game in games:
            try:
                keyboard.row(
                    InlineKeyboardButton(text=f"{other_games_info[game[-1]]['emoji']} #{game[0]} | {game[2]}₽",
                                        callback_data=game_info_callback.new(
                                            game_name=game_name, action="info", game_id=f"{game[0]}"
                                        )))
            except:
                pass

    elif game_name == "blackjack":
        games = get_blackjack_games()
        for game in games:
            keyboard.row(
                InlineKeyboardButton(text=f"🔍 Game #{game[0]} | {game[-2]}₽",
                                     callback_data=game_info_callback.new(
                                         game_name=game_name, action="info", game_id=f"{game[0]}"
                                     )))

    elif game_name == "bakkara":
        games = get_bakkara_games()
        for game in games:
            keyboard.row(
                InlineKeyboardButton(text=f"🔍 Game #{game[0]} | {game[-2]}₽",
                                     callback_data=game_info_callback.new(
                                         game_name=game_name, action="info", game_id=f"{game[0]}"
                                     )))

    button1 = InlineKeyboardButton(text=f"{emoji} Создать", callback_data=game_callback.new(
        game_name=game_name, action="create"
    ))
    button2 = InlineKeyboardButton(text="♻ Обновить", callback_data=game_callback.new(
        game_name=game_name, action="update"
    ))
    button3 = InlineKeyboardButton(text="📊 Статистика", callback_data=game_callback.new(
        game_name=game_name, action="statistic"
    ))
    keyboard.add(button1, button2, button3)
    return keyboard


def standart_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text=f"🃏 21 очко", callback_data=game_callback.new(game_name="game_blackjack", action="menu"))
    button2 = InlineKeyboardButton(text="🀄️ Baccara", callback_data=game_callback.new(game_name="game_baccara", action="menu"))
    button3 = InlineKeyboardButton(text="🎰 Слоты",callback_data=game_callback.new(game_name="game_slots", action="menu"))
    button4 = InlineKeyboardButton(text="🎴 Дурак, Покер", callback_data="durak_poker")
    button5 = InlineKeyboardButton(text="🕹 Другие игры", callback_data=game_callback.new(game_name="game_other", action="menu"))
    
    keyboard.add(button1, button2)
    keyboard.add(button3,button4)
    keyboard.add(button5)
    return keyboard

    
def other_games_types():
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="🎲 Кости", callback_data=other_game_callback.new(
        game_name="other", action="type_choice", game_type="dice"
    ))
    button2 = InlineKeyboardButton(text="🎯 Дартс", callback_data=other_game_callback.new(
        game_name="other", action="type_choice", game_type="darts"
    ))
    button3 = InlineKeyboardButton(text="🏀 Баскетбол", callback_data=other_game_callback.new(
        game_name="other", action="type_choice", game_type="basketball"
    ))
    button4 = InlineKeyboardButton(text="🎳 Боулинг", callback_data=other_game_callback.new(
        game_name="other", action="type_choice", game_type="bowling"
    ))
    keyboard.add(button1, button2, button3, button4)
    return keyboard


def games_info_keyboard(game_name, game_id):
    if game_name == "other":
        emoji = other_games_info[get_other_game(game_id)[-1]]['emoji']
        text = "Играть"
    elif game_name == "blackjack":
        emoji = ""
        text = "Принять ставку"
    elif game_name == "bakkara":
        emoji = ""
        text = "Играть"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text=f"{emoji} {text}",
                                   callback_data=game_info_callback.new(
                                       game_name=game_name, action="enjoy", game_id=game_id
                                   ))
    button2 = InlineKeyboardButton(text="Закрыть", callback_data="close")
    keyboard.add(button1, button2)

    return keyboard


def blackjack_keyboard(game_name, game_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text=f'➕ Взять еще карту', callback_data=game_info_callback.new(
        game_name=game_name, action="add_card", game_id=game_id
    ))
    button2 = InlineKeyboardButton(text=f'✔Хватит, вскрываемся', callback_data=game_info_callback.new(
        game_name=game_name, action="stop", game_id=game_id
    ))

    keyboard.add(button1, button2)

    return keyboard


def slots_menu_keyboard(game_name):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="🎰 Играть", callback_data=game_callback.new(
        game_name=game_name, action="play"
    ))
    button2 = InlineKeyboardButton(text="📊 Статистика", callback_data=game_callback.new(
        game_name=game_name, action="statistic"
    ))

    button3 = InlineKeyboardButton(text="💢 Закрыть", callback_data="close")

    keyboard.add(button1, button2, button3)

    return keyboard


def understand_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="💢 Понятно", callback_data="close")
    keyboard.add(button1)

    return keyboard


def jackpot_keyboard(game_name):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="⚡ Присоедениться", callback_data=game_callback.new(
        game_name=game_name, action="enjoy"
    ))
    button2 = InlineKeyboardButton(text="💰 Банк", callback_data=game_callback.new(
        game_name=game_name, action="bank"
    ))

    button3 = InlineKeyboardButton(text="📊 Статистика", callback_data=game_callback.new(
        game_name=game_name, action="statistic"
    ))

    button4 = InlineKeyboardButton(text="💢 Закрыть", callback_data="close")

    keyboard.add(button1, button2, button3)
    keyboard.row(button4)

    return keyboard


def jackpot_bank_keyboard(game_name):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="♻ Обновить", callback_data=game_callback.new(
        game_name=game_name, action="update_bank"
    ))
    button2 = InlineKeyboardButton(text="💢 Закрыть", callback_data="close")

    keyboard.add(button1)
    keyboard.row(button2)

    return keyboard


def first_bakkara_keyboard(game_name, game_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text=f'➕ Взять еще карту', callback_data=game_info_callback.new(
        game_name=game_name, action="add_card", game_id=game_id
    ))

    keyboard.add(button1)

    return keyboard