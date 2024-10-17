import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext



TOKEN = '7791332578:AAEmhl_Ws9aVfnXo14ocQziTx0_OW9uDSsM'


REPO_URL = 'https://github.com/erikahutieva/laba1'


IMAGE_PATH = './image.jpg'
AUDIO_PATH = './audio.mp3'
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
        context.bot.send_photo(chat_id=query.message.chat_id, photo=open(IMAGE_PATH, 'rb'))

def get_audio(update: Update, context: CallbackContext) -> None:
    context.bot.send_audio(chat_id=update.message.chat_id, audio=open(AUDIO_PATH, 'rb'))

def get_repo_link(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Ссылка на репозиторий: {REPO_URL}')

def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("get_audio", get_audio))
    dispatcher.add_handler(CommandHandler("get_repo_link", get_repo_link))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()