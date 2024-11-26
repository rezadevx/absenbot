# handler.py

import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import save_absen, is_user_absent
from datetime import datetime

async def handle_start(client, message):
    """Fungsi untuk mengirim pesan dengan tombol absen"""
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✔ Absen Sekarang", callback_data="absen")]
        ]
    )

    await message.reply(
        "Selamat datang! Tekan tombol di bawah untuk melakukan absen.",
        reply_markup=keyboard
    )

async def handle_button_click(client, callback_query):
    """Fungsi untuk menangani klik tombol"""
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username or callback_query.from_user.first_name
    absen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Cek apakah user sudah absen
    if is_user_absent(user_id):
        await callback_query.answer(f"{username}, kamu sudah absen sebelumnya.")
    else:
        # Menyimpan data absen user baru
        save_absen(user_id, username, absen_time)
        await callback_query.answer(f"Absen berhasil tercatat untuk {username}!")
    
    # Memberikan pesan tambahan di chat
    await callback_query.message.reply(f"Terima kasih {callback_query.from_user.first_name}, absen kamu telah tercatat!")