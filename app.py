import asyncio,aioschedule,sqlite3,random

from aiogram import executor

from middlewares import setup_middlewares
from data.functions.functions import game_time
from handlers import dp
from loader import bot
from config import config
from data.functions.db import update_balance,add_game_log,info_participate,delete_participate
from keyboards.inline.other_keyboards import participate


async def on_startup(dp):
    asyncio.create_task(scheduler2())

async def scheduler2():
    aioschedule.every().day.at("12:00").do(main_func)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def main_func():
    print("stating...")
    try:
        info = 'Не учавствуешь'
        
        participate_before = await info_participate()
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        result = c.execute(f"SELECT * FROM `users_participate` ORDER BY RANDOM() LIMIT 1;").fetchone()
        count_users = c.execute(f"SELECT * FROM `users_participate`").fetchall()
        prize = int(open("wheel_of_fortune.txt","r").readline())*len(count_users)

        coms = 1 - (float(config('game_percent')) * 0.01)
        win = round(float(prize*coms))
        profit = prize - win
        print(f"Profit: {profit} Win: {win}")
        add_game_log(random.randint(1,1000000), result[0], "0", prize, profit, "wheel")
        update_balance(result[0], win)
        
        await delete_participate()
        participate_after = await info_participate()
        await bot.send_message(result[0],f'''
🥳 Поздравляю! Ты выйграл приз размером в {win}₽!
❗️ Новая рулетка уже запущена, скорей учавствуй, тебе и в этот раз тоже повезет!

👤 Участников: {len(participate_after)}
⚡️ Твой статус: {info}
    ''', reply_markup=participate())
        
        for row in participate_before:
            
            if(row[0] != result[0]):
                await bot.send_message(row[0],f'''
🅱️ К сожалению ты не выйграл в колесе фортуны :(
😮‍💨 Выйграл пользователь с ID: {result[0]} приз размером в {win}₽

❗️ Новая рулетка уже запущена, скорей учавствуй в этот раз тебе повезет!

👤 Участников: {len(participate_after)}
⚡️ Твой статус: {info}
    ''', reply_markup=participate())
    except Exception as err:
        print(err)
    print("finish...")

if __name__ == "__main__":
    setup_middlewares(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(game_time(bot))
    executor.start_polling(dp,on_startup=on_startup)
