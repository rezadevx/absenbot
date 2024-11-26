import asyncio
from pyrogram import Client, filters

api_id = "API_ID"
api_hash = "API_HASH"
bot_token = "YOUR_BOT_TOKEN"

# Membuat aplikasi bot
app = Client("absenbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Menambahkan handler untuk perintah /start
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Bot ini sedang berjalan!")

# Fungsi utama untuk menjalankan bot
async def main():
    # Menjalankan bot
    await app.start()
    print("Bot is running")
    await app.idle()  # Menunggu bot berhenti

# Menjalankan bot menggunakan asyncio
if __name__ == "__main__":
    app.run()  # Ganti dengan app.run() untuk menjalankan bot