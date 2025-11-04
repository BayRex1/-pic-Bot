import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
BOT_TOKEN = "8253801561:AAFL2nrKZ1QghtucHr7hMstT_P9Ilbxj2ig"
# ID администратора
ADMIN_ID = 8221276881

# URL для загрузки APK из твоего GitHub репозитория
GITHUB_RAW_URL = "https://raw.githubusercontent.com/BayRex1/-pic-Bot/4554d4ffa15f8e2c27558495f95c7c3a88a1f33d/public/files/base%20(2).apk"

# Альтернативный URL (используем direct ссылку)
GITHUB_DIRECT_URL = "https://github.com/BayRex1/-pic-Bot/raw/4554d4ffa15f8e2c27558495f95c7c3a88a1f33d/public/files/base%20(2).apk"

# URL для загрузки WebApp
WEBAPP_RAW_URL = "https://raw.githubusercontent.com/BayRex1/-pic-Bot/e58a520263f577421ba1025a321c1708cdcc11b5/public/files/WebApp.apk"
WEBAPP_DIRECT_URL = "https://github.com/BayRex1/-pic-Bot/raw/e58a520263f577421ba1025a321c1708cdcc11b5/public/files/WebApp.apk"

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
/webapp - скачать WebApp версию
/payment - помочь в развитии Epic Messenger
/help - связаться с поддержкой

Бот готов к работе! 🚀
    """
    await update.message.reply_text(welcome_text)

# Функция для команды /download
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Показываем пользователю, что файл загружается
        loading_msg = await update.message.reply_text("📥 Загружаем файл из GitHub...")
        
        # Пробуем первый URL
        response = requests.get(GITHUB_RAW_URL, stream=True, timeout=30)
        
        # Если первый URL не работает, пробуем альтернативный
        if response.status_code != 200:
            response = requests.get(GITHUB_DIRECT_URL, stream=True, timeout=30)
        
        if response.status_code != 200:
            await loading_msg.delete()
            await update.message.reply_text("❌ Файл не найден в репозитории. Проверьте ссылку.")
            return
            
        response.raise_for_status()  # Проверяем статус ответа
        
        # Создаем временный файл
        temp_file = "temp_epic_messenger.apk"
        file_size = 0
        
        # Скачиваем файл
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    file_size += len(chunk)
        
        # Удаляем сообщение о загрузке
        await loading_msg.delete()
        
        # Проверяем размер файла (должен быть больше 0)
        if file_size == 0:
            raise Exception("Файл пустой или не был загружен")
        
        # Отправляем файл пользователю
        with open(temp_file, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename='Epic-Messenger.apk',
                caption="📲 Epic Messenger APK\n\nУстановите приложение и наслаждайтесь общением!"
            )
        
        # Удаляем временный файл
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        logging.info(f"Файл успешно загружен из GitHub ({file_size} байт) и отправлен пользователю")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при загрузке файла из GitHub: {e}")
        await update.message.reply_text("❌ Ошибка при загрузке файла из репозитория. Попробуйте позже.")
    except Exception as e:
        logging.error(f"Ошибка при отправке файла: {e}")
        await update.message.reply_text("❌ Произошла ошибка при загрузке файла")

# Функция для команды /webapp
async def webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Показываем пользователю, что файл загружается
        loading_msg = await update.message.reply_text("📥 Загружаем WebApp из GitHub...")
        
        # Пробуем первый URL
        response = requests.get(WEBAPP_RAW_URL, stream=True, timeout=30)
        
        # Если первый URL не работает, пробуем альтернативный
        if response.status_code != 200:
            response = requests.get(WEBAPP_DIRECT_URL, stream=True, timeout=30)
        
        if response.status_code != 200:
            await loading_msg.delete()
            await update.message.reply_text("❌ WebApp файл не найден в репозитории. Проверьте ссылку.")
            return
            
        response.raise_for_status()  # Проверяем статус ответа
        
        # Создаем временный файл
        temp_file = "temp_webapp.apk"
        file_size = 0
        
        # Скачиваем файл
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    file_size += len(chunk)
        
        # Удаляем сообщение о загрузке
        await loading_msg.delete()
        
        # Проверяем размер файла (должен быть больше 0)
        if file_size == 0:
            raise Exception("Файл пустой или не был загружен")
        
        # Отправляем файл пользователю
        with open(temp_file, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename='Epic-Messenger-WebApp.apk',
                caption="🌐 Epic Messenger WebApp\n\nВеб-версия приложения для удобного использования!"
            )
        
        # Удаляем временный файл
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        logging.info(f"WebApp успешно загружен из GitHub ({file_size} байт) и отправлен пользователю")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при загрузке WebApp из GitHub: {e}")
        await update.message.reply_text("❌ Ошибка при загрузке WebApp из репозитория. Попробуйте позже.")
    except Exception as e:
        logging.error(f"Ошибка при отправке WebApp: {e}")
        await update.message.reply_text("❌ Произошла ошибка при загрузке WebApp")

# Функция для команды /ecoin
async def ecoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ecoin_text = """
💰 **Покупка Ε-COIN**
в разработке

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
• Скачать WebApp через команду /webapp
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
    application.add_handler(CommandHandler("webapp", webapp))
    application.add_handler(CommandHandler("ecoin", ecoin))
    application.add_handler(CommandHandler("payment", payment))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reply", reply_command))
    
    # Обработчик текстовых сообщений от пользователей
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    
    # Обработчик callback кнопок
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Обработчик ответов администратора (реплаев)
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_admin_reply))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
