
import asyncio
import signal
from pyrogram import Client, filters
from handler import handle_start, handle_button_click  # Mengimpor handler
import config

# Membuat aplikasi bot
app = Client("absenbot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Mengonfigurasi handler untuk pesan "start"
app.add_handler(filters.command("start"), handle_start)

# Mengonfigurasi handler untuk klik tombol (callback_query)
app.add_handler(filters.CallbackQuery(), handle_button_click)

# Fungsi shutdown handler untuk menangani SIGINT atau SIGTERM
async def shutdown_handler(signal, loop):
    print("Bot is shutting down...")
    await app.stop()  # Memberhentikan bot dengan aman
    loop.stop()  # Memberhentikan event loop

# Menambahkan signal handler untuk shutdown menggunakan signal module
loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, asyncio.create_task, shutdown_handler(signal.SIGINT, loop))
loop.add_signal_handler(signal.SIGTERM, asyncio.create_task, shutdown_handler(signal.SIGTERM, loop))

# Menjalankan aplikasi bot
if __name__ == "__main__":
    app.run()  # Menjalankan bot menggunakan asyncio