
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext



TOKEN = '7791332578:AAEmhl_Ws9aVfnXo14ocQziTx0_OW9uDSsM'


REPO_URL = 'https://github.com/erikahutieva/laba1'


IMAGE_PATH = 'https://ru.wikipedia.org/wiki/%D0%A2%D0%B8%D0%B3%D1%80#/media/%D0%A4%D0%B0%D0%B9%D0%BB:P.t.altaica_Tomak_Male.jpg'
AUDIO_PATH = 'https://d12.drivemusic.me/dl/l2gUEBPSyHDjzXGh-GbzzA/1729204227/download_music/2015/06/vivaldi-vremena-goda-leto.mp3'
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Получить изображение", callback_data='get_image')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'get_image':
        context.bot.send_photo(chat_id=query.message.chat_id, photo=IMAGE_PATH)

def get_audio(update: Update, context: CallbackContext) -> None:
      context.bot.send_audio(chat_id=update.message.chat_id, audio=AUDIO_PATH)

def get_repo_link(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Ссылка на репозиторий: {REPO_URL}')

def stop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Бот остановлен")
    context.bot_data['updater'].stop()

def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.bot_data['updater'] = updater

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("get_audio", get_audio))
    dispatcher.add_handler(CommandHandler("get_repo_link", get_repo_link))
    dispatcher.add_handler(CommandHandler("stop", stop))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()