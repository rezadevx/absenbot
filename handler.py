
# handler.py
from pyrogram import Client, filters

async def handle_start(client, message):
    """Fungsi untuk menangani perintah /start"""
    await message.reply("Halo! Bot ini siap digunakan.")

async def handle_button_click(client, callback_query):
    """Fungsi untuk menangani callback query dari tombol"""
    await callback_query.answer("Tombol ditekan!")