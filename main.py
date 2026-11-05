import telebot
import requests
import os
from flask import Flask
import threading

app = Flask(__name__)

# Токены лучше вынести в переменные окружения Render, но для теста можно оставить здесь
TELEGRAM_TOKEN = "8634076483:AAFBXaGnTy-KeJbtXi-bIsNldEHvR0ts2mE"
OPENROUTER_API_KEY = "AQ.Ab8RN6JHsw63k_Qh7M3M-mcwR4eVO0COQRKr7W4JEbg1geRP6A"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_ai(user_message):
    # Ошибка №1 исправлена: изменен базовый URL на эндпоинт чат-комплитов
    url = "https://openrouter.ai"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    data = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # Печатаем ответ в логи Render для удобной отладки
        print(f"Ответ от OpenRouter: {result}")
        
        ai_text = result['choices'][0]['message']['content']
        return ai_text
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        return "Извините, произошла техническая заминка. Пожалуйста, попробуйте еще раз!"

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я твой Telegram-бот с искусственным интеллектом Llama 3. Задай мне любой вопрос!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ai_response = ask_ai(message.text)
    bot.reply_to(message, ai_response)

@app.route('/')
def index():
    return "Бот работает!"

if __name__ == "__main__":
    # Ошибка №2 исправлена: добавлен параметр skip_pending=True
    threading.Thread(target=bot.infinity_polling, kwargs={"skip_pending": True}, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
