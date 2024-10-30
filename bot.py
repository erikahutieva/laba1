import requests
import urllib3
from pydub.generators import Sine
import telebot
from MukeshAPI import api
from gtts import gTTS
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

REPO_URL = 'https://github.com/erikahutieva/laba1'
# Ваш токен от BotFather
TOKEN = '7791332578:AAEmhl_Ws9aVfnXo14ocQziTx0_OW9uDSsM'
bot = telebot.TeleBot(TOKEN)

START_BTNS = [
    ["Генерировать изображение", "generate_image"],
]

# Flag for bot status
running = True

# Polling in a separate thread
def start_polling():
    global running
    while running:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка при запуске: {e}")
            bot.stop_polling()

# Start polling in a thread
polling_thread = threading.Thread(target=start_polling)
polling_thread.start()

# Функция генерации изображения
def gen_img(msg):
    bot.clear_step_handler_by_chat_id(msg.chat.id)
    try:
        img = api.ai_image(msg.text)  # Генерация изображения через MukeshAPI
        bot.send_photo(msg.chat.id, img, caption=msg.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(msg.chat.id, "Не удалось отправить изображение")

    # Создание клавиатуры
    keyboard = telebot.types.InlineKeyboardMarkup()
    for btn_text, btn_callback in START_BTNS:
        keyboard.add(telebot.types.InlineKeyboardButton(text=btn_text, callback_data=btn_callback))
    bot.send_message(msg.chat.id, "Выберите действие:", reply_markup=keyboard)

# Функция генерации аудио из текста
def gen_audio(msg):
    bot.clear_step_handler_by_chat_id(msg.chat.id)
    try:
        # Генерация аудио из текста
        tts = gTTS(text=msg.text, lang='en')
        tts.save("req.mp3")
        
        # Отправка сгенерированного аудио в Telegram чат
        with open("req.mp3", "rb") as f:
            bot.send_audio(chat_id=msg.chat.id, audio=f)
    except Exception as ex:
        bot.send_message(msg.chat.id, f"Не удалось отправить аудио: {ex}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(msg):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for btn_text, btn_callback in START_BTNS:
        keyboard.add(telebot.types.InlineKeyboardButton(text=btn_text, callback_data=btn_callback))
    bot.send_message(msg.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=keyboard)

# Обработчик команды /gen_audio для генерации аудио
@bot.message_handler(commands=['gen_audio'])
def gen_audio_handler(msg):
    bot.send_message(msg.chat.id, "Отправьте текст для преобразования в аудио.")
    bot.register_next_step_handler(msg, gen_audio)

# Обработчик команды /repo для получения ссылки на репозиторий
@bot.message_handler(commands=['repo'])
def repo_handler(msg):
    bot.send_message(msg.chat.id, f"Вот ссылка на репозиторий: {REPO_URL}")

# Обработчик команды /stop для остановки бота
@bot.message_handler(commands=['stop'])
def stop_handler(msg):
    global running
    bot.send_message(msg.chat.id, "Бот отключен.")
    running = False
    bot.stop_polling()  # Stop polling to break the loop

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def text_handler(msg):
    if msg.text.startswith("Генерировать изображение"):
        bot.send_message(msg.chat.id, "Отправьте текст для генерации изображения.")
        bot.register_next_step_handler(msg, gen_img)
    else:
        # Сообщение, если текст не распознан как команда
        bot.send_message(msg.chat.id, "Неизвестная команда. Используйте /gen_audio для генерации аудио или /repo для получения репозитория.")

# Обработчик обратного вызова для клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "generate_image":
        bot.send_message(call.message.chat.id, "Отправьте текст для генерации изображения.")
        bot.register_next_step_handler(call.message, gen_img)
