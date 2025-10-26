from flask import Flask
import subprocess
import threading
import os
import time

app = Flask(__name__)

# Флаг для отслеживания состояния бота
bot_process = None

def start_bot():
    """Запускает бота в отдельном процессе"""
    global bot_process
    try:
        print("🚀 Запускаем Telegram бота...")
        bot_process = subprocess.Popen(['python', 'bot.py'])
        print("✅ Бот запущен в отдельном процессе")
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

@app.route('/')
def home():
    return """
    <html>
        <body>
            <h1>🤖 Telegram Bot is Running!</h1>
            <p>Use <strong>/start</strong> in Telegram to interact with the bot.</p>
            <p>Bot status: <span style="color: green;">🟢 Active</span></p>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK"

@app.route('/status')
def status():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return "🟢 Bot is running"
    else:
        return "🔴 Bot is not running"

if __name__ == '__main__':
    # Запускаем бота при старте
    start_bot()
    
    # Запускаем Flask сервер
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Web server starting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)