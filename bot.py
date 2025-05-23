import openai
import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = os.environ.get("")
OPENAI_API_KEY = os.environ.get("")

openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    match = re.match(r'(?i)^gpt\s+(.*)', message)
    if not match:
        return

    user_input = match.group(1)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response['choices'][0]['message']['content']
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"خطا در پاسخ: {e}")

if __name__ == 'main':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
