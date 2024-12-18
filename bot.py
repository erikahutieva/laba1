#Класс описывает, как будет устроен объект. Он определяет свойства (переменные) и методы (функции), которые объект этого класса будет иметь.
#Объект — это экземпляр (реализация) класса. Он создается на основе класса и имеет все свойства и методы, описанные в этом классе.
import urllib3  
import telebot  
from MukeshAPI import api 
from gtts import gTTS  #  Google Text-to-Speech для создания аудиофайлов из текста, использует записанные фрагменты речи, соединяя их в нужном порядке для создания слов и предложений.
import threading  #  для многопоточного выполнения кода


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

REPO_URL = 'https://github.com/erikahutieva/laba1' 
TOKEN = '7791332578:AAEmhl_Ws9aVfnXo14ocQziTx0_OW9uDSsM'
bot = telebot.TeleBot(TOKEN)  # TeleBot класс из библиотеки telebot для взаимодействия с Telegram API
#Создание объекта bot  позволяет боту получать сообщения и отправлять ответы пользователям. 
START_BTNS = [
    ["Генерировать изображение", "generate_image"],  
]


running = True


def start_polling():
    global running  
    while running:  # выполняем бесконечный цикл
        try:
            bot.polling(none_stop=True)  
        except Exception as e:
            print(f"Ошибка при запуске: {e}")  # 
            bot.stop_polling()  

# создает и запускает отдельный поток для выполнения функции start_polling, которая отвечает за постоянный polling (опрос) сообщений от Telegram.

polling_thread = threading.Thread(target=start_polling)
polling_thread.start()


def gen_img(msg):#это объект сообщения, передаваемый из Telegram
    bot.clear_step_handler_by_chat_id(msg.chat.id)  #  для сброса текущих шагов и предотвращения конфликта обработчиков (например, если уже ожидался другой ввод от пользователя).
    try:
        img = api.ai_image(msg.text)  #  MukeshAPI для генерации изображения
        bot.send_photo(msg.chat.id, img, caption=msg.text)  # Отправляем изображение в чат вместе с отправленным текстом
    except Exception as e:
        print(f"Ошибка: {e}") 
        bot.send_message(msg.chat.id, "Не удалось отправить изображение") 

    keyboard = telebot.types.InlineKeyboardMarkup()# Создаем клавиатуру с кнопками действий
    for btn_text, btn_callback in START_BTNS:  
        keyboard.add(telebot.types.InlineKeyboardButton(text=btn_text, callback_data=btn_callback))#добавляем текст и действие
    bot.send_message(msg.chat.id, "Выберите действие:", reply_markup=keyboard)  # Отправляем клавиатуру пользователю


def gen_audio(msg):
    bot.clear_step_handler_by_chat_id(msg.chat.id)  
    try:
        tts = gTTS(text=msg.text, lang='en')  # Создаем аудио из текста с помощью gTTS, можно ru для русского
        tts.save("laba1.mp3") 
        
        # Открываем файл и отправляем его в чат
        with open("laba1.mp3", "rb") as f: #read binary
            bot.send_audio(chat_id=msg.chat.id, audio=f)  
    except Exception as ex:
        bot.send_message(msg.chat.id, f"Не удалось отправить аудио: {ex}")  


@bot.message_handler(commands=['start'])
def start_handler(msg):
    keyboard = telebot.types.InlineKeyboardMarkup() 
    for btn_text, btn_callback in START_BTNS: 
        keyboard.add(telebot.types.InlineKeyboardButton(text=btn_text, callback_data=btn_callback))
    bot.send_message(msg.chat.id, "Выберите действие:", reply_markup=keyboard) 


@bot.message_handler(commands=['gen_audio'])
def gen_audio_handler(msg):
    bot.send_message(msg.chat.id, "Отправьте текст для преобразования в аудио.") 
    bot.register_next_step_handler(msg, gen_audio) 


@bot.message_handler(commands=['repo'])
def repo_handler(msg):
    bot.send_message(msg.chat.id, f"Cсылка на репозиторий: {REPO_URL}")  # Отправляем ссылку на репозиторий

# Обработчик команды /stop для остановки бота
@bot.message_handler(commands=['stop'])
def stop_handler(msg):
    global running  
    bot.send_message(msg.chat.id, "Бот отключен.")  
    running = False  # чтобы остановить цикл polling
    bot.stop_polling()  # Останавливаем polling в telebot


@bot.message_handler(content_types=['text'])
def text_handler(msg):
    if msg.text.startswith("Генерировать изображение"): 
        bot.send_message(msg.chat.id, "Отправьте текст для генерации изображения.") 
        bot.register_next_step_handler(msg, gen_img) 
    else:
        bot.send_message(msg.chat.id, "Неизвестная команда. Используйте /gen_audio для генерации аудио, /repo для получения репозитория или /stop для остановки бота")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "generate_image":  # Если callback_data равна "generate_image"
        bot.send_message(call.message.chat.id, "Отправьте текст для генерации изображения.")
        bot.register_next_step_handler(call.message, gen_img)  




'''
Основные свойства:
TOKEN: Этот токен передается при создании объекта bot и используется для аутентификации с Telegram API.

last_update_id: Свойство, используемое для отслеживания последних обновлений. Оно помогает избежать обработки одних и тех же сообщений несколько раз.

update_listener: Позволяет установить пользовательскую функцию, которая будет вызываться при каждом получении нового сообщения. Это полезно, если нужно обрабатывать сообщения нестандартным образом.

Основные методы:
send_message(chat_id, text, **kwargs): Отправляет сообщение пользователю или в группу.
reply_to(message, text, **kwargs): Отвечает на конкретное сообщение пользователя.
edit_message_text(...): Изменяет текст уже отправленного сообщения.
delete_message(chat_id, message_id): Удаляет сообщение из чата.
get_me(): Возвращает информацию о боте (например, его имя и имя пользователя).
get_updates(): Получает обновления (сообщения и события) от сервера Telegram.
polling(): Запускает бесконечный цикл, который проверяет новые сообщения и обрабатывает их.
stop_polling(): Останавливает опрос сообщений.
set_webhook(url=None, certificate=None, max_connections=None, allowed_updates=None): Устанавливает Webhook для взаимодействия с сервером.
delete_webhook(): Удаляет установленный Webhook.
get_chat(chat_id): Получает информацию о чате.
get_chat_administrators(chat_id): Возвращает список администраторов чата.
get_chat_member(chat_id, user_id): Возвращает информацию об участнике чата.
get_chat_members_count(chat_id): Возвращает количество участников в чате.
send_photo(chat_id, photo, **kwargs): Отправляет фото в чат.
send_audio(chat_id, audio, **kwargs): Отправляет аудио в чат.
send_document(chat_id, document, **kwargs): Отправляет документ в чат.
send_video(chat_id, video, **kwargs): Отправляет видео в чат.
send_voice(chat_id, voice, **kwargs): Отправляет голосовое сообщение.
send_location(chat_id, latitude, longitude, **kwargs): Отправляет местоположение.
send_poll(chat_id, question, options, **kwargs): Отправляет опрос в чат.
Обработчики событий:
@bot.message_handler(commands=['start', 'help']): Декоратор для обработки команд.
@bot.message_handler(func=lambda message: True): Декоратор для обработки всех типов сообщений.

'''