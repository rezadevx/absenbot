import logging
import uvloop  # Import uvloop
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import config
import asyncio  # Import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO)

# Inisialisasi bot
app = Client("absenbot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Tempat menyimpan data absensi (untuk contoh, menggunakan dictionary)
absen_data = {}

# Fungsi untuk mencatat absen
def catat_absen(user_id, user_name):
    waktu_absen = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    absen_data[user_id] = {"name": user_name, "waktu": waktu_absen}
    return waktu_absen

# Command start untuk menyambut pengguna
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Absen", callback_data="absen")]
    ])
    await message.reply("Selamat datang! Tekan tombol di bawah untuk absen hari ini.", reply_markup=keyboard)

# Fungsi untuk menangani tombol absen
@app.on_callback_query(filters.regex("absen"))
async def absen_button(client, callback_query):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name
    
    # Cek apakah pengguna sudah absen hari ini
    if user_id in absen_data:
        # Jika sudah absen, beri pesan bahwa absen sudah dilakukan
        await callback_query.answer("Anda sudah absen hari ini. Silakan absen lagi besok.", show_alert=True)
    else:
        # Mencatat waktu absen
        waktu_absen = catat_absen(user_id, user_name)
        await callback_query.answer(f"Terima kasih {user_name}, Anda telah absen pada {waktu_absen}.", show_alert=True)
        
        # Kirim pesan konfirmasi dan pin pesan
        reply_msg = await callback_query.message.reply(f"Terima kasih {user_name}, Anda telah absen pada {waktu_absen}.")
        try:
            await callback_query.message.chat.pin_message(reply_msg.message_id)  # Pin pesan balasan
        except Exception as e:
            logging.error(f"Error saat mem-pin pesan: {e}")

# Fungsi untuk menangani daftar absen
@app.on_message(filters.command("daftarabsen"))
async def daftar_absen(client, message: Message):
    if not absen_data:
        await message.reply("Belum ada yang absen.")
        return
    
    daftar = "\n".join([f"{data['name']} - {data['waktu']}" for data in absen_data.values()])
    await message.reply(f"Daftar absen:\n{daftar}")

# Fungsi utama untuk menjalankan bot
def main():
    # Menggunakan uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # Set event loop ke uvloop
    app.run(timeout=60)  # Menambahkan timeout lebih lama

if __name__ == "__main__":
    main()