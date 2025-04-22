from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Final
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup
import os


# constants


TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменной окружения
BOT_NAME: Final = '@far_hamburg_bot'
ASKING_MESSAGE, ASKING_LANGUAGE = range(2)
# anastas as an admin
ADMIN_ID: Final = '328310817'
GROUP_ID: Final = '-4757667404'
#####################################################################

# language keyboard

user_lang = {}
language_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton('Deutsch'), KeyboardButton('Русский')]
], resize_keyboard=True)

# inline menu 
inline_keyboard_de = [
    [InlineKeyboardButton("1️⃣Dem FAR-Chat beitreten", callback_data="join_chat")],
    [InlineKeyboardButton("2️⃣Mitglied der Zelle werden", callback_data="join")],
    [InlineKeyboardButton("3️⃣Zusammenarbeit vorschlagen", callback_data="cooperate")],
    [InlineKeyboardButton("4️⃣Eine Frage stellen", callback_data="question")],
    [InlineKeyboardButton("5️⃣Mehr über FAR Hamburg", callback_data="about")],
]

inline_keyboard_ru = [
    [InlineKeyboardButton("1️⃣Вступить в чат сторонни:ц", callback_data="join_chat")],
    [InlineKeyboardButton("2️⃣Стать участни:цей ячейки", callback_data="join")],
    [InlineKeyboardButton("3️⃣Предложить сотрудничество", callback_data="cooperate")],
    [InlineKeyboardButton("4️⃣Задать вопрос", callback_data="question")],
    [InlineKeyboardButton("5️⃣Узнать о ФАС Гамбург", callback_data="about")],
]
#####################################################################

# store user language preference and chosen topic
user_data = {}

#####################################################################

# Language selection handler

async def handle_language(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user_data[user_id] = {'language': update.message.text.lower()}

    if user_data[user_id]['language'] == 'deutsch':
        await update.message.reply_text("Du hast Deutsch gewählt. Was möchtest du wissen?", reply_markup=InlineKeyboardMarkup(inline_keyboard_de))
    elif user_data[user_id]['language'] == 'русский':
        await update.message.reply_text("Ты выбрал:и русский язык. Что бы ты хотел:и узнать?", reply_markup=InlineKeyboardMarkup(inline_keyboard_ru))
    else:
        await update.message.reply_text('Пожалуйста, выбери язык с помощью клавиатуры. // Bitte wähle eine Sprache mit der Tastatur.')
        return ASKING_LANGUAGE

    return ASKING_MESSAGE

# topic selection handler
async def handle_inline_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_lang = user_data.get(user_id, {}).get('language', 'deutsch')
    user_data[user_id]['topic'] = query.data  # Сохраняем выбранную тему

    chosen_topic = ""

    if user_lang == 'deutsch':
        if query.data == 'join':
            chosen_topic = "Mitglied werden"
            await query.message.reply_text(text="Du willst aktiv werden und Teil unserer Zelle werden? Großartig!🌱\nErzähl uns kurz etwas über dich – unsere Koordinator:in wird sich bei dir melden, um alles Weitere zu besprechen.\n‼️Bitte schreibe alles in einer Nachricht – wir bekommen nur die erste angezeigt!"),
            parse_mode='Markdown'
        elif query.data == 'join_chat':
            await query.message.reply_text(
            "Im Unterstützer*innen-Chat von FAR Hamburg pflegen wir eine freundliche und solidarische Atmosphäre💬✨.\n"
            'Alle, die mitmachen, stimmen auch den Werten in unserem <a href="https://femagainstwar.notion.site/DER-FEMINISTISCHE-WIDERSTAND-GEGEN-DEN-KRIEG-MANIFEST-9897451ac0d746899bbcbdf92b9e9dc5">Manifest</a> zu.\n'
            "Wenn du dich mit dem Manifest und der Atmosphäre wohlfühlst – schreib einfach \"Chat beitreten\"🧡",
            parse_mode='HTML'
            )
        elif query.data == 'cooperate':
            chosen_topic = "eine Zusammenarbeit vorschlagen"
            await query.message.reply_text(text="Du hast eine Idee für eine Zusammenarbeit? Super!✊\nErkläre kurz, worum es geht – unsere Koordinato:rin wird sich bei dir melden.\n‼️Bitte schreibe alles in einer Nachricht – wir bekommen nur die erste angezeigt!")
        elif query.data == 'question':
            chosen_topic = "eine Frage stellen"
            await query.message.reply_text(text="Du hast eine Frage? Stell sie uns einfach🧐\nUnsere Koordinator:in wird sich bald bei dir melden.\n‼️Bitte schreibe alles in einer Nachricht – wir bekommen nur die erste angezeigt!")
        elif query.data == 'about':
            chosen_topic = "über FAR Hamburg"
            await query.message.reply_text(text="Hallo! Wir sind das Kollektiv FAR Hamburg🖤\n" 
            "Unsere Werte sind: Solidarität mit der Ukraine, Unterstützung politischer Gefangener, Einsatz für Frauenrechte und den Schutz der queeren Community."
            "\nWir organisieren Veranstaltungen und Spendenaktionen für unterstützende Organisationen."
            "\nMach mit – gemeinsam können wir mehr bewegen!"
            "\nAlle Links und unsere Social Media findest du hier\n👉 linktr.ee/far_hamburg"
                
            )
    elif user_lang == 'русский':
        if query.data == 'join':
            chosen_topic = "стать участни:цей"
            await query.message.reply_text(text="Если ты хочешь стать активной участницей или участником ячейки — расскажи немного о себе🌱\n"
            "Наша координатор:ка свяжется с тобой, чтобы обсудить детали.\n‼️Пожалуйста, напиши всё в одном сообщении — мы получим только первое!")
        elif query.data == 'join_chat':
            await query.message.reply_text(
            'В чате сторонни:ц ФАС Гамбург мы создаём дружелюбную и поддерживающую атмосферу💬✨.\n'
            'Также, все участни:цы соглашаются с ценностями, прописанными в нашем <a href="https://femagainstwar.notion.site/manifest">манифесте</a>.\n'
            'Если тебе подходит манифест и ты за дружественную обстановку — напиши \"Вступить в чат\" 🧡',
            parse_mode='HTML'
            )
        elif query.data == 'cooperate':
            chosen_topic = "предложить сотрудничество"
            await query.message.reply_text(text="У тебя есть идея для сотрудничества? Отлично!✊\nОпиши свою идею — координатор:ка свяжется с тобой.\n"
            "‼️Пожалуйста, напиши всё в одном сообщении — мы получим только первое!")
        elif query.data == 'question':
            chosen_topic = "задать вопрос"
            await query.message.reply_text(text="Хочешь задать вопрос? Просто напиши, что тебя интересует🧐\nКоординатор:ка скоро ответит."
            "\n‼️Пожалуйста, напиши всё в одном сообщении — мы получим только первое!")
        elif query.data == 'about':
            chosen_topic = "о ФАС Гамбург"
            await query.message.reply_text(text="Привет! Мы – коллектив ФАС Гамбург🖤\n"
            "Наши ценности – солидарность с Украиной, поддержка политзаключённых, защита прав женщин и квир-сообщества.\n"
            "Мы организуем мероприятия и сборы в поддержку помогающих организаций.\n"
            "Присоединяйся к нам — вместе мы сделаем больше!\n"
            "Все полезные ссылки и наши соцсети ты найдёшь здесь\n👉 linktr.ee/far_hamburg"
            )
# topic button handler



# define commands
#####################################################################

#start command handler
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('🥰Привет! Это чат-бот ФАС Гамбург.// 🥰Hallo! Ich bin der Chat-Bot von FAR Hamburg.\n\nВыбери язык:⤵️ // Wähle bitte eine Sprache⤵️', reply_markup=language_keyboard)
    return ASKING_LANGUAGE



#####################################################################
app = ApplicationBuilder().token(TOKEN).build()
#####################################################################

app.add_handler(MessageHandler(filters.Regex(
    r'^Deutsch$|^Русский$'), handle_language))



# forward message to an admin

#message handler

async def handle_message(update: Update, context: CallbackContext) -> int:
    user_message = update.message.text
    user_id = update.message.from_user.id

    if user_id not in user_data:
        await update.message.reply_text("Пожалуйста, начните сначала с /start.")
        return ConversationHandler.END

    language = user_data[user_id]['language']
    chosen_topic = user_data[user_id]['topic']

    # 🔹 Обработка специального случая — вступление в чат
    if chosen_topic == 'join_chat' and user_message.strip().lower() in [
        "хочу вступить в чат", "ich möchte dem chat beitreten"
    ]:
        message_to_admin = (
            f"Запрос на вступление в чат\n"
            f"Имя: {update.effective_user.first_name}\n"
            f"Ник: @{update.effective_user.username}"
        )
        await context.bot.send_message(chat_id=GROUP_ID, text=message_to_admin)

        if language == 'deutsch':
            await update.message.reply_text("Ihre Anfrage wurde gesendet. Eine:r Koordinator:in wird Ihnen bald den Link zum Chat schicken.")
        elif language == 'русский':
            await update.message.reply_text("Ваш запрос отправлен. Координатор:ка отправит вам ссылку на чат в ближайшее время.")

        del user_data[user_id]
        return ConversationHandler.END

    # 🔹 Обычное сообщение по выбранной теме
    message_to_admin = (
        f"Сообщение от пользователь:ницы\n"
        f"Имя: {update.effective_user.first_name}\n"
        f"Ник: @{update.effective_user.username}\n"
        f"Тема: #{chosen_topic}\n"
        f"Сообщение: {user_message}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=message_to_admin)

    if language == 'deutsch':
        await update.message.reply_text('Ihre Nachricht wurde gesendet. Eine:r unserer Koordinator:innen wird sich in Kürze bei Ihnen melden.')
    elif language == 'русский':
        await update.message.reply_text('Сообщение переслано. С вами свяжется одна из наших координатор:ок в ближайшее время.')

    del user_data[user_id]
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Действие отменено. Вы можете начать сначала с /start.")
    if update.message.from_user.id in user_data:
        del user_data[update.message.from_user.id]
    return ConversationHandler.END

# Define ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASKING_LANGUAGE: [MessageHandler(filters.Regex(r'^Deutsch$|^Русский$'), handle_language)],
        ASKING_MESSAGE: [CallbackQueryHandler(handle_inline_button), MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
#####################################################################
# add commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_inline_button))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(conv_handler)

#####################################################################
# run
app.run_polling()
