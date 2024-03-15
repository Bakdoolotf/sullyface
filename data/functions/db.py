import sqlite3
import datetime
import time
from time import strftime

def get_now_date():
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    return date


def add_profit(user_id,game_name,price):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute("INSERT INTO `profit` (user_id, game_name, price_from_game) VALUES(?,?,?)",
                   (user_id, game_name, price,))
    db.commit()

# STAT
def add_stat(user_id, cost, pre_bal):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    user = [user_id, 0, "False", "False", get_now_date()]
    cursor.execute("INSERT INTO stat (user_id, cost, pre_bal) VALUES(?,?,?)",
                   (user_id, cost, pre_bal,))
    db.commit()


def select_buy_stat(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM stat WHERE user_id =?", (user_id,))
    row = cursor.fetchone()
    return row


def delete_stat(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    user = [user_id, 0, "False", "False", get_now_date()]
    cursor.execute("DELETE FROM stat WHERE user_id =?", (user_id,))
    db.commit()


def add_user_to_db(user_id, referer):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    user = [user_id, 0, "False", "False", get_now_date(), referer or 0]
    cursor.execute(f'''INSERT INTO users(user_id, balance, twist, banned, registration_date, referer) VALUES(?,?,?,?,?,?)''', user)
    db.commit()


async def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

async def create_promo(name,price,count):
    try:
        print(price)
        print(name)
        print(count)
        if (await isfloat(price) is not False):
            if name is not None:
                result = await user_add_promo(name, float(price),count)
            
            if (result == 1):
                return True
        else:
            return False

    except Exception as e:
        print(e)
        return False



async def user_add_promo(name, price,count):
    try:
        with sqlite3.connect("data/database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO `promocode` (`name`, `price`,`count`) VALUES(?,?,?)", (name, int(price),int(count)))
        return 1
    except Exception as e:
        print(e)
        return 0

async def exists_promo(name):
    try:
        with sqlite3.connect("data/database.db") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `promocode` WHERE `name` = ?', (name,)).fetchall()
            if (bool(len(result)) == True):
                for row in result:
                    return row[1]
            else:
                return 0
    except Exception as e:
        print(e)
        return 0

async def execute_promocode(user_id,name):
    conn = sqlite3.connect("data/database.db")
    c =conn.cursor()
    c.execute("INSERT INTO `promocode_user` (`user_id`, `name`) VALUES(?,?)", (user_id, name,))
    conn.commit()
    conn.close()

async def exists_execute_promo(user_id,name):
    try:
        with sqlite3.connect("data/database.db") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `promocode_user` WHERE `name` = ? AND `user_id` = ?', (name,user_id,)).fetchall()
            check_count = cur.execute('SELECT * FROM `promocode` WHERE `name` = ? ', (name,)).fetchall()
            print(result)
            print(check_count)
            if(int(check_count[0][2]) > 0):
                print("1")
                if len(result) <= 0:
                    print("2")
                    return False
                else:
                    print("3")
                    return True
            else:
                print("0")
                return True
    except Exception as err:
        print(err)
        return True

async def count_minus_promocode(name):
    conn = sqlite3.connect("data/database.db")
    c =conn.cursor()
    c.execute("UPDATE promocode SET count=count-1 WHERE name=?",(name,))
    conn.commit()
    conn.close()

async def enter_promo(user_id,name):
    try:
        price = await exists_promo(name)
        execute = await exists_execute_promo(user_id,name)

        if(execute):
            return False
        else:
            update_balance(user_id, price)
            await count_minus_promocode(name)
            await execute_promocode(user_id,name)
            return True
    except:
        pass

async def add_participate(user_id):
	time = strftime("%Y-%m-%d %H:%M:%S")

	conn = sqlite3.connect("data/database.db")
	c = conn.cursor()
	c.execute("INSERT INTO `users_participate` VALUES(?,?)",(user_id,time,))
	conn.commit()
	conn.close()
async def delete_participate():
	conn = sqlite3.connect("data/database.db")
	c = conn.cursor()
	result = c.execute(f"DELETE FROM `users_participate`")
	conn.commit()

async def info_participate():
	conn = sqlite3.connect("data/database.db")
	c = conn.cursor()
	result = c.execute(f"SELECT * FROM `users_participate`").fetchall()
	return result
	
async def check_participate(user_id):
	try:
		conn = sqlite3.connect("data/database.db")
		c = conn.cursor()
		result = c.execute(f"SELECT * FROM `users_participate` WHERE user_id = {user_id}").fetchone()
		print(result)
		if len(result) == 0:
			return False
		else:
			return True
	except:
		return False

def get_user(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM users WHERE user_id = '{user_id}'""")
    row = cursor.fetchone()
    return row


def profit_day():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM games_logs WHERE date= '{get_now_date()}' ''')
    row = cursor.fetchall()
    profit = 0
    for rows in row:
        profit += float(rows[4])
    return profit




def get_all_users():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM users""")
    row = cursor.fetchall()
    return row


def get_all_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM games_logs''')
    row = cursor.fetchall()
    return row


def get_all_slots_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM slots_logs''')
    row = cursor.fetchall()
    return row


def get_all_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank) FROM games_logs''')
    row = cursor.fetchone()[0]
    return row


def get_all_slots_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM slots_logs''')
    row = cursor.fetchone()[0]
    return row


def get_all_today_users():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM users WHERE registration_date = '{get_now_date()}' """)
    row = cursor.fetchone()
    return row


def get_all_today_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM games_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchall()
    return row


def get_all_today_slots_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM slots_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchall()
    return row


def get_all_today_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank) FROM games_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchone()[0]
    return row


def get_all_today_slots_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM slots_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchone()[0]
    return row


def change_spinup_status(user_id, status):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE users SET twist = '{status}' WHERE user_id = '{user_id}' """)
    db.commit()

async def get_info_other_game(game_id):
    db = sqlite3.connect("data/database.db")
    cursor = db.cursor()
    res = cursor.execute("SELECT player_1,bet,game_name FROM `other_games_chat` WHERE game_id=?",(game_id,)).fetchone()
    print(res[0])
    print(res[1])
    print(res[2])
    return res[0],res[1],res[2]

def profit_all():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM games_logs ''')
    row = cursor.fetchall()
    profit = 0
    for rows in row:
        profit += float(rows[4])
    return profit

def update_balance(user_id, amount, add=True):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    if add:
        cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id,))
    else:
        cursor.execute(f"""UPDATE users SET balance = ? WHERE user_id = ? """, (amount, user_id,))

    db.commit()
    db.close()

def add_other_game_to_db(game_id, player_1, bet, game_name):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, player_1, bet, game_name]
    cursor.execute(f'''INSERT INTO other_games(game_id, player_1, bet, game_name) VALUES(?,?,?,?)''', game)
    db.commit()
    
def add_other_game_to_db_chat(game_id, player_1, username_1, bet, game_name):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, player_1, bet, game_name, username_1]
    cursor.execute(f'''INSERT INTO other_games_chat(game_id, player_1, bet, game_name, username_1) VALUES(?,?,?,?,?)''', game)
    db.commit()

def update_other_game_to_db(game_id, answer_here, player_2, username_2):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE other_games SET (player_2, answer_here, username_2) = (?, ?, ?) WHERE game_id = ? """, (player_2, answer_here, username_2, game_id,))
    db.commit()

def update_other_game_to_db_chat(game_id, answer_here, player_2, username_2):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE other_games_chat SET (player_2, answer_here, username_2) = (?, ?, ?) WHERE game_id = ? """, (player_2, answer_here, username_2, game_id,))
    db.commit()

def update_score1_other_game_to_db(game_id, score_1):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE other_games_chat SET score_1 = ? WHERE game_id = ? """, (score_1, game_id,))
    db.commit()

def update_score2_other_game_to_db(game_id, score_2):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE other_games_chat SET score_2 = ? WHERE game_id = ? """, (score_2, game_id,))
    db.commit()

def update_status_other_game_to_db(game_id, status):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE other_games_chat SET status = status + ? WHERE game_id = ? """, (status, game_id,))
    db.commit()

def get_other_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM other_games""")
    row = cursor.fetchall()
    return row


def get_other_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM other_games WHERE game_id = '{game_id}'""")
    row = cursor.fetchone()
    return row

def get_other_game2(answer_here):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM other_games_chat WHERE answer_here = '{answer_here}'""")
    row = cursor.fetchall()
    return row


def delete_other_game_chat(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM other_games_chat WHERE game_id = '{game_id}'""")
    db.commit()

def delete_other_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM other_games WHERE game_id = '{game_id}'""")
    db.commit()
    
def delete_game(game_id,type):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM `{type}` WHERE game_id = '{game_id}'""")
    db.commit()

def add_blackjack_game_to_db(game_id, player_1, bet):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, player_1, 0, 0, 0, 0, 0, 0, 0, bet, "False"]
    cursor.execute(f'''INSERT INTO blackjack_games VALUES(?,?,?,?,?,?,?,?,?,?,?)''', game)
    db.commit()


def get_blackjack_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM blackjack_games WHERE status = 'False' """)
    row = cursor.fetchall()
    return row


def get_blackjack_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM blackjack_games WHERE game_id = '{game_id}'""")
    row = cursor.fetchone()
    return row


def update_player_blackjack(game_id, player_2):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE blackjack_games SET player_2 = '{player_2}' WHERE game_id = '{game_id}' """)
    db.commit()


def update_blackjack_game_status(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE blackjack_games SET status = 'True' WHERE game_id = '{game_id}' """)
    db.commit()


def add_card_to_player(game_id, player, number):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE blackjack_games SET {player}_amount = {player}_amount + 1 WHERE game_id = '{game_id}' """)
    db.commit()
    cursor.execute(
        f"""UPDATE blackjack_games SET {player}_result = {player}_result + {number} WHERE game_id = '{game_id}' """)
    db.commit()


def delete_blackjack_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM blackjack_games WHERE game_id = '{game_id}'""")
    db.commit()


def add_game_log(game_id, winner, loser, bank, profit, game_name):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, winner, loser, bank, profit, game_name, get_now_date()]
    cursor.execute(f'''INSERT INTO games_logs VALUES(?,?,?,?,?,?,?)''', game)
    db.commit()


def add_slots_log(player, bet, win, win_amount):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [player, bet, win, win_amount, get_now_date()]
    cursor.execute(f'''INSERT INTO slots_logs VALUES(?,?,?,?,?)''', game)
    db.commit()


def add_jackpot_log(winner, bank, profit, losers):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [winner, bank, profit, losers, get_now_date()]
    cursor.execute(f'''INSERT INTO jackpot_logs VALUES(?,?,?,?,?)''', game)
    db.commit()


def get_user_other_game_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM games_logs WHERE winner = '{user_id}'
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_other_game_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM((bank - profit)/2) FROM games_logs WHERE loser = '{user_id}'
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_other_game_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM games_logs WHERE winner = '{user_id}'
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_other_lose_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(loser) FROM games_logs WHERE loser = '{user_id}'
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_game_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_lose_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(loser) FROM games_logs WHERE loser = '{user_id}'
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_game_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_game_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM((bank - profit)/2) FROM games_logs WHERE loser = '{user_id}'
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def add_bakkara_game_to_db(game_id, player_1, bet):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, player_1, 0, 0, 0, None, None, bet, "False"]
    cursor.execute(f'''INSERT INTO bakkara_games VALUES(?,?,?,?,?,?,?,?,?)''', game)
    db.commit()


def update_bakkara_game_status(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET status = 'True' WHERE game_id = '{game_id}' """)
    db.commit()


def update_player_bakkara(game_id, player_2):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET player_2 = '{player_2}' WHERE game_id = '{game_id}' """)
    db.commit()


def get_bakkara_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM bakkara_games WHERE game_id = '{game_id}'""")
    row = cursor.fetchone()
    return row


def get_bakkara_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM bakkara_games WHERE status = 'False' """)
    row = cursor.fetchall()
    return row


def add_card_to_bakkara_player(game_id, player, number):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET {player}_result = '{number}' WHERE game_id = '{game_id}' """)
    db.commit()


def add_cards_to_bakkara_player(game_id, player, cards):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET {player}_cards = '{cards}' WHERE game_id = '{game_id}' """)
    db.commit()


def delete_bakkara_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM bakkara_games WHERE game_id = '{game_id}'""")
    db.commit()


def get_user_bakkara_game_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_bakkara_lose_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(loser) FROM games_logs WHERE loser = '{user_id}'
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_bakkara_game_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_bakkara_game_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM((bank - profit)/2) FROM games_logs WHERE loser = '{user_id}'
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def add_jackpot_bet(user_id, bet):
    if get_jackpot_bet(user_id) == None:
        if len(get_jackpot_bets()) == 1:
            update_jackpot_end_time(time.time() + 120)
        db = sqlite3.connect('data/database.db')
        cursor = db.cursor()
        bet = [user_id, bet]
        cursor.execute(f'''INSERT INTO jackpot_bets VALUES(?,?)''', bet)
        db.commit()
    else:
        db = sqlite3.connect('data/database.db')
        cursor = db.cursor()
        cursor.execute(f'''UPDATE jackpot_bets SET bet = bet + '{bet}' WHERE user_id = '{user_id}' ''')
        db.commit()


def get_jackpot_end_time():
    db = sqlite3.connect('data/database.db')
    
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM jackpot_game """)
    
    db.close()
    row = cursor.fetchone()[0]
    return row


def update_jackpot_end_time(end_time):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''UPDATE jackpot_game SET end_time = '{end_time}' ''')
    db.commit()


def get_jackpot_bets():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM jackpot_bets """)
    row = cursor.fetchall()
    return row


def get_jackpot_bet(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM jackpot_bets WHERE user_id = '{user_id}' """)
    row = cursor.fetchone()
    return row


def get_jackpot_bets_amount():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM jackpot_bets ''')
    row = cursor.fetchone()[0]
    return row


def delete_jackpot_bets():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''DELETE FROM jackpot_bets''')
    db.commit()


def get_user_jackpot_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM jackpot_logs WHERE winner = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_jackpot_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM jackpot_logs WHERE winner = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_game_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(player) FROM slots_logs WHERE player = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_game_bet_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM slots_logs WHERE player = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(win_amount) FROM slots_logs WHERE player = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(win_amount) FROM slots_logs WHERE player = '{user_id}' AND win_amount = 0 ''')
    row = cursor.fetchone()[0]
    return row
