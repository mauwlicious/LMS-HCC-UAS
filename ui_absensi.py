# ui_absensi.py
import streamlit as st # mengimpor Streamlit untuk antarmuka web
from data_utils import read_lines, append_line # mengimpor fungsi dari data_utils.py
from utils import generate_id, now_iso # mengimpor fungsi dari utils.py

ABS_PATH = "data/absensi.txt" # path ke file data absensi
MEM_PATH = "data/members.txt" # path ke file data anggota

def _read_members(): # fungsi untuk membaca data anggota
    lines = read_lines(MEM_PATH) # membaca baris dari file anggota
    return [ln.split("|") for ln in lines if ln] # mengembalikan daftar anggota yang dipisahkan oleh "|"

def absensi_page(username): # halaman absensi
    st.header("Absensi Pengurus / Member") # judul halaman absensi
    members = _read_members() # membaca data anggota
    member_map = {r[0]: r[1] for r in members} # membuat peta anggota dengan ID sebagai kunci dan nama sebagai nilai

    st.subheader("Tambah Absensi") # subjudul untuk menambah absensi
    with st.form("form_absen"): # membuat form absensi
        sel_id = st.selectbox("Pilih anggota", list(member_map.keys()), format_func=lambda x: f"{member_map[x]} ({x})") # dropdown untuk memilih anggota
        status = st.selectbox("Status", ["Hadir", "Izin", "Alpha"]) # dropdown untuk memilih status absensi
        note = st.text_area("Catatan (opsional)") # area teks untuk catatan opsional
        btn = st.form_submit_button("Simpan Absensi") # tombol submit untuk menyimpan absensi
    if btn: # jika tombol submit ditekan
        aid = generate_id("A") # menghasilkan ID absensi baru
        date = now_iso() # mendapatkan tanggal dan waktu saat ini dalam format ISO
        append_line(ABS_PATH, f"{aid}|{sel_id}|{date}|{status}|{note}") # menambahkan baris absensi ke file
        st.success("Absensi dicatat.") # menampilkan pesan sukses

    st.markdown("---") # garis pemisah
    st.subheader("Log Absensi Terakhir") # subjudul untuk log absensi terakhir
    logs = read_lines(ABS_PATH) # membaca baris dari file absensi
    if not logs: # jika tidak ada log absensi
        st.info("Belum ada absensi.") # menampilkan informasi bahwa belum ada absensi
    else: # jika ada log absensi
        # tampilkan paling baru dulu 
        for ln in reversed(logs[-30:]): # menampilkan 30 log absensi terakhir
            parts = ln.split("|") # memisahkan baris berdasarkan delimiter "|"
            pid, mid, date, status, note = parts[0], parts[1], parts[2], parts[3], (parts[4] if len(parts)>4 else "") # mengambil bagian-bagian dari baris
            name = member_map.get(mid, "Unknown") # mendapatkan nama anggota berdasarkan ID
            st.write(f"- {date} — **{name}** ({mid}) — {status} {('- ' + note) if note else ''}") # menampilkan log absensi dengan format yang rapi