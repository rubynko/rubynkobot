import telebot
import random

# --- НАСТРОЙКИ ---
TOKEN = '8613717747:AAFdi1AU7e-jdACCXl1KfHW8PqQ4036F2dc'
MY_ID = 8322888745 # Твой ID

bot = telebot.TeleBot(TOKEN)
questions = {}

# --- КОМАНДА: РУБИБОТ РАНДОМ ---
@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith("рубибот рандом"))
def ruby_random(message):
    try:
        # Убираем саму фразу "рубибот рандом" из текста
        raw_text = message.text.lower().replace("рубибот рандом", "").strip()
        
        # Разбиваем текст на строки и убираем лишние пробелы
        options = [line.strip() for line in raw_text.split('\n') if line.strip()]
        
        if not options:
            bot.reply_to(message, "Эй, а где варианты? Напиши их с новой строчки после 'Рубибот рандом'! ✨")
            return
            
        # Выбираем случайный вариант
        winner = random.choice(options)
        
        # Красивый ответ
        responses = [
            f"🔮 Моя интуиция подсказывает: **{winner}**",
            f"🎰 Выпало: **{winner}**",
            f"🌟 Звезды сошлись на варианте: **{winner}**",
            f"🎲 Рандом выбрал: **{winner}**"
        ]
        
        bot.reply_to(message, random.choice(responses), parse_mode="Markdown")
        
    except Exception as e:
        print(f"Ошибка в рандоме: {e}")

# --- КЛАССИЧЕСКИЙ РИКРОЛЛ ---
@bot.message_handler(commands=['rick'])
def rick(message):
    bot.send_animation(message.chat.id, "https://media.giphy.com/media/Vuw9m5wXviFIQ/giphy.gif", caption="Never gonna give you up! 🎶")

# --- ЛОГИКА ПЕРЕСЫЛКИ (РУБИ) ---
@bot.message_handler(func=lambda m: m.text and "рубибот" in m.text.lower() and not m.text.lower().startswith("рубибот рандом") and m.chat.id != MY_ID)
def forward_logic(message):
    sent_msg = bot.forward_message(MY_ID, message.chat.id, message.message_id)
    questions[sent_msg.message_id] = {'chat_id': message.chat.id, 'orig_msg_id': message.message_id}
    bot.send_message(MY_ID, f"🌟 Вопрос из '{message.chat.title}'", reply_to_message_id=sent_msg.message_id)

@bot.message_handler(func=lambda m: m.reply_to_message and m.chat.id == MY_ID)
def answer_logic(message):
    data = questions.get(message.reply_to_message.message_id)
    if data:
        bot.send_message(data['chat_id'], message.text, reply_to_message_id=data['orig_msg_id'])

bot.polling(none_stop=True)
