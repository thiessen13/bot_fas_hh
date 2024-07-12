from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Final
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup

TOKEN: Final = "6509875211:AAH4TAmJNHjN0ReEorby4YBx6FKCr1ia-y8"
BOT_NAME: Final = '@coven_budget_bot'
ASKING_MESSAGE, ASKING_LANGUAGE = range(2)
# anastas as an admin
ADMIN_ID: Final = '328310817'

# language
user_lang = {}
language_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton('Немецкий'), KeyboardButton('Русский')]
], resize_keyboard=True)

# inline menu keyboards
inline_keyboard_de = [
    [
        InlineKeyboardButton("Ich möchte Mitglied werden", callback_data="join"),
    ],
    [InlineKeyboardButton("Ich möchte eine Zusammenarbeit vorschlagen", callback_data="cooperate")],
    [InlineKeyboardButton("Ich möchte eine Frage stellen", callback_data="question")], 

]

inline_keyboard_ru = [
    [
        InlineKeyboardButton("Хочу стать участниц:ей", callback_data="join"),
    ],
    [InlineKeyboardButton("Хочу предложить сотрудничество", callback_data="cooperate")],
    [InlineKeyboardButton("Хочу задать вопрос", callback_data="question")], 
]

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    user_lang[user_id] = update.message.text.lower()
    
    if user_lang[user_id] == 'немецкий':
        await update.message.reply_text('Du hast Deutsch gewählt.')
        await update.message.reply_text("Bitte wählen Sie:", reply_markup=InlineKeyboardMarkup(inline_keyboard_de))
    elif user_lang[user_id] == 'русский':
        await update.message.reply_text('Вы выбрали русский язык.')
        await update.message.reply_text("Пожалуйста, выберите:", reply_markup=InlineKeyboardMarkup(inline_keyboard_ru))
    else:
        await update.message.reply_text('Пожалуйста, выберите язык с помощью клавиатуры.')
        return ASKING_LANGUAGE

    return ASKING_MESSAGE

async def handle_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if user_lang.get(user_id) == 'немецкий':
        await query.edit_message_text(text="Ausgezeichnet, danke")
        await query.message.reply_text("Jetzt schreiben Sie bitte, was Sie möchten")
    elif user_lang.get(user_id) == 'русский':
        await query.edit_message_text(text="Отлично, спасибо")
        await query.message.reply_text("Теперь напишите, что вы хотите")

# define commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Выберите язык:', reply_markup=language_keyboard)
    return ASKING_LANGUAGE

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'используйте команды /start, /help или напишите сообщение боту.')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.Regex(
    r'^Немецкий$|^Русский$'), handle_language))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Действие отменено.')
    return ConversationHandler.END

# forward message to an admin
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_message = update.message.text
    user_id = update.message.from_user.id

    # Пересылка сообщения администратору
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"Сообщение от ник: {update.effective_user.name} имя: {update.effective_user.first_name} сообщение: {user_message} ")
    
    if user_lang.get(user_id) == 'немецкий':
        await update.message.reply_text('Ihre Nachricht wurde de:r Administrator:in gesendet.')
    elif user_lang.get(user_id) == 'русский':
        await update.message.reply_text('Сообщение переслано администратор:ке. Спасибо!')

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASKING_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language)],
        ASKING_MESSAGE: [CallbackQueryHandler(handle_inline_button), MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# add commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CallbackQueryHandler(handle_inline_button))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(conv_handler)

# run
app.run_polling()