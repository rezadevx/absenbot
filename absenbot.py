import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config  # Mengimpor konfigurasi dari config.py

# Membaca konfigurasi dari file config.py
api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN
database_file = config.DATABASE_FILE

# Membaca data absen dari file JSON (jika ada)
def load_absen_data():
    try:
        with open(database_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Menyimpan data absen ke file JSON
def save_absen_data(absen_data):
    with open(database_file, 'w') as f:
        json.dump(absen_data, f, indent=4)

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
    if callback_query.data == "absen":
        # Memuat data absen yang sudah ada
        absen_data = load_absen_data()

        # Mencatat absen untuk user yang klik tombol
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username or callback_query.from_user.first_name

        # Pastikan user belum absen
        if user_id not in absen_data:
            absen_data[user_id] = {
                "username": username,
                "absen_time": callback_query.message.date.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Menyimpan data absen ke file
            save_absen_data(absen_data)

            # Menanggapi klik tombol dan mencatat bahwa pengguna sudah absen
            await callback_query.answer(f"Absen berhasil tercatat untuk {username}!")
        else:
            await callback_query.answer(f"{username}, kamu sudah absen sebelumnya.")

        # Memberikan pesan tambahan di chat
        await callback_query.message.reply(f"Terima kasih {callback_query.from_user.first_name}, absen kamu telah tercatat!")

# Menjalankan bot menggunakan app.run()
if __name__ == "__main__":
    app.run()  # app.run() sudah menangani event loop