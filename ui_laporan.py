# ui_laporan.py
import streamlit as st # mengimpor Streamlit untuk antarmuka web
from data_utils import read_lines, append_line, write_lines # mengimpor fungsi dari data_utils.py
from utils import generate_id, now_iso # mengimpor fungsi dari utils.py

LAP_PATH = "data/laporan.txt" # path ke file data laporan
MEM_PATH = "data/members.txt" # path ke file data anggota

def _read_members(): # fungsi untuk membaca data anggota
    return [ln.split("|") for ln in read_lines(MEM_PATH) if ln] # mengembalikan daftar anggota yang dipisahkan oleh "|"

def laporan_page(username): # halaman laporan
    st.header("Laporan Proses Pembelajaran (oleh Pengurus)") # judul halaman laporan

    members = _read_members() # membaca data anggota
    mem_map = {r[0]: r[1] for r in members} # membuat peta anggota dengan ID sebagai kunci dan nama sebagai nilai

    st.subheader("Tambah Laporan") # subjudul untuk menambah laporan
    with st.form("form_lap"): # membuat form laporan
        target = st.selectbox("Untuk Anggota (opsional)", ["-"] + list(mem_map.keys()), format_func=lambda x: ("Semua" if x=="-" else f"{mem_map[x]} ({x})")) # dropdown untuk memilih target anggota
        title = st.text_input("Judul Laporan") # input judul laporan
        content = st.text_area("Isi Laporan") # area teks untuk isi laporan
        btn = st.form_submit_button("Tambahkan Laporan") # tombol submit untuk menambahkan laporan
    if btn: # jika tombol submit ditekan
        if not title or not content: # memeriksa apakah judul dan isi diisi
            st.error("Judul dan isi wajib.") # menampilkan pesan error
        else: # jika valid
            lid = generate_id("R") # menghasilkan ID laporan baru
            date = now_iso() # mendapatkan tanggal dan waktu saat ini dalam format ISO
            target_id = "" if target == "-" else target # menentukan ID target
            append_line(LAP_PATH, f"{lid}|{target_id}|{title}|{content}|{username}|{date}") # menambahkan baris laporan ke file
            st.success("Laporan ditambahkan.") # menampilkan pesan sukses

    st.markdown("---") # garis pemisah
    st.subheader("Daftar Laporan") # subjudul untuk daftar laporan
    logs = read_lines(LAP_PATH) # membaca baris dari file laporan
    if not logs: # jika tidak ada laporan
        st.info("Belum ada laporan.") # menampilkan informasi bahwa belum ada laporan
    else: # jika ada laporan
        for ln in reversed(logs[-50:]): # menampilkan 50 laporan terakhir
            parts = ln.split("|") # memisahkan baris berdasarkan delimiter "|"
            lid, target_id, title, content, created_by, date = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5] # mengambil bagian-bagian dari baris
            target_name = mem_map.get(target_id, "Semua") if target_id else "Semua" # mendapatkan nama target berdasarkan ID
            st.write(f"**{title}** — untuk: *{target_name}* — oleh `{created_by}` pada {date}") # menampilkan judul laporan dengan informasi tambahan
            st.write(content) # menampilkan isi laporan
            st.write("---") # garis pemisah antar laporan
