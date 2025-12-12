# data_utils.py
import os # untuk operasi file
from utils import atomic_write # mengimpor fungsi atomic_write dari utils.py

def read_lines(path): # fungsi untuk membaca baris dari file
    if not os.path.exists(path): # jika file tidak ada, kembalikan list kosong
        return [] # file tidak ada
    with open(path, "r", encoding="utf-8") as f: # membuka file untuk membaca
        lines = [ln.strip() for ln in f if ln.strip()] # membaca dan membersihkan baris
    return lines # mengembalikan daftar baris

def write_lines(path, lines): # fungsi untuk menulis baris ke file
    text = "\n".join(lines) + ("\n" if lines else "") # menggabungkan baris menjadi satu string
    atomic_write(path, text) # menulis string ke file secara atomik

def append_line(path, line): # fungsi untuk menambahkan satu baris ke file
    lines = read_lines(path) # membaca baris yang ada
    lines.append(line) # menambahkan baris baru
    write_lines(path, lines) # menulis kembali semua baris ke file

def find_lines_with_prefix(path, key_index, key_value): # fungsi untuk menemukan baris dengan prefix tertentu
    """Return (idx, parts, raw) for lines matching key at index when split by |""" # komentar penjelas fungsi
    results = [] # inisialisasi daftar hasil
    lines = read_lines(path) # membaca baris dari file
    for i, raw in enumerate(lines): # iterasi setiap baris dengan indeks
        parts = raw.split("|") # memisahkan baris berdasarkan delimiter "|"
        if len(parts) > key_index and parts[key_index] == key_value: # memeriksa apakah bagian pada indeks tertentu cocok dengan nilai kunci
            results.append((i, parts, raw))     # menambahkan hasil ke daftar
    return results # mengembalikan daftar hasil
