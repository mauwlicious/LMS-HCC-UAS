# ui_materi.py
import streamlit as st # mengimpor Streamlit untuk antarmuka web
from data_utils import read_lines, write_lines, append_line, search_rows # mengimpor fungsi dari data_utils.py
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
    safe_rows = [] # inisialisasi daftar baris yang aman
    for r in rows: # iterasi setiap baris
        r_copy = r.copy() # membuat salinan baris
        r_copy[2] = r_copy[2].replace("\n", "\\n")  # encode sebelum simpan
        safe_rows.append("|".join(r_copy)) # menggabungkan bagian menjadi baris

    write_lines(MATERI_PATH, safe_rows) # menulis baris ke file materi


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
    
    st.subheader("Daftar Materi") # subjudul untuk daftar materi
    if rows: # jika ada materi
        search = st.text_input(" Cari judul / isi / pembuat") #search bar materi

        show_rows = search_rows(rows, search, [1, 2, 3]) # mencari materi berdasarkan input pencarian
        if search: # jika ada input pencarian
            st.write(f"Menampilkan {len(show_rows)} dari {len(rows)} materi yang cocok dengan '{search}':") # menampilkan jumlah materi yang ditemukan
            if not show_rows and search != "": # jika pencarian tidak ditemukan
                st.info("Pencarian tidak ditemukan.") # menampilkan informasi bahwa pencarian tidak ditemukan
                
        for r in reversed(show_rows): # iterasi setiap materi yang akan ditampilkan
            st.write(f"**{r[1]}** — oleh `{r[3]}` pada {r[4]}") # menampilkan judul materi dengan informasi tambahan
            if r[2]: # jika ada deskripsi
                st.write(r[2]) # menampilkan deskripsi materi
            st.write("---") # garis pemisah antar materi
            
    if not rows: # jika tidak ada materi
        st.info("Belum ada materi.") # menampilkan informasi bahwa belum ada materi
        return # keluar dari fungsi

    st.subheader("Ubah / Hapus Materi") # subjudul untuk ubah/hapus materi

    # MEMBUAT OPSI DROPDOWN MATERI

    options = { # inisialisasi opsi dropdown
        f"{r[0]} — {r[1]}": r # menambahkan opsi dropdown dengan ID dan judul materi sebagai label
        for r in rows # iterasi setiap baris materi
    }
    # key   : "ID — Judul Materi"
    # value : data materi lengkap

    # CEK DATA KOSONG

    if not options: # jika tidak ada opsi
        st.info("Tidak ada materi untuk diubah atau dihapus.") # menampilkan informasi bahwa tidak ada materi untuk diubah/hapus
        return # keluar dari fungsi

    # PLACEHOLDER DROPDOWN

    placeholder = "---- PILIH MATERI UNTUK UBAH / HAPUS ----" # inisialisasi placeholder dropdown

    dropdown_options = [placeholder] + list(options.keys()) # menambahkan placeholder ke opsi dropdown

    # DROPDOWN PILIH MATERI

    sel_label = st.selectbox( # menampilkan dropdown
        "Pilih Materi", # label dropdown
        dropdown_options, # opsi dropdown
        index=0 # default ke placeholder
    )

    # JIKA BELUM PILIH MATERI

    if sel_label == placeholder: # jika placeholder dipilih
        st.info("Silakan pilih materi terlebih dahulu.") # menampilkan informasi untuk memilih materi
        return # keluar dari fungsi

    # AMBIL DATA MATERI TERPILIH 

    r = options[sel_label] # mendapatkan data materi berdasarkan pilihan
    
    # FORM EDIT / HAPUS MATERI

    with st.form("edit_m"): # membuat form edit/hapus materi
        t2 = st.text_input("Judul", r[1]) # input judul materi
        d2 = st.text_area("Deskripsi", r[2]) # area teks untuk deskripsi materi

        btn_up = st.form_submit_button("Simpan Perubahan") # tombol submit untuk menyimpan perubahan
        btn_del = st.form_submit_button("Hapus Materi") # tombol submit untuk menghapus materi


    # UPDATE MATERI

    if btn_up: # jika tombol simpan perubahan ditekan
        if not t2.strip(): # memeriksa apakah judul diisi
            st.error("❌ Judul materi tidak boleh kosong.") # menampilkan pesan error
            st.stop() # menghentikan eksekusi lebih lanjut

        for i, rr in enumerate(rows): # iterasi setiap baris materi
            if rr[0] == r[0]: # jika ID materi cocok
                rows[i] = [ 
                    r[0],      # ID tetap
                    t2.strip(),# judul baru
                    d2, # deskripsi baru
                    rr[3],     # pembuat tetap
                    rr[4]      # tanggal tetap
                ]
                _save_materi(rows) # menyimpan data materi
                st.success("Materi diperbarui.") # menampilkan pesan sukses
                st.rerun() # memuat ulang halaman

    # DELETE MATERI
    
    if btn_del: # jika tombol hapus materi ditekan
        rows = [rr for rr in rows if rr[0] != r[0]] # menghapus materi dari daftar
        _save_materi(rows) # menyimpan data materi
        st.success("Materi dihapus.") # menampilkan pesan sukses
        st.rerun()  # memuat ulang halaman