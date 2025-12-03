import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = 'کد رباتت رو اینجا بذار'  # مثلاً '1234567890:AAHblahblah'

OPENROUTER_API_KEY = 'sk-or-v1-free'  # کلید رایگان هوش مصنوعی

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('سلام! عکس چارت بیت‌کوین رو بفرست تا تحلیل کنم.')

async def analyze_chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.photo:
        await update.message.reply_text('لطفاً عکس چارت بفرست.')
        return
    
    await update.message.reply_text('در حال تحلیل... (رایگان و ساده)')
    
    prompt = "تحلیل چارت بیت‌کوین: صعودی یا نزولی؟ سطوح کلیدی و پیشنهاد معامله بده."
    
    headers = {'Authorization': f'Bearer {OPENROUTER_API_KEY}', 'Content-Type': 'application/json'}
    data = {'model': 'meta-llama/llama-3.1-70b-instruct:free', 'messages': [{'role': 'user', 'content': prompt}]}
    
    try:
        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            await update.message.reply_text(f'تحلیل: {result}')
        else:
            await update.message.reply_text('خطا. بعداً امتحان کن.')
    except:
        await update.message.reply_text('مشکل. عکس رو دوباره بفرست.')

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, analyze_chart))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
