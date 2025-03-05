from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# کلید گوگل
GOOGLE_API_KEY = "AIzaSyBqwu5Fg4gBZwdCMt2wyvpZ1OJdmRIoBio"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# توکن تلگرام
TELEGRAM_TOKEN = "8150256753:AAEakQU7RH6yOIK365rHvhFspY7TXrWckDs"

# این برای جواب متنی
def get_gemini_response(text):
    response = model.generate_content(text)
    return response.text

# این برای ساخت عکس (فرضی)
def generate_image(prompt):
    # فرض می‌کنیم Gemini یه تابع داره که عکس می‌سازه
    response = model.generate_image(prompt)  # تابع فرضی
    if response:
        with open("generated_image.png", "wb") as f:
            f.write(response.content)  # فرض می‌کنیم محتوا برمی‌گردونه
        return "generated_image.png"
    return None

# پیام خوش‌آمدگویی
async def start(update: Update, context):
    await update.message.reply_text("سلام! من ربات Gemini هستم. بگو 'متن' برای چت یا 'عکس' و یه توضیح برای تصویر!")

# جواب به پیام‌ها
async def handle_message(update: Update, context):
    user_message = update.message.text
    if user_message.startswith("عکس "):
        prompt = user_message[4:]  # برداشتن "عکس " از اول
        image_path = generate_image(prompt)
        if image_path:
            with open(image_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
            await update.message.reply_text("عکست آماده شد!")
        else:
            await update.message.reply_text("مشکلی پیش اومد، دوباره امتحان کن!")
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