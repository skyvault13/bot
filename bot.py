import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8237153560:AAGiqIBs6xhDQ0c8p6xbYlob-fd9X2VZQxw')

# Текст инструкции
INSTRUCTION_TEXT = """
📖 **ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ**

Добро пожаловать в наш бот! Вот основные функции:

1. **Получение инструкции** - нажмите кнопку "📄 Получить брошюру"
2. **Контакты** - нажмите кнопку "📞 Контакты" для связи с нами
3. **Помощь** - всегда доступна через команду /help

Для начала работы просто используйте кнопки меню ниже!
"""

# Текст контактов
CONTACTS_TEXT = """
📞 **НАШИ КОНТАКТЫ**

Аккаунты в Telegram:
@oolleesshh Олешко Виктория
@im\_emii Караева Эмилия 
@a\_rinaa Борзина Арина 
@stlunth Стрюкова Елизаветa 
@rakitinass Ракитина Анастасия
@sokolovaapsy Соколова Анастасия

Мы всегда рады помочь вам!
"""

async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start - показывает главное меню"""
    keyboard = [
        [KeyboardButton("📄 Получить брошюру")],
        [KeyboardButton("📞 Контакты")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    welcome_text = "👋 Добро пожаловать! Выберите нужную опцию:"
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_instruction_button(update: Update, context: CallbackContext) -> None:
    """Обработчик нажатия на кнопку получения инструкции"""
    try:
        await update.message.reply_text(INSTRUCTION_TEXT, parse_mode='Markdown')
        with open("брошюра_буллинг2.pdf", "rb") as file:
            await update.message.reply_document(
                document=file,
                filename="Брошюра_буллинг.pdf",
                caption="📎 Вот ваша брошюра в виде файла"
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке инструкции: {e}")
        await update.message.reply_text("❌ Произошла ошибка при отправке файла. Попробуйте позже.")

async def handle_contacts_button(update: Update, context: CallbackContext) -> None:
    """Обработчик нажатия на кнопку контактов"""
    await update.message.reply_text(CONTACTS_TEXT, parse_mode='Markdown')

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений"""
    text = update.message.text
    if text == "📄 Получить брошюру":
        await handle_instruction_button(update, context)
    elif text == "📞 Контакты":
        await handle_contacts_button(update, context)
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки меню 👇")

async def help_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /help"""
    help_text = """
🤖 **Доступные команды:**

/start - Запустить бота и показать меню
/help - Показать эту справку

Или просто используйте кнопки меню!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Основная функция запуска бота"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не установлен!")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Бот запущен...")
    print("🤖 Бот запущен и готов к работе!")
    application.run_polling()

if __name__ == '__main__':
    main()