import telebot
import requests
import os
from flask import Flask
import threading

# Создаем фиктивный веб-сайт для бесплатного тарифа Render
app = Flask(__name__)

TELEGRAM_TOKEN = "9268507501:AAGISYrcBRf4pU0sdWbamcVLHPW_ovKObQ8"
GEMINI_API_KEY = "AQ.Ab8RN6JHsw63k_Qh7M3M-mcwR4eVO0COQRKr7W4JEbg1geRP6A"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_gemini_direct(user_message):
    url = "https://openrouter.ai"
 headers = {
     "Content-Type": "application/json",
     "Authorization": "Bearer AQ.Ab8RN6JHsw63k_Qh7M3M-mcwR4eVO0COQRKr7W4JEbg1geRP6A"
 }
 data = {
     "model": "meta-llama/llama-3-8b-instruct:free",
     "messages": [{"role": "user", "content": user_message}]
 }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        ai_text = result['candidates']['content']['parts']['text']
        return response.json()['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Извините, произошла техническая заминка. Пожалуйста, попробуйте еще раз!"

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я твой бесплатный ИИ-бот. Задай мне любой вопрос!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ai_response = ask_gemini_direct(message.text)
    bot.reply_to(message, ai_response)

@app.route('/')
def index():
    return "Бот работает!"

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке, чтобы он не мешал сайту
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    # Слушаем порт, который требует Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
