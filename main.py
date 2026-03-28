import telebot

# --- ДАННЫЕ ---
TOKEN = '8613717747:AAFdi1AU7e-jdACCXl1KfHW8PqQ4036F2dc'
MY_ID = 8322888745 # Твой ID
# --------------

bot = telebot.TeleBot(TOKEN)

# Хранилище: ID в личке бота -> {chat_id: ID группы, msg_id: ID сообщения в группе}
questions = {}

@bot.message_handler(func=lambda m: m.text and "рубибот" in m.text.lower())
def forward_to_ruby(message):
    try:
        # Пересылаем сообщение Руби
        sent_msg = bot.forward_message(MY_ID, message.chat.id, message.message_id)
        
        # Сохраняем и ID чата, и ID конкретного сообщения
        questions[sent_msg.message_id] = {
            'chat_id': message.chat.id,
            'orig_msg_id': message.message_id
        }
        
        bot.send_message(MY_ID, f"🌟 Вопрос из чата '{message.chat.title}'", reply_to_message_id=sent_msg.message_id)
    except Exception as e:
        print(f"Ошибка: {e}")

@bot.message_handler(func=lambda m: m.reply_to_message is not None and m.chat.id == MY_ID)
def answer_to_group(message):
    try:
        original_msg_id = message.reply_to_message.message_id
        data = questions.get(original_msg_id)

        if data:
            # Отправляем ответ в группу как REPLY на исходное сообщение
            bot.send_message(
                data['chat_id'], 
                message.text, 
                reply_to_message_id=data['orig_msg_id']
            )
            bot.send_message(MY_ID, "✅ Улетело в группу с реплаем!")
        else:
            # Если в словаре нет (например, бот перезагрузился), шлем просто так
            if message.reply_to_message.forward_from_chat:
                bot.send_message(message.reply_to_message.forward_from_chat.id, message.text)
                bot.send_message(MY_ID, "✅ Отправлено без реплая (память очистилась)")
            
    except Exception as e:
        bot.send_message(MY_ID, f"❌ Ошибка: {e}")
        
# --- ОБРАБОТЧИК ВСТУПЛЕНИЯ В ГРУППУ ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_bot(message):
    for user in message.new_chat_members:
        # Проверяем, что в чат добавили именно нашего бота
        if user.id == bot.get_me().id:
            try:
                # Ссылка на твой арт или любую картинку
                photo_url = 'https://i.pinimg.com/736x/83/04/c7/8304c70b08c191656de22d3dc5e2b702.jpg' 
                
                caption_text = (
                    "Привет!! Я - Рубибот, роботизированная версия Руби. \n\n"
                    "Я РЕАЛЬНО мощный чат-менеджер. Если есть вопросы - "
                    "просто напиши в чате 'Рубибот [твой вопрос]', и я отвечу!"
                )
                
                # Отправляем фото с подписью
                bot.send_photo(message.chat.id, photo_url, caption=caption_text)
                print(f"Поприветствовал чат: {message.chat.title}")
            except Exception as e:
                # Если с картинкой беда, просто шлем текст
                bot.send_message(message.chat.id, "Привет! Я Рубибот, и я тут самый ахуенный. Вопросы?")
                print(f"Ошибка в приветствии: {e}")

bot.polling(none_stop=True)
