import telebot
import yt_dlp
import os

# Sening bot tokening
TOKEN = '8096181370:AAE4pGrErpqT-wmPPv01j_EVOo-zohcrioQ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! YouTube linkini yuboring, yuklab beraman. 🚀")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        sent_msg = bot.reply_to(message, "Tayyorlanyapti... ⏳")
        
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'video.mp4',
            'max_filesize': 48 * 1024 * 1024, 
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            os.remove('video.mp4')
            bot.delete_message(message.chat.id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text("Xato! Video juda katta bo'lishi mumkin.", message.chat.id, sent_msg.message_id)
    else:
        bot.reply_to(message, "Iltimos, faqat YouTube linkini yuboring!")

bot.infinity_polling()
          
