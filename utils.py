# utils.py
import os # untuk operasi file
import uuid # untuk menghasilkan UUID unik
from datetime import datetime # untuk mendapatkan tanggal dan waktu saat ini
import tempfile # untuk operasi file sementara

def generate_id(prefix="X"): # fungsi untuk menghasilkan ID unik dengan prefix tertentu
    """Generate unique id: prefix + 6 char hex""" # komentar penjelas fungsi
    return f"{prefix}{uuid.uuid4().hex[:6].upper()}" # mengembalikan ID unik

def now_iso(): # fungsi untuk mendapatkan tanggal dan waktu saat ini dalam format ISO (YYYY-MM-DD HH:MM:SS)
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") # mengembalikan tanggal dan waktu dalam format ISO

def atomic_write(path, text): # fungsi untuk menulis file secara atomik
    """Write file atomically (write to temp then replace).""" # komentar penjelas fungsi
    d = os.path.dirname(path) or "." # mendapatkan direktori dari path
    fd, tmp = tempfile.mkstemp(dir=d) # membuat file sementara di direktori yang sama
    with os.fdopen(fd, "w", encoding="utf-8") as f: # membuka file sementara untuk menulis
        f.write(text) # menulis teks ke file sementara
    os.replace(tmp, path) # menggantikan file asli dengan file sementara secara atomik
