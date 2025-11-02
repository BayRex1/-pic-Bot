import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота (замени на свой)
BOT_TOKEN = "8253801561:AAFL2nrKZ1QghtucHr7hMstT_P9Ilbxj2ig"
# ID администратора (замени на свой Telegram ID)
ADMIN_ID = 8221276881  # Убрал кавычки для числового ID

# Хранилище для переписки (user_id: message)
user_conversations = {}

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
👋 Привет, {user.first_name}!

Доступные команды:
/start - показать это сообщение
/download - скачать Epic Messenger APK
/ecoin - покупка Ε-COIN
/payment - помочь в развитии Epic Messenger
/help - связаться с поддержкой

Бот готов к работе! 🚀
    """
    await update.message.reply_text(welcome_text)

# Функция для команды /download
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Путь к файлу APK в папке Epic Bot
    apk_path = "/storage/emulated/0/Epic bot/public/files/Epic-Messenger.apk"
    
    try:
        # Проверяем существование файла
        if os.path.exists(apk_path):
            await update.message.reply_document(
                document=open(apk_path, 'rb'),
                filename='Epic-Messenger.apk',
                caption="📲 Epic Messenger APK\n\nУстановите приложение и наслаждайтесь общением!"
            )
            logging.info(f"Файл успешно отправлен: {apk_path}")
        else:
            await update.message.reply_text("❌ Файл временно недоступен. Попробуйте позже.")
            logging.error(f"Файл не найден по пути: {apk_path}")
            
    except Exception as e:
        logging.error(f"Ошибка при отправке файла: {e}")
        await update.message.reply_text("❌ Произошла ошибка при загрузке файла")

# Функция для команды /ecoin
async def ecoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ecoin_text = """
💰 **Покупка Ε-COIN**

Ε-COIN - это внутренняя валюта Epic Messenger, которая позволяет вам:

• Покупать премиум-стикеры
• Отправлять виртуальные подарки
• Получать эксклюзивные функции
• Поддерживать разработчиков

**Доступные пакеты Ε-COIN:**

🟢 100 Ε-COIN - 99 ₽
🟡 500 Ε-COIN - 449 ₽  
🔴 1000 Ε-COIN - 799 ₽
🟣 5000 Ε-COIN - 3499 ₽

Для покупки Ε-COIN свяжитесь с администратором через команду /help
    """
    await update.message.reply_text(ecoin_text)

# Функция для команды /payment
async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    donation_url = "https://donate.stream/donate_69072f4c2450e"
    
    keyboard = [
        [InlineKeyboardButton("💳 Поддержать разработку", url=donation_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    payment_text = """
❤️ **Поддержка Epic Messenger**

Ваша поддержка помогает нам развивать приложение и добавлять новые функции!

Каждое пожертвование идет на:
• Улучшение серверов
• Разработку новых функций
• Исправление ошибок
• Поддержку пользователей

Нажмите на кнопку ниже, чтобы перейти к пожертвованию:
    """
    
    await update.message.reply_text(
        payment_text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# Функция для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 Помощь и поддержка

Напишите ваше сообщение ниже, и оно будет переслано администратору.

Администратор ответит вам в ближайшее время.

*Также вы можете:*
• Купить Ε-COIN через команду /ecoin
• Поддержать проект через команду /payment
• Скачать приложение через команду /download
    """
    await update.message.reply_text(help_text)

# Обработка текстовых сообщений от пользователей (для поддержки)
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_message = update.message.text
    
    # Сохраняем информацию о пользователе для ответа
    user_conversations[user.id] = user
    
    # Пересылаем сообщение администратору с кнопкой ответа
    try:
        keyboard = [
            [InlineKeyboardButton("📨 Ответить", callback_data=f"reply_{user.id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"✉️ Сообщение от пользователя @{user.username or 'NoUsername'} (ID: {user.id}):\n\n{user_message}",
            reply_markup=reply_markup
        )
        await update.message.reply_text("✅ Ваше сообщение отправлено администратору! Ожидайте ответа.")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения администратору: {e}")
        await update.message.reply_text("❌ Ошибка при отправке сообщения администратору")

# Обработка ответов от администратора
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Проверяем, что сообщение от администратора
    if user.id != ADMIN_ID:
        return
    
    # Проверяем, является ли сообщение ответом на другое сообщение
    if update.message.reply_to_message:
        reply_to_message = update.message.reply_to_message.text
        admin_reply = update.message.text
        
        # Ищем ID пользователя в тексте сообщения, на которое отвечаем
        if "ID:" in reply_to_message:
            try:
                # Извлекаем ID пользователя из сообщения
                lines = reply_to_message.split('\n')
                for line in lines:
                    if "ID:" in line:
                        user_id = int(line.split("ID:")[1].split(')')[0].strip())
                        
                        # Отправляем ответ пользователю
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=f"📩 Ответ от администратора:\n\n{admin_reply}"
                        )
                        await update.message.reply_text("✅ Ответ отправлен пользователю!")
                        return
            except Exception as e:
                logging.error(f"Ошибка при обработке ответа администратора: {e}")
                await update.message.reply_text("❌ Ошибка при отправке ответа пользователю")

# Обработка callback кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Обработка кнопки "Ответить"
    if query.data.startswith('reply_'):
        user_id = int(query.data.split('_')[1])
        context.user_data['reply_to'] = user_id
        await query.edit_message_text(
            text=f"💬 Ответ пользователю (ID: {user_id})\n\nОтправьте сообщение для этого пользователя:"
        )

# Команда для администратора для ответа пользователю
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ Эта команда только для администратора")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Использование: /reply <user_id> <сообщение>")
        return
    
    try:
        user_id = int(context.args[0])
        message_text = ' '.join(context.args[1:])
        
        if not message_text:
            await update.message.reply_text("❌ Введите сообщение для отправки")
            return
            
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📩 Ответ от администратора:\n\n{message_text}"
        )
        await update.message.reply_text("✅ Ответ отправлен пользователю!")
        
    except ValueError:
        await update.message.reply_text("❌ Неверный формат user_id")
    except Exception as e:
        logging.error(f"Ошибка при отправке ответа: {e}")
        await update.message.reply_text("❌ Ошибка при отправке ответа пользователю")

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Ошибка: {context.error}")

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("download", download))
    application.add_handler(CommandHandler("ecoin", ecoin))
    application.add_handler(CommandHandler("payment", payment))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reply", reply_command))
    
    # Обработчик текстовых сообщений от пользователей
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    
    # Обработчик callback кнопок
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Обработчик ответов администратора (реплаев) - ИСПРАВЛЕННАЯ СТРОКА
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_admin_reply))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()