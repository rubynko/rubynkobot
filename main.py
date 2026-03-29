import telebot
import random

# --- НАСТРОЙКИ (Впиши свои данные!) ---
TOKEN = '8613717747:AAFdi1AU7e-jdACCXl1KfHW8PqQ4036F2dc' 
MY_ID = 8322888745 # Твой ID (узнай в @getmyid_bot)
# --------------------------------------

bot = telebot.TeleBot(TOKEN)
questions = {}
is_sleeping = False # Статус спящего режима

# --- 1. УПРАВЛЕНИЕ СПЯЩИМ РЕЖИМОМ (ТОЛЬКО ДЛЯ ТЕБЯ) ---
@bot.message_handler(commands=['sleep'], func=lambda m: m.from_user.id == MY_ID)
def toggle_sleep(message):
    global is_sleeping
    is_sleeping = not is_sleeping
    status = "🌙 Спящий режим ВКЛЮЧЕН. Теперь я буду говорить всем, что отдыхаю!." if is_sleeping else "☀️ Спящий режим ВЫКЛЮЧЕН. Работаю в штатном режиме!"
    bot.reply_to(message, status)

# --- 2. КОМАНДА: РУБИБОТ РАНДОМ (С КРАСИВЫМИ ВСТУПЛЕНИЯМИ) ---
@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith("рубибот рандом"))
def ruby_random(message):
    try:
        lines = message.text.split('\n')
        options = [l.strip() for l in lines[1:] if l.strip()]
        
        if not options:
            bot.reply_to(message, "Варианты с новой строчки после 'Рубибот рандом', плез! ✨")
            return
            
        winner = random.choice(options)
        
        # Возвращаем те самые варианты вступлений
        intros = [
            f"🔮 Моя интуиция подсказывает: **{winner}**",
            f"🎰 Выпало: **{winner}**",
            f"🌟 Звезды сошлись на варианте: **{winner}**",
            f"🎲 Рандом выбрал: **{winner}**"
        ]
        
        bot.reply_to(message, random.choice(intros), parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка в рандоме: {e}")

# --- 3. РИКРОЛЛ ---
@bot.message_handler(commands=['rick'])
def rick(message):
    bot.send_animation(message.chat.id, "https://media.giphy.com/media/Vuw9m5wXviFIQ/giphy.gif")

# --- 4. ОСНОВНАЯ ЛОГИКА: ПЕРЕСЫЛКА (МЕДИА + ИНФО О ЧАТЕ) ---
@bot.message_handler(func=lambda m: m.chat.id != MY_ID, content_types=['text', 'photo', 'sticker', 'video', 'animation', 'voice'])
def handle_messages(message):
    msg_text = ""
    if message.text: msg_text = message.text.lower()
    elif message.caption: msg_text = message.caption.lower()

    if "рубибот" in msg_text:
        # Если включен спящий режим — бот отвечает, что спит, НО продолжает код дальше
        if is_sleeping:
            bot.reply_to(message, "💤 Рубибот сейчас спит... отвечу позже!")

        # Пересылка сообщения тебе (даже если бот спит!)
        try:
            # Сначала отправляем само медиа/текст
            sent_msg = bot.copy_message(MY_ID, message.chat.id, message.message_id)
            questions[sent_msg.message_id] = {'chat_id': message.chat.id, 'orig_msg_id': message.message_id}
            
            # Добавляем инфо, от кого и откуда пришло (возвращаем эту фичу)
            chat_title = message.chat.title if message.chat.title else "Личка"
            user_name = message.from_user.first_name
            bot.send_message(MY_ID, f"🌟 От: {user_name} | Чат: '{chat_title}'", reply_to_message_id=sent_msg.message_id)
            
        except Exception as e:
            print(f"Ошибка пересылки: {e}")

# --- 5. ТВОЙ ОТВЕТ ИЗ ЛИЧКИ В ГРУППУ ---
@bot.message_handler(func=lambda m: m.reply_to_message and m.chat.id == MY_ID)
def answer_logic(message):
    # Ищем в памяти, на какое сообщение ты отвечаешь
    data = questions.get(message.reply_to_message.message_id)
    if data:
        bot.copy_message(data['chat_id'], MY_ID, message.message_id, reply_to_message_id=data['orig_msg_id'])
        bot.send_message(MY_ID, "✅ Улетело в группу!")

bot.polling(none_stop=True)
