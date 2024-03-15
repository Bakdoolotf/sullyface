from aiogram.types import ReplyKeyboardMarkup


def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    #keyboard.row("🃏21 очко", "🀄️Baccara")
    #keyboard.row("🕹Игры", "🎰 Слоты")
    keyboard.row("🕹Играть")
    keyboard.row("🖥 Кабинет‍")
    #keyboard.row("🌴Отзывы🌴", "📚 Помощь" ,"💬CHAT 💬")
    keyboard.row("💬CHAT 💬","👥 Партнёрка")
    return keyboard


def play_slots_keyboard(bet):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"📍 Крутить | Ставка: {bet}")
    keyboard.row("🔁 Изменить ставку", "⏪ Выход")
    return keyboard

