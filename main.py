import telebot

# --- ДАННЫЕ ---
TOKEN = '8613717747:AAFdi1AU7e-jdACCXl1KfHW8PqQ4036F2dc'
MY_ID = 8322888745 # <--- ТВОЙ ID
# --------------

bot = telebot.TeleBot(TOKEN)

# Хранилище для связки сообщений (чтобы бот знал, куда отвечать)
questions = {}

@bot.message_handler(func=lambda m: m.text and "рубибот" in m.text.lower())
def forward_to_ruby(message):
    try:
        # Пересылаем сообщение
        sent_msg = bot.forward_message(MY_ID, message.chat.id, message.message_id)
        
        # Запоминаем: ID сообщения в твоей личке = ID группы
        questions[sent_msg.message_id] = message.chat.id
        
        bot.send_message(MY_ID, f"🌟 Вопрос из чата '{message.chat.title}'", reply_to_message_id=sent_msg.message_id)
    except Exception as e:
        print(f"Ошибка: {e}")

@bot.message_handler(func=lambda m: m.reply_to_message is not None and m.chat.id == MY_ID)
def answer_to_group(message):
    try:
        # Ищем ID чата в нашем словаре по ID сообщения, на которое ты отвечаешь
        original_msg_id = message.reply_to_message.message_id
        target_chat_id = questions.get(original_msg_id)

        # Если в словаре не нашли, пробуем достать из пересланного (на всякий случай)
        if not target_chat_id:
            if message.reply_to_message.forward_from_chat:
                target_chat_id = message.reply_to_message.forward_from_chat.id
            elif message.reply_to_message.forward_from:
                target_chat_id = message.reply_to_message.forward_from.id

        if target_chat_id:
            bot.send_message(target_chat_id, message.text)
            bot.send_message(MY_ID, "✅ Улетело в группу!")
        else:
            bot.send_message(MY_ID, "❌ Не понял куда слать. Попробуй ответить на само пересланное сообщение.")
            
    except Exception as e:
        bot.send_message(MY_ID, f"❌ Ошибка: {e}")

bot.polling(none_stop=True)
