# ui_materi.py
import streamlit as st # mengimpor Streamlit untuk antarmuka web
from data_utils import read_lines, write_lines, append_line # mengimpor fungsi dari data_utils.py
from utils import generate_id, now_iso # mengimpor fungsi dari utils.py

MATERI_PATH = "data/materi.txt" # path ke file data materi

def _read_materi(): # fungsi untuk membaca data materi
    rows = [] # inisialisasi daftar baris
    for ln in read_lines(MATERI_PATH): # membaca baris dari file materi
        if not ln.strip():  # lewati baris kosong
            continue # lewati baris kosong
        parts = ln.split("|") # memisahkan baris berdasarkan delimiter "|"
        # pastikan parts minimal 5 elemen
        while len(parts) < 5: # jika kurang dari 5 bagian
            parts.append("")# tambahkan string kosong
        # decode newline
        parts[2] = parts[2].replace("\\n", "\n") # mengganti \n dengan newline sebenarnya
        rows.append(parts) # menambahkan bagian ke daftar baris
    return rows # mengembalikan daftar baris

def _save_materi(rows): # fungsi untuk menyimpan data materi
    write_lines(MATERI_PATH, ["|".join(r) for r in rows]) # menulis baris ke file materi

def materi_page(username): # halaman materi
    st.header("Materi Pembelajaran (untuk semua member)") # judul halaman materi

    st.subheader("Tambah Materi") # subjudul untuk menambah materi
    with st.form("form_m"): # membuat form materi
        title = st.text_input("Judul Materi") # input judul materi
        desc = st.text_area("Deskripsi / link / ringkasan") # area teks untuk deskripsi materi
        btn = st.form_submit_button("Tambah Materi") # tombol submit untuk menambahkan materi
    if btn: # jika tombol submit ditekan
        if not title: # memeriksa apakah judul diisi
            st.error("Judul wajib diisi.") # menampilkan pesan error
        else: # jika valid
            mid = generate_id("T") # menghasilkan ID materi baru
            date = now_iso() # mendapatkan tanggal dan waktu saat ini dalam format ISO
            desc_clean = desc.replace("\n", "\\n")  # baris baru diganti dengan \n
            append_line(MATERI_PATH, f"{mid}|{title}|{desc_clean}|{username}|{date}") # menambahkan baris materi ke file
            st.success("Materi ditambahkan.") # menampilkan pesan sukses

    st.markdown("---") # garis pemisah
    rows = _read_materi() # membaca data materi
    if not rows: # jika tidak ada materi
        st.info("Belum ada materi.") # menampilkan informasi bahwa belum ada materi
        return # keluar dari fungsi
    st.subheader("Daftar Materi") # subjudul untuk daftar materi
    for r in reversed(rows): # menampilkan materi dari yang terbaru
        st.write(f"**{r[1]}** — oleh `{r[3]}` pada {r[4]}") # menampilkan judul materi dengan informasi tambahan
        if r[2]: # jika ada deskripsi
            st.write(r[2]) # menampilkan deskripsi materi
        st.write("---") # garis pemisah antar materi

    st.subheader("Ubah / Hapus Materi") # subjudul untuk mengubah atau menghapus materi
    ids = {r[0]: r for r in rows} # membuat peta materi dengan ID sebagai kunci
    sel = st.selectbox("Pilih Materi", list(ids.keys())) # dropdown untuk memilih materi
    if sel: # jika ada materi yang dipilih
        r = ids[sel] # mendapatkan data materi yang dipilih
        with st.form("edit_m"): # membuat form edit materi
            t2 = st.text_input("Judul", r[1]) # input judul materi
            d2 = st.text_area("Deskripsi", r[2]) # area teks untuk deskripsi materi
            btn_up = st.form_submit_button("Simpan Perubahan") # tombol submit untuk menyimpan perubahan
            btn_del = st.form_submit_button("Hapus Materi") # tombol submit untuk menghapus materi
        if btn_up: # jika tombol simpan perubahan ditekan
            for i, rr in enumerate(rows): # iterasi setiap baris materi
                if rr[0] == sel: # jika ID materi cocok
                    rows[i] = [sel, t2, d2, rr[3], rr[4]] # memperbarui data materi
                    _save_materi(rows) # menyimpan data materi
                    st.success("Materi diperbarui.") # menampilkan pesan sukses
                    st.rerun() # memuat ulang halaman
        if btn_del: # jika tombol hapus materi ditekan
            rows = [rr for rr in rows if rr[0] != sel] # menghapus materi dari daftar
            _save_materi(rows) # menyimpan data materi
            st.success("Materi dihapus.") # menampilkan pesan sukses
            st.rerun() # memuat ulang halaman
