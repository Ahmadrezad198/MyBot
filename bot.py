from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import google.generativeai as genai
import requests

# کلید گوگل برای متن
GOOGLE_API_KEY = "AIzaSyBqwu5Fg4gBZwdCMt2wyvpZ1OJdmRIoBio"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# کلید SerpAPI برای جست‌وجوی وب
SERPAPI_API_KEY = "9f7fcd0781c8b82ffba81234502fb02bba79221a9cb6d3e7ba8a448f122fb244"

# توکن تلگرام
TELEGRAM_TOKEN = "8150256753:AAEakQU7RH6yOIK365rHvhFspY7TXrWckDs"

# جواب متنی از Gemini
def get_gemini_response(text):
    response = model.generate_content(text)
    return response.text

# جست‌وجوی وب با SerpAPI
def search_web(query):
    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERPAPI_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        return results.get("organic_results", [{}])[0].get("snippet", "چیزی پیدا نشد")
    return "مشکلی پیش اومد"

# پیام خوش‌آمدگویی
async def start(update: Update, context):
    await update.message.reply_text("سلام! بگو 'جست‌وجو' و یه چیز برای وب، یا هر چی برای چت!")

# جواب به پیام‌ها
async def handle_message(update: Update, context):
    user_message = update.message.text
    if user_message.startswith("جست‌وجو "):
        query = user_message[7:]
        result = search_web(query)
        await update.message.reply_text(result)
    else:
        gemini_reply = get_gemini_response(user_message)
        await update.message.reply_text(gemini_reply)

# راه‌اندازی ربات
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()