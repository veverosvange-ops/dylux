from flask import Flask, request, jsonify
import hashlib
import time
import telebot

app = Flask(__name__)

# Konfigurasi Bot Telegram (Ganti dengan Token Bot kamu dari @BotFather)
TELEGRAM_BOT_TOKEN = "8903996033:AAHn0_-0W6jHlcU7IvlCH-YuT3t2FcjujRU"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Database Sederhana di Server
DATABASE_AKUN = {}
VALID_KEYS = {
    "DYLUX-VIP-GROOT": {"tier": "premium"}
}

# --- ENDPOINT API BACKEND ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "service": "Dylux Telegram Backend Engine"})

@app.route('/api/v1/game/inject', methods=['POST'])
def server_side_inject():
    data = request.json or {}
    tool_key = data.get("key", "")
    email = data.get("email", "")
    action_type = data.get("action", "")
    amount = int(data.get("amount", 0))
    
    if tool_key not in VALID_KEYS:
        return jsonify({"ok": False, "msg": "Key tidak valid!"}), 403
        
    if email not in DATABASE_AKUN:
        DATABASE_AKUN[email] = {"money": 10000, "gold": 50}
        
    if action_type == "money":
        DATABASE_AKUN[email]["money"] += amount
    elif action_type == "gold":
        DATABASE_AKUN[email]["gold"] += amount

    return jsonify({
        "ok": True,
        "msg": f"Berhasil inject {action_type} sebanyak {amount}!",
        "updated_profile": DATABASE_AKUN[email]
    })


# --- FITUR BOT TELEGRAM ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
        "🤖 *Selamat datang di Dylux Bot!*\n\n"
        "Gunakan perintah berikut untuk mulai:\n"
        "/inject <email> <jumlah_money> - Untuk inject uang\n"
        "Contoh: `/inject emailku@gmail.com 5000000`", 
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['inject'])
def handle_telegram_inject(message):
    try:
        # Format pesan: /inject email@mail.com 5000000
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ Format salah! Gunakan: `/inject <email> <jumlah>`", parse_mode="Markdown")
            return
            
        email = args[1]
        amount = int(args[2])
        
        # Simulasi eksekusi langsung dari server backend
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
    # Menjalankan Bot Telegram secara background/polling atau jalankan Flask
    # Catatan: Dalam deployment cloud (Railway/Render), biasanya bot dijalankan dengan Webhook.
    print("Dylux Server & Telegram Bot siap dijalankan...")
    app.run(host='0.0.0.0', port=5000, debug=True)
