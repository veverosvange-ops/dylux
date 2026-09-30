from flask import Flask, request, jsonify
import telebot

app = Flask(__name__)

# Token Bot Telegram kamu yang baru
TELEGRAM_BOT_TOKEN = "8903996033:AAFjq32aNVAnRbPy-51ufNWGwIaxntKTVKo"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)

# Database Sederhana di Server
DATABASE_AKUN = {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "service": "Dylux Telegram Webhook Engine"})

# Endpoint Webhook utama yang lebih aman
@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_data = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

# --- FITUR BOT TELEGRAM ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
        "🤖 *Selamat datang di Dylux Bot!*\n\n"
        "Gunakan perintah berikut untuk mulai:\n"
        "`/inject <email> <jumlah_money>`\n"
        "Contoh: `/inject azizi177@gmail.com 5000000`", 
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['inject'])
def handle_telegram_inject(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ Format salah! Gunakan: `/inject <email> <jumlah>`", parse_mode="Markdown")
            return
            
        email = args[1]
        amount = int(args[2])
        
        if email not in DATABASE_AKUN:
            DATABASE_AKUN[email] = {"money": 10000, "gold": 50}
            
        DATABASE_AKUN[email]["money"] += amount
        
        bot.reply_to(message, 
            f"✅ *INJECT BERHASIL!*\n\n"
            f"📧 Akun: `{email}`\n"
            f"💰 Tambahan: `{amount}`\n"
            f"💵 Total Money Sekarang: `{DATABASE_AKUN[email]['money']}`",
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi kesalahan: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
