import telebot
import random
import os

TOKEN = '8613717747:AAFdi1AU7e-jdACCXl1KfHW8PqQ4036F2dc' 
MY_ID = 8322888745 # Твой ID

bot = telebot.TeleBot(TOKEN)
questions = {}
STATUS_FILE = "sleep_status.txt" 

def save_sleep_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write("1" if status else "0")

def get_sleep_status():
    if not os.path.exists(STATUS_FILE):
        return False
    with open(STATUS_FILE, "r") as f:
        return f.read() == "1"


@bot.message_handler(commands=['sleep'], func=lambda m: m.from_user.id == MY_ID)
def toggle_sleep(message):
    current_status = get_sleep_status()
    new_status = not current_status
    save_sleep_status(new_status)
    
    status_text = "🌙 Спящий режим ВКЛЮЧЕН. Теперь я буду говорить всем, что отдыхаю." if new_status else "☀️ Спящий режим ВЫКЛЮЧЕН. Работаю как надо!"
    bot.reply_to(message, status_text)


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith("рубибот рандом"))
def ruby_random(message):
    try:
        lines = message.text.split('\n')
        options = [l.strip() for l in lines[1:] if l.strip()]
        if not options:
            bot.reply_to(message, "ало ало завелись дебилы, варианты напиши с новой строчки пж")
            return
        winner = random.choice(options)
        intros = [
            f"🔮 Моя интуиция подсказывает: **{winner}**",
            f"🎰 Выпало: **{winner}**",
            f"🌟 Звезды сошлись на варианте: **{winner}**",
            f"🎲 Рандом выбрал: **{winner}**"
        ]
        bot.reply_to(message, random.choice(intros), parse_mode="Markdown")
    except Exception: pass


@bot.message_handler(commands=['rick'])
def rick(message):
    bot.send_animation(message.chat.id, "https://media.giphy.com/media/Vuw9m5wXviFIQ/giphy.gif")


@bot.message_handler(func=lambda m: m.chat.id != MY_ID, content_types=['text', 'photo', 'sticker', 'video', 'animation', 'voice'])
def handle_messages(message):
    msg_text = (message.text or message.caption or "").lower()

    if "рубибот" in msg_text:

        if get_sleep_status():
            bot.reply_to(message, "💤 Рубибот сейчас спит... отвечу позже!")


        try:
            sent_msg = bot.copy_message(MY_ID, message.chat.id, message.message_id)
            questions[sent_msg.message_id] = {'chat_id': message.chat.id, 'orig_msg_id': message.message_id}
            
            chat_title = message.chat.title if message.chat.title else "Личка"
            user_name = message.from_user.first_name
            bot.send_message(MY_ID, f"🌟 От: {user_name} | Чат: '{chat_title}'", reply_to_message_id=sent_msg.message_id)
        except Exception: pass


@bot.message_handler(func=lambda m: m.reply_to_message and m.chat.id == MY_ID)
def answer_logic(message):
    data = questions.get(message.reply_to_message.message_id)
    if data:
        bot.copy_message(data['chat_id'], MY_ID, message.message_id, reply_to_message_id=data['orig_msg_id'])
        bot.send_message(MY_ID, "✅ Ушло в группу!")

bot.polling(none_stop=True)
