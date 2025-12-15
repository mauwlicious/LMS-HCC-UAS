# auth.py
import hashlib # untuk hashing password
import os
from data_utils import read_lines, write_lines, append_line # mengimpor fungsi dari data_utils.py
from utils import generate_id # mengimpor fungsi generate_id dari utils.py

ADM_PATH = "data/admins.txt" # path ke file data admin
# kode rahasia untuk registrasi admin baru
REG_SECRET = "HCC2025"  

def _hash_password(username, password): # fungsi untuk meng-hash password dengan salt
    """Simple salted hash: sha256(username + password)""" # komentar penjelas fungsi
    salt = username[::-1]  # gunakan username terbalik sebagai salt
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() # mengembalikan hash heksadesimal

def load_admins(): # fungsi untuk memuat data admin dari file
    lines = read_lines(ADM_PATH) # membaca baris dari file admin
    admins = {} # inisialisasi dictionary untuk menyimpan data admin
    for ln in lines: # iterasi setiap baris
        parts = ln.split("|") # memisahkan baris berdasarkan delimiter "|"
        if len(parts) >= 2: # jika ada setidaknya dua bagian (username dan hash password)
            username = parts[0] # ambil username
            passwd_hash = parts[1] # ambil hash password
            admins[username] = passwd_hash # simpan di dictionary
    return admins # mengembalikan dictionary admin

def register_admin(username, password, secret): # fungsi untuk mendaftarkan admin baru
    if secret != REG_SECRET: # memeriksa kode rahasia
        return False, "Secret code salah. Minta secret ke pengajar." # jika salah, kembalikan pesan error
    admins = load_admins() # memuat data admin yang ada
    if username in admins: # memeriksa apakah username sudah ada
        return False, "Username sudah ada." # jika ada, kembalikan pesan error
    h = _hash_password(username, password) # meng-hash password
    append_line(ADM_PATH, f"{username}|{h}") # menambahkan admin baru ke file
    return True, "Admin terdaftar." # mengembalikan pesan sukses

def verify_admin(username, password): # fungsi untuk memverifikasi kredensial admin
    admins = load_admins() # memuat data admin yang ada
    if username not in admins: # memeriksa apakah username ada
        return False # jika tidak ada, kembalikan False
    return admins[username] == _hash_password(username, password) # memeriksa apakah hash password cocok