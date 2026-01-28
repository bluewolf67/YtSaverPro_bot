import telebot
import yt_dlp
import os
from threading import Thread
from flask import Flask

# Bot tokeningiz
TOKEN = '8096181370:AAE4pGrErpqT-wmPPv01j_EVOo-zohcrioQ'
bot = telebot.TeleBot(TOKEN)
user_links = {}

# Render uchun web server (bot o'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home(): return "Bot ishlayapti!"
def run(): app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Salom! YouTube linkini yuboring. 🎬")

@bot.message_handler(func=lambda m: "youtu" in m.text)
def get_link(m):
    user_links[m.chat.id] = m.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("480p", callback_data="480"),
               telebot.types.InlineKeyboardButton("720p", callback_data="720"))
    bot.reply_to(m, "Sifatni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def download(call):
    url = user_links.get(call.message.chat.id)
    if not url: return
    quality = call.data
    bot.edit_message_text(f"⏳ {quality}p yuklanyapti... Kuting.", call.message.chat.id, call.message.message_id)
    
    fn = f'v_{call.message.chat.id}.mp4'
    opts = {
        'format': f'best[height<={quality}][ext=mp4]/best',
        'outtmpl': fn,
        'max_filesize': 80 * 1024 * 1024, # 80MB gacha ruxsat
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        with open(fn, 'rb') as f:
            bot.send_video(call.message.chat.id, f)
        os.remove(fn)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        bot.send_message(call.message.chat.id, "❌ Xato: Video juda katta yoki link noto'g'ri.")
        if os.path.exists(fn): os.remove(fn)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
        opts = {
        'format': f'best[height<={quality}][ext=mp4]/best',
        'outtmpl': fn,
        'max_filesize': 80 * 1024 * 1024,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
}

    
