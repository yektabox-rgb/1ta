import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = '8591678543:AAEgQCUWxvG83VOSJFq01Xe_BTq6IqxWZJg'

OPENROUTER_API_KEY = 'کلیدت رو اینجا بذار'  # همون که از openrouter.ai گرفتی

OPENROUTER_BASE = 'https://openrouter.ai/api/v1/chat/completions'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('سلام! عکس چارت بیت‌کوین رو بفرست تا با ۳ هوش مصنوعی تحلیل کنم.')

async def analyze_chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.photo:
        await update.message.reply_text('لطفاً عکس چارت بفرست.')
        return
    
    await update.message.reply_text('در حال تحلیل با ۳ هوش مصنوعی... (تکنیکال + سنتیمنت + محاسبات)')
    
    # ۱. تکنیکال با Llama
    prompt_tech = "تحلیل تکنیکال چارت بیت‌کوین: الگوها، سطوح حمایت/مقاومت، RSI، پیش‌بینی روند."
    response_tech = call_openrouter('meta-llama/llama-3.1-70b-instruct:free', prompt_tech)
    
    # ۲. سنتیمنت با Grok
    prompt_sent = "سنتیمنت X و آنچین بیت‌کوین: اخبار اخیر، جریان whale، funding rate."
    response_sent = call_openrouter('xai/grok-3-mini:free', prompt_sent)
    
    # ۳. محاسبات با Qwen
    prompt_calc = "محاسبات معامله: TP/SL/RR بر اساس سطوح ۹۳k حمایت و ۹۶k مقاومت، بک‌تست ساده."
    response_calc = call_openrouter('qwen/qwen-2.5-72b-instruct:free', prompt_calc)
    
    full_analysis = f"**تکنیکال (Llama):** {response_tech}\n\n**سنتیمنت (Grok):** {response_sent}\n\n**محاسبات (Qwen):** {response_calc}"
    
    await update.message.reply_text(full_analysis)

def call_openrouter(model, prompt):
    headers = {'Authorization': f'Bearer {OPENROUTER_API_KEY}', 'Content-Type': 'application/json'}
    data = {'model': model, 'messages': [{'role': 'user', 'content': prompt}]}
    try:
        response = requests.post(OPENROUTER_BASE, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return 'خطا در مدل. بعداً امتحان کن.'
    except:
        return 'مشکل اتصال.'

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, analyze_chart))
    application.run_polling()

if __name__ == '__main__':
    main()
