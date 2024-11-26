import asyncio
import aiosignal
from pyrogram import Client, filters
import signal
from handler import handle_start, handle_button_click
import config

# Membuat aplikasi bot
app = Client("absenbot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Mengonfigurasi handler untuk pesan "start"
app.add_handler(filters.command("start"), handle_start)

# Mengonfigurasi handler untuk klik tombol (callback_query)
app.add_handler(filters.callback_query(), handle_button_click)  # Perbaiki di sini

# Signal handler untuk shutdown
async def shutdown_handler():
    print("Bot is shutting down...")
    await app.stop()  # Memberhentikan bot dengan aman

# Menambahkan signal handler untuk shutdown menggunakan aiosignal
aiosignal.signal(signal.SIGINT, shutdown_handler)
aiosignal.signal(signal.SIGTERM, shutdown_handler)

# Menjalankan aplikasi bot
if __name__ == "__main__":
    app.run()  # Menjalankan bot menggunakan asyncio