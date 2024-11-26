# database.py

import os
import config

# Fungsi untuk menyimpan data absen ke file teks
def save_absen(user_id, username, absen_time):
    with open(config.DATABASE_FILE, 'a') as f:  # Gunakan 'a' untuk append data baru
        f.write(f"{user_id}|{username}|{absen_time}\n")

# Fungsi untuk memeriksa apakah user sudah absen
def is_user_absent(user_id):
    if not os.path.exists(config.DATABASE_FILE):
        return False
    with open(config.DATABASE_FILE, 'r') as f:
        for line in f:
            if line.startswith(str(user_id) + "|"):
                return True
    return False