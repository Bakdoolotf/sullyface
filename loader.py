import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.dispatcher.fsm.strategy import FSMStrategy

from config import config

bot = Bot(token=config("bot_token"), parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)#, fsm_strategy=FSMStrategy.CHAT

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
