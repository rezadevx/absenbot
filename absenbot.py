from pyrogram import Client, filters
import config  # Mengimpor konfigurasi dari config.py

# Membaca konfigurasi dari file config.py
api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN

# Membuat aplikasi bot
app = Client("absenbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Menambahkan handler untuk perintah /start
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Bot ini sedang berjalan!")

# Menjalankan bot menggunakan app.run()
if __name__ == "__main__":
    app.run()  # app.run() sudah menangani event loop