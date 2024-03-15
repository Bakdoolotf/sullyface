# - *- coding: utf- 8 - *-
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update



# Проверка юзеров в БД и его добавление

def clear_html(get_text):
    if get_text is not None:
        if "<" in get_text: get_text = get_text.replace("<", "*")
        if ">" in get_text: get_text = get_text.replace(">", "*")

    return get_text
class ExistsUserMiddleware(BaseMiddleware):
    def __init__(self):
        self.prefix = "key_prefix"
        super(ExistsUserMiddleware, self).__init__()

    async def on_process_update(self, update: Update, data: dict):
        if "message" in update:
            this_user = update.message.from_user
        elif "callback_query" in update:
            this_user = update.callback_query.from_user
        else:
            this_user = None

        '''if this_user is not None:
            get_settings = get_settingsx()
            get_prefix = self.prefix

            if get_settings['status_work'] == "False" or this_user.id in get_admins():
                if not this_user.is_bot:
                    get_user = get_userx(user_id=this_user.id)

                    user_id = this_user.id
                    user_login = this_user.username
                    user_name = clear_html(this_user.first_name)

                    if user_login is None: user_login = ""

                    if get_user is None:
                        await send_admins(f'💎 Зарегистрирован новый пользователь @{user_login}')
                   # else:

                        #if user_name != get_user['user_name']:
                        #    update_userx(get_user['user_id'], user_name=user_name)

                        #if len(user_login) >= 1:
                        #    if user_login != get_user['user_login']:
                        #        update_userx(get_user['user_id'], user_login=user_login)
                        #else:
                        #    update_userx(get_user['user_id'], user_login="")
                            '''
