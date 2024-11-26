import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config  # Mengimpor konfigurasi dari config.py

# Membaca konfigurasi dari file config.py
api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN
database_file = config.DATABASE_FILE  # Lokasi file data absen

# Fungsi untuk menyimpan data absen ke file teks
def save_absen(user_id, username, absen_time):
    with open(database_file, 'a') as f:  # Gunakan 'a' untuk append data baru
        f.write(f"{user_id}|{username}|{absen_time}\n")

# Fungsi untuk memeriksa apakah user sudah absen
def is_user_absent(user_id):
    if not os.path.exists(database_file):
        return False
    with open(database_file, 'r') as f:
        for line in f:
            if line.startswith(str(user_id) + "|"):
                return True
    return False

# Membuat aplikasi bot
app = Client("absenbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Fungsi untuk mengirim pesan dengan tombol absen
@app.on_message(filters.command("start"))
async def start(client, message):
    # Membuat tombol centang hijau untuk absen
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✔ Absen Sekarang", callback_data="absen")]
        ]
    )

    # Mengirim pesan dengan tombol absen
    await message.reply(
        "Selamat datang! Tekan tombol di bawah untuk melakukan absen.",
        reply_markup=keyboard
    )

# Fungsi untuk menangani klik tombol
@app.on_callback_query()
async def handle_button_click(client, callback_query):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username or callback_query.from_user.first_name
    absen_time = callback_query.message.date.strftime("%Y-%m-%d %H:%M:%S")

    # Cek apakah user sudah absen
    if is_user_absent(user_id):
        await callback_query.answer(f"{username}, kamu sudah absen sebelumnya.")
    else:
        # Menyimpan data absen user baru
        save_absen(user_id, username, absen_time)
        await callback_query.answer(f"Absen berhasil tercatat untuk {username}!")
    
    # Memberikan pesan tambahan di chat
    await callback_query.message.reply(f"Terima kasih {callback_query.from_user.first_name}, absen kamu telah tercatat!")

# Menjalankan aplikasi bot
if __name__ == "__main__":
    app.run()  # Menggunakan app.run() untuk menjalankan bot