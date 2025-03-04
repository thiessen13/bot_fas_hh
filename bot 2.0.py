from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Final
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup


# constants

TOKEN: Final = "7113973054:AAEEkPm8E8TFq3YGj7cswPt9drH7TbQRjVk"
BOT_NAME: Final = '@far_hamburg_bot'
ASKING_MESSAGE, ASKING_LANGUAGE = range(2)
# anastas as an admin
ADMIN_ID: Final = '328310817'
GROUP_ID: Final = '-4757667404'
#####################################################################

# language keyboard

user_lang = {}
language_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton('Немецкий'), KeyboardButton('Русский')]
], resize_keyboard=True)

# inline menu 
inline_keyboard_de = [
    [
        InlineKeyboardButton("Ich möchte Mitglied werden",
                             callback_data="join"),
    ],
    [InlineKeyboardButton(
        "Ich möchte eine Zusammenarbeit vorschlagen", callback_data="cooperate")],
    [InlineKeyboardButton("Ich möchte eine Frage stellen",
                          callback_data="question")],

]

inline_keyboard_ru = [
    [
        InlineKeyboardButton("Хочу стать участниц:ей", callback_data="join"),
    ],
    [InlineKeyboardButton("Хочу предложить сотрудничество",
                          callback_data="cooperate")],
    [InlineKeyboardButton("Хочу задать вопрос", callback_data="question")],
]
#####################################################################

# store user language preference and chosen topic
user_data = {}

#####################################################################

# Language selection handler

async def handle_language(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user_data[user_id] = {'language': update.message.text.lower()}

    if user_data[user_id]['language'] == 'немецкий':
        await update.message.reply_text('Du hast Deutsch gewählt.')
        await update.message.reply_text("Bitte wählen Sie das Thema Ihrer Nachricht :", reply_markup=InlineKeyboardMarkup(inline_keyboard_de))
    elif user_data[user_id]['language'] == 'русский':
        await update.message.reply_text('Вы выбрали русский язык.')
        await update.message.reply_text("Пожалуйста, выберите тему Вашего сообщения:", reply_markup=InlineKeyboardMarkup(inline_keyboard_ru))
    else:
        await update.message.reply_text('Пожалуйста, выберите язык с помощью клавиатуры.')
        return ASKING_LANGUAGE

    return ASKING_MESSAGE

# topic selection handler
async def handle_inline_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    chosen_topic = ""

    if query.data == 'join':
        chosen_topic = "стать участни:цей"
    elif query.data == 'cooperate':
        chosen_topic = "предложить сотрудничество"
    elif query.data == 'question':
        chosen_topic = "задать вопрос"

    if user_lang.get(user_id) == 'немецкий':
        await query.message.reply_text(f"Вы выбрали тему: {chosen_topic}. Ausgezeichnet, danke")
        await query.message.reply_text(text="Schreiben Sie jetzt auf, was Sie uns mitteilen möchten")
    elif user_lang.get(user_id) == 'русский':
        await query.message.reply_text(f"Вы выбрали тему: {chosen_topic}. Отлично, спасибо")
        await query.message.reply_text(text="Теперь напишите, что вы хотите нам сообщить")

# topic button handler

async def handle_inline_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data[user_id]['topic'] = query.data  # Store the chosen topic

    chosen_topic = ""

    if user_data[user_id]['language'] == 'немецкий':
        if query.data == 'join':
            chosen_topic = "Mitglied werden"
        elif query.data == 'cooperate':
            chosen_topic = "eine Zusammenarbeit vorschlagen"
        elif query.data == 'question':
            chosen_topic = "eine Frage stellen"
        await query.message.reply_text(f"Sie haben das Thema gewählt: {chosen_topic}. Ausgezeichnet, danke")
        await query.message.reply_text(text="Schreiben Sie jetzt auf, was Sie uns mitteilen möchten")
    elif user_data[user_id]['language'] == 'русский':
        if query.data == 'join':
            chosen_topic = "стать участни:цей"
        elif query.data == 'cooperate':
            chosen_topic = "предложить сотрудничество"
        elif query.data == 'question':
            chosen_topic = "задать вопрос"
        await query.message.reply_text(f"Вы выбрали тему: {chosen_topic}. Отлично, спасибо")
        await query.message.reply_text(text="Теперь напишите, что вы хотите нам сообщить")

# Cancel command handler
#TODO

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Действие отменено.')
    if update.message.from_user.id in user_data:
        # Clear user data if canceling
        del user_data[update.message.from_user.id]
    return ConversationHandler.END

# define commands
#####################################################################

#start command handler
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Выберите язык:', reply_markup=language_keyboard)
    return ASKING_LANGUAGE

#help command handler

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Используйте команду /start, чтобы написать сообщение боту. Все полезные ссылки и наши соцсети также можно найти здесь linktr.ee/far_hamburg')

# About command handler

async def about(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    # Default to 'немецкий' if language not set
    language = user_data.get(user_id, {}).get('language', 'немецкий')
    if language == 'немецкий':
        await update.message.reply_text(
            'Wir sind das Team  Feminist Anti-War Resistance(FAR) in Hamburg. Unser Hauptziel ist die Solidarität mit der Ukraine sowie die Unterstützung politischer Gefangener, der Frauenrechte und der LGBTQI+-Gemeinschaft. Wir organisieren Veranstaltungen und Sammlungen, bei denen Sie Spenden für unterstützende Organisationen leisten können. Schließen Sie sich uns an – gemeinsam können wir mehr bewirken! Folgen Sie uns in den sozialen Medien, um nichts zu verpassen.\n'
            'Alle nützlichen Links und unsere sozialen Netzwerke finden Sie auch unter linktr.ee/far_hamburg'
        )
    elif language == 'русский':
        await update.message.reply_text(
            'Привет! Мы – команда ФАС в Гамбурге. Наша главная цель – проявление солидарности с Украиной, а также поддержка политических заключённых, защита прав женщин и квир-сообщества. Мы организуем мероприятия и сборы средств, на которых вы можете сделать пожертвование в пользу нуждающихся организаций. Присоединяйтесь к нам – вместе мы сделаем больше! Подписывайтесь на нас в социальных сетях, чтобы ничего не пропустить.\n'
            'Все полезные ссылки и наши соцсети также можно найти здесь linktr.ee/far_hamburg'
        )
    else:
        await update.message.reply_text(
            'Hello! We are the team of FAS in Hamburg. Our main goal is to show solidarity with Ukraine and support political prisoners, women''s'' rights, and the LGBTQI+ community. We organize events and fundraisers where you can make donations to supporting organizations. Join us – together we can make a difference! Follow us on social media to stay updated.\n'
            'You can find all useful links and our social networks here linktr.ee/far_hamburg'
        )

#####################################################################
app = ApplicationBuilder().token(TOKEN).build()
#####################################################################

app.add_handler(MessageHandler(filters.Regex(
    r'^Немецкий$|^Русский$'), handle_language))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Действие отменено.')
    return ConversationHandler.END

# forward message to an admin

#message handler

async def handle_message(update: Update, context: CallbackContext) -> int:
    user_message = update.message.text
    user_id = update.message.from_user.id

    language = user_data[user_id]['language']
    chosen_topic = user_data[user_id]['topic']

    # build message

    message_to_admin = (
        f"Сообщение от пользователь:ницы\n"
        f"Имя: {update.effective_user.first_name}\n"
        f"Ник: @{update.effective_user.username}\n"
        f"Тема: #{chosen_topic}\n"
        f"Сообщение: {user_message}"
    )

    #await context.bot.send_message(chat_id=ADMIN_ID, text=message_to_admin)
    await context.bot.send_message(chat_id=GROUP_ID, text=message_to_admin)

    if language == 'немецкий':
        await update.message.reply_text('Ihre Nachricht wurde de:r Administrator:in gesendet.')
    elif language == 'русский':
        await update.message.reply_text('Сообщение переслано администратор:ке!!!')

    del user_data[user_id]  # Clear user data after processing

    return ConversationHandler.END

# Define ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASKING_LANGUAGE: [MessageHandler(filters.Regex(r'^Немецкий$|^Русский$'), handle_language)],
        ASKING_MESSAGE: [CallbackQueryHandler(handle_inline_button), MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
#####################################################################
# add commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("about", about))
app.add_handler(CallbackQueryHandler(handle_inline_button))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(conv_handler)

#####################################################################
# run
app.run_polling()