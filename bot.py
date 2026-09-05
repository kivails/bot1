from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "НОВЫЙ_ТОКЕН_ПОСЛЕ_REVOKE"

# Ссылка на твой сайт
WEBAPP_URL = "https://bot1-export.onrender.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "💰 Открыть PayDays",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в PayDays!\n"
        "Нажми кнопку, чтобы пополнить депозит:",
        reply_markup=reply_markup
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
