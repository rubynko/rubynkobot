import telebot

# --- НАСТРОЙКИ ---
TOKEN = '8613717747:AAFdi1AU7e-jdACCXl1KfHW8PqQ4036F2dc' # Твой токен
MY_ID = 8322888745 # <--- ЗАМЕНИ ЭТИ ЦИФРЫ НА СВОЙ ID ИЗ @getmyid_bot
# -----------------

bot = telebot.TeleBot(TOKEN)

# 1. Ловим слово "рубибот" в группе
@bot.message_handler(func=lambda m: m.text and "рубибот" in m.text.lower())
def forward_to_ruby(message):
    try:
        # Пересылаем само сообщение тебе в личку
        bot.forward_message(MY_ID, message.chat.id, message.message_id)
        bot.send_message(MY_ID, f"☝️ Руби, в чате '{message.chat.title}' вопрос!")
    except Exception as e:
        print(f"Ошибка пересылки: {e}")

# 2. Твой ответ в личке бота отправляется обратно в группу
@bot.message_handler(func=lambda m: m.reply_to_message is not None)
def send_answer(message):
    try:
        # Пытаемся понять, откуда пришло сообщение (из группы или лички)
        if message.reply_to_message.forward_from_chat:
            target_id = message.reply_to_message.forward_from_chat.id
        elif message.reply_to_message.forward_from:
            target_id = message.reply_to_message.forward_from.id
        else:
            return # Если это не пересланное сообщение, ничего не делаем

        bot.send_message(target_id, message.text)
        bot.send_message(MY_ID, "✅ Ответ отправлен!")
    except Exception as e:
        bot.send_message(MY_ID, f"❌ Не удалось отправить: {e}")

print("Рубибот запущен и слушает чаты...")
bot.polling(none_stop=True)
