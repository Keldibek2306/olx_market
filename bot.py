from decouple import config
import requests

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

BACKEND_URL = "http://127.0.0.1:8000/api/v1/auth/telegram-login/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    data = {
        "telegram_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    response = requests.post(BACKEND_URL, json=data)

    result = response.json()

    access = result["access"]

    await update.message.reply_text(
        f"Login successful!\n\nYour token:\n{access}"
    )


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()