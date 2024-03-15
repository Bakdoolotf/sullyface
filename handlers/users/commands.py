from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import random,sqlite3,re

from aiogram import Dispatcher

from loader import bot
from states.states import OtherGameState
from config import config
from data.functions.db import get_user, delete_game,add_game_log,add_user_to_db,update_balance,add_other_game_to_db_chat,get_info_other_game, update_other_game_to_db_chat, update_score1_other_game_to_db, update_score2_other_game_to_db,update_status_other_game_to_db, get_other_game2,delete_other_game,delete_other_game_chat
from filters.filters import IsPrivate
from keyboards.inline.admin_menu_keyboards import admin_menu_keyboard
from keyboards.reply.reply_keyboards import main_menu_keyboard
from keyboards.inline.games_keyboard import join_game_chat,active_games_chat
from loader import dp

command_cub = "cub"
command_dar = "dar"
command_bol = "bol"

async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="Starting bot")
    ]
    await bot.set_my_commands(bot_commands)

@dp.message_handler(Command([command_cub,command_dar,command_bol]))#, chat_type='supergroup')
async def answer_command_game(message: Message):
        print(message)
        try:
            if message.text.split(' ')[1].isdigit():
                amount = int(message.text.split(' ')[1])
                if int(amount) >= 25:
                    if get_user(message.from_user.id)[1] >= int(amount):
                        me = await bot.get_me()
                        command_from_user = message.text.split(' ')[0].replace('/','').lower().replace(f'@{me.username}','')
                        game_id = random.randint(1111111, 9999999)
                        add_other_game_to_db_chat(game_id, message.from_user.id, message.from_user.username, amount, f"{command_from_user}_chat")
                        update_balance(message.from_user.id, -int(amount))
                        game_name=''
                        if(command_cub == command_from_user):
                            game_name = "🎲 Кубик"
                        elif(command_dar == command_from_user):
                            game_name = "🎯 Дартс"
                        else:
                            game_name = "🎳 Боулинг"
                        await message.answer(text=f"{game_name} Игра #{game_id}\n\n👤 Создал: @{message.from_user.username}\n\n💰 Ставка: {amount}₽", reply_markup=join_game_chat(game_id))
                    else:
                        await message.reply(text="Недостаточно средств для создания игры.")
                else:
                    await message.reply(text="Минимальная сумма ставки равна 25.")
            else:
                await message.reply(text="Неверный ввод.")
        except Exception as err:
            await message.reply(text=f"Введите правильно команду! {message.text.split(' ')[0]} и сумму\nПример: {message.text.split(' ')[0]} 100")
            print(f"Err: {err}")
            pass


@dp.callback_query_handler(text_startswith="join_game", state="*")
async def join_game_callback(call: types.CallbackQuery, state:FSMContext):
    variant = call.data.split(":")[1]
    if variant == "chat":
        game_id = call.data.split(":")[2]
        game_player1,game_bet,game_name = await get_info_other_game(game_id)
        try:
            if(str(call.from_user.id) != str(game_player1)):
                if get_user(call.from_user.id)[1] >= int(game_bet):
                    await call.message.delete()
                    game_player1_username = await bot.get_chat_member(chat_id=call.message.chat.id,user_id=game_player1)
                    print(game_player1_username.user.username)
                    #game_player1_username =  re.findall(r'Создал: @([A-Za-z0-9]+)',call.message.text)
                    #game_player1_username = game_player1_username[0]

                    game_name1 = ''
                    if(str(command_cub) == str(game_name.split('_')[0])):
                        game_name1 = "🎲 Кубик"
                    elif(str(command_dar) == str(game_name.split('_')[0])):
                        game_name1 = "🎯 Дартс"
                    else:
                        game_name1 = "🎳 Боулинг"
                    update_balance(call.from_user.id, -int(game_bet))

                    msg_simvol = await call.message.answer(text=f"{game_name1} #{game_id}\n\n👥Игроки:\n1️⃣ - @{game_player1_username.user.username}\n2️⃣ - @{call.from_user.username}\n\n - Отправьте {game_name1.split(' ')[0]} в ответ на это сообщение\n\n💰 Ставка: {game_bet}₽")
                    update_other_game_to_db_chat(game_id, msg_simvol.message_id, call.from_user.id, call.from_user.username)

                else:
                    await call.answer(text=f"Недостаточно средств для создания игры")
            else:
                await call.answer(text=f" Ты не можете играть с самим собой")
        except Exception as err:
            print("JoinGame_err: {err}")
            pass
    

# # # Ловит символы в чате
@dp.message_handler(content_types='dice', state='*')#chat_type='supergroup',
async def dice_msg(message: types.Message, state: FSMContext):
    try:
        if 'reply_to_message' in message:
            user_id = int(message.from_user.id)
            reply = int(message.reply_to_message.message_id)
            game = get_other_game2(reply)
            for row in game:
                if row[4] == 'cub_chat':
                    game_simvol = '🎲'
                elif row[4] == 'bol_chat':
                    game_simvol = '🎳'
                else:
                    game_simvol = '🎯'

                if message.dice.emoji == game_simvol:
                    if row[1] == user_id:
                        if row[6] == 0:
                            res = message.dice.value
                            print(f"res1 {message.dice.value}")
                            update_score1_other_game_to_db(row[0], res)
                            update_status_other_game_to_db(row[0], 1)
                    elif row[2] == user_id:
                        if row[7] == 0:
                            res = message.dice.value
                            print(f"res2 {message.dice.value}")
                            update_score2_other_game_to_db(row[0], res)
                            update_status_other_game_to_db(row[0], 1)
            try:
                game = get_other_game2(reply)
                
            except Exception as err:
                print(err)
                game == 0
            print(f"game_st {game}")
            if game != 0:
                for row in game:
                    print(f"row_game {row}")
                    if row[8] == 2:
                        print(f"Log game chat: {row[4]} #{row[0]} Users: @{row[9]}[{row[6]}] | @{row[10]}[{row[7]}] Win: win Winner: @{row[9]}")
                        delete_other_game_chat(row[0])
                        coms = 1 - (float(config('game_percent')) * 0.01)
                        win = round(float(row[3]*2*coms))
                        profit = row[3]*2 - win
                        

                        if row[6] > row[7]:
                            update_balance(row[1], +win, True)
                            await message.answer(
                                    text = f"{game_simvol} #{row[0]}\n\n"
                                           f"💰 Выигрыш: {win}₽\n\n"
                                            "👥Игроки:\n"
                                           f"1️⃣ - @{row[9]}[{row[6]}]\n"
                                           f"2️⃣ - @{row[10]}[{row[7]}]\n\n"
                                           f"🥳 Победитель: @{row[9]}"
                            )
                            add_game_log(row[0], row[1], row[2], row[3], profit, row[4])
                        elif row[6] < row[7]:
                            update_balance(row[2], +win, True)
                            await message.answer(
                                    text = f"{game_simvol} #{row[0]}\n\n"
                                           f"💰 Выигрыш: {win}₽\n\n"
                                            "👥Игроки:\n"
                                           f"1️⃣ - @{row[9]}[{row[6]}]\n"
                                           f"2️⃣ - @{row[10]}[{row[7]}]\n\n"
                                           f"🥳 Победитель: @{row[10]}"
                            )
                            add_game_log(row[0], row[2], row[1], row[3], profit, row[4])
                        else:
                            update_balance(row[1], +row[3])
                            update_balance(row[2], +row[3])
                            await message.answer(
                                    text = f"{game_simvol} #{row[0]}\n\n"
                                           f"💰 Выигрыш: {win}₽\n\n"
                                            "👥Игроки:\n"
                                           f"1️⃣ - @{row[9]}[{row[6]}]\n"
                                           f"2️⃣ - @{row[10]}[{row[7]}]\n\n"
                                            "⚪️⚪️⚪️ У игроков ничья!"
                            )
                    
    except Exception as err:
        print(f"ErrorChat: {err}")
        pass


@dp.message_handler(Command("start"))
async def answer_start(message: Message, state:FSMContext):
    await setup_bot_commands()
    if(message.chat.type == types.ChatType.PRIVATE):
        await state.finish()
        if get_user(message.chat.id) == None:
            add_user_to_db(message.chat.id, message.get_args())
            if message.get_args() and get_user(int(message.get_args())):
                await bot.send_message(message.get_args(), 'У вас новый реферал!')
        await bot.send_dice(chat_id=message.chat.id)
        await message.answer(text="🎲 Добро пожаловать в <b>Golden Rain Casino!</b>",
                            reply_markup=main_menu_keyboard())
    else:
        await message.answer(text="🔢 Доступные команды:\n/cub [сумма_ставки]\n/dar [сумма_ставки]\n/bol [сумма_ставки]\n/all_games")

@dp.message_handler(IsPrivate(), Command("admin"))
async def admin_menu(message: Message):
    if get_user(message.chat.id) != None:
        if str(message.chat.id) in str(config("admin_id")):
            await message.answer(text="<i>Админ меню</i>",
                                 reply_markup=admin_menu_keyboard())


@dp.message_handler(Command("all_games"))
async def all_games(message: Message):
    con = sqlite3.connect("data/database.db")
    cur = con.cursor()
    result = cur.execute('SELECT * FROM `other_games_chat` WHERE player_2 IS NULL').fetchall()
    con.close()

    if(len(result) >= 1):
        await message.answer('Активные игры', reply_markup=active_games_chat())
    else:
        await message.answer('Нет активных игр! :(')

@dp.message_handler(IsPrivate(), Command("game_remove_chat"))
async def admin_menu3(message: Message):
    print(str(config("admin_id")))
    if str(message.chat.id) in str(config("admin_id")):
        try:
            game_id = message.text.split(' ')[1]
            
            con = sqlite3.connect("data/database.db")
            cur = con.cursor()
            result = cur.execute(f'SELECT player_1,bet,player_2 FROM `other_games_chat` WHERE game_id= "{game_id}"').fetchone()
            con.close()
            print(f"result db: {result}")
            if(result[2]):
                update_balance(result[2], result[1], True)
                await bot.send_message(result[2],f"Твоя игра #{game_id} удалена, твои {result[1]} рублей возвращены!")
                await message.answer(text=f"Успешно удалена игра#{game_id}, сумма {result[1]} рублей возвращены пользователю {result[2]}")
            update_balance(result[0], result[1], True)
            await bot.send_message(result[0],f"Твоя игра #{game_id} удалена, твои {result[1]} рублей возвращены!")
            await message.answer(text=f"Успешно удалена игра#{game_id}, сумма {result[1]} рублей возвращены пользователю {result[0]}")
            delete_other_game_chat(game_id)
        except Exception as err:
            print(err)
            await message.answer(text=f"Формат команды: /game_remove_chat 123\n123 - Айди игры\nОшибка: {err}")


@dp.message_handler(IsPrivate(), Command("game_remove"))
async def admin_menu32(message: Message):
    print(str(config("admin_id")))
    if str(message.chat.id) in str(config("admin_id")):
        try:
            game_id = message.text.split(' ')[2]
            type_game = message.text.split(' ')[1]
            if(type_game == "other"):
                type_game = "other_games"
            elif(type_game == "blackjack"):
                type_game = "blackjack_games"
            else:
                type_game = "bakkara_games"
            con = sqlite3.connect("data/database.db")
            cur = con.cursor()
            g_player1, g_player2, g_bet = '','',''
            try:
                result = cur.execute(f'SELECT player_1,player_2,bet FROM `{type_game}` WHERE game_id= "{game_id}"').fetchone()
                g_player1 = result[0]
                g_bet = result[2]
                g_player2 = result[1]
            except:
                result = cur.execute(f'SELECT player_1,bet FROM `{type_game}` WHERE game_id= "{game_id}"').fetchone()
                g_player1 = result[0]
                g_bet = result[1]
            con.close()
            print(f"result db: {result}")
            try:
                if(g_player2):
                    update_balance(g_player2, g_bet, True)
                    await bot.send_message(g_player2,f"Твоя игра #{game_id} удалена, твои {g_bet} рублей возвращены!")
                    await message.answer(text=f"Успешно удалена игра#{game_id}, сумма {g_bet} рублей возвращены пользователю {g_player2}")
            except:
                pass
            update_balance(g_player1, g_bet, True)
            await bot.send_message(g_player1,f"Твоя игра #{game_id} удалена, твои {g_bet} рублей возвращены!")
            await message.answer(text=f"Успешно удалена игра#{game_id}, сумма {g_bet} рублей возвращены пользователю {g_player1}")
            delete_game(game_id,type_game)
        except Exception as err:
            print(err)
            await message.answer(text=f"Формат команды: /game_remove blackjack 123\n123 - Айди игры\nblackjack - тип игры(вариации <code>other</code> <code>blackjack</code>(21) <code>bakkara</code>)\nОшибка: {err}")

@dp.message_handler(IsPrivate(), Command("game_list_chat"))
async def admin_menu21(message: Message):
    print("!")
   
    if str(message.chat.id) in str(config("admin_id")):
        print("2")
        array = []
        con = sqlite3.connect("data/database.db")
        cur = con.cursor()
        result = cur.execute('SELECT game_id,bet,game_name,status FROM `other_games_chat`').fetchall()
        con.close()
        print(result)
        for row in result:
            array.append(f" <code>{row[0]}</code> <i>{row[2]}</i> - <b>{row[3]}</b> - <code>{row[1]}₽</code>")
        
        if (len(array) > 0):
            mess = ''
            for key in array:
                mess += key
                mess += '\n'
            await message.answer(text="Список игр\n\nID - GAME - STATUS - BET\n" + mess)
        else:
            await message.answer(text="Не наблюдается никаких игр")


@dp.message_handler(IsPrivate(), Command("game_list"))
async def admin_menu2(message: Message):
    print("!")
    if str(message.chat.id) in str(config("admin_id")):
        print("2")
        other_games_array,blackjack_games_array,bakkara_games_array = [],[],[]
        con = sqlite3.connect("data/database.db")
        cur = con.cursor()
        other_games_result = cur.execute('SELECT game_id,bet,game_name FROM `other_games`').fetchall()
        blackjack_games_result = cur.execute('SELECT game_id,bet,status FROM `blackjack_games`').fetchall()
        bakkara_games_result = cur.execute('SELECT game_id,bet,status FROM `bakkara_games`').fetchall()
        con.close()
        print(other_games_result)
        for row in other_games_result:
            other_games_array.append(f" <code>{row[0]}</code> <i>{row[2]}</i> - <code>{row[1]}₽</code>")
        for row in blackjack_games_result:
            blackjack_games_array.append(f" <code>{row[0]}</code> <i>{row[2]}</i> - <code>{row[1]}₽</code>")
        for row in bakkara_games_result:
            bakkara_games_array.append(f" <code>{row[0]}</code> <i>{row[2]}</i> - <code>{row[1]}₽</code>")
        other_games,blackjack_games,bakkara_games = '','',''
        if (len(other_games_array) > 0):
            for key in other_games_array:
                other_games += key
                other_games += '\n'
            await message.answer(text="Список игр other_games\nID - GAME - BET\n"+other_games)
        if (len(blackjack_games_array) > 0):
            for key in blackjack_games_array:
                blackjack_games += key
                blackjack_games += '\n'
            await message.answer(text="Список игр blackjack_games\nID - STATUS - BET\n"+blackjack_games)
        if (len(bakkara_games_array) > 0):
            for key in bakkara_games_array:
                bakkara_games += key
                bakkara_games += '\n'
            await message.answer(text="Список игр bakkara_games\nID - STATUS - BET\n"+bakkara_games)
       



