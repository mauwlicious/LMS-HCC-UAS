# ui_members.py
import streamlit as st # mengimpor Streamlit untuk antarmuka web
from data_utils import member_exists_by_number, read_lines, write_lines, append_line, search_rows # mengimpor fungsi dari data_utils.py
from utils import generate_id, now_iso # mengimpor fungsi dari utils.py

MEM_PATH = "data/members.txt" # path ke file data anggota

def _read_members(): # fungsi untuk membaca data anggota
    lines = read_lines(MEM_PATH) # membaca baris dari file anggota
    rows = [] # inisialisasi daftar baris
    for ln in lines: # iterasi setiap baris
        parts = ln.split("|") # memisahkan baris berdasarkan delimiter "|"
        # member_id|name|member_number|prodiangakatan|role|position
        if len(parts) >= 5: # memeriksa apakah ada setidaknya 5 bagian
            rows.append(parts) # menambahkan bagian ke daftar
    return rows # mengembalikan daftar baris

def _save_members(rows): # fungsi untuk menyimpan data anggota
    lines = ["|".join(r) for r in rows] # menggabungkan bagian-bagian menjadi baris
    write_lines(MEM_PATH, lines) # menulis baris ke file anggota

def members_page(): # halaman anggota
    st.header("Manajemen Pengurus / Member") # judul halaman anggota

    if rows:= _read_members(): # membaca data anggota
        st.subheader("Daftar Anggota") # subjudul untuk daftar anggota
        search = st.text_input("Cari nama / nomor /prodi/ jabatan") #search bar untuk mencari anggota

        show_rows = search_rows(rows, search, [1, 2, 3, 4, 5]) # mencari anggota berdasarkan input pencarian
        
        if search: # jika ada input pencarian
            st.write(f"Menampilkan {len(show_rows)} dari {len(rows)} anggota yang cocok dengan '{search}':") # menampilkan jumlah anggota yang ditemukan
            if not show_rows and search != "": # jika pencarian tidak ditemukan
                st.info("Pencarian tidak ditemukan.") # menampilkan informasi bahwa pencarian tidak ditemukan
            
        for r in show_rows: # menampilkan setiap anggota yang ditemukan
            st.write(f"• {r[1]} | {r[2]} | {r[3]} | {r[5]}")
    else:
        st.info("Belum ada data anggota.") # menampilkan informasi bahwa belum ada data anggota

    st.markdown("---") # garis pemisah
    st.subheader("Tambah Anggota / Pengurus") # subjudul untuk menambah anggota
    with st.form("form_add"): # membuat form tambah anggota
        name = st.text_input("Nama").strip() # input nama anggota
        member_number = st.text_input("Nomor Anggota").strip().upper() # input nomor anggota
        prodiangkatan = st.text_input("Prodi / Angkatan (ex: IK25)").strip().upper() # input prodi/angkatan
        role = st.selectbox("Role", ["member", "pengurus"]) # dropdown untuk memilih role
        position = st.text_input("Jabatan (contoh: Ketua, Sekretaris, Dept X)").strip() # input jabatan
        submitted = st.form_submit_button("Tambah") # tombol submit untuk menambah anggota
    if submitted: # jika tombol submit ditekan
        if not (name and member_number and position): # memeriksa apakah semua field diisi
            st.error("Isi semua field.") # menampilkan pesan error
        elif member_exists_by_number(member_number): # memeriksa apakah nomor anggota sudah ada
            st.error("Nomor anggota sudah ada.") # menampilkan pesan error
        elif not member_number.strip().startswith("HCC"): # memeriksa apakah nomor anggota valid
            st.error("Nomor anggota tidak valid. Harus diawali dengan 'HCC'.") # menampilkan pesan error
        else: # jika valid
            mid = generate_id("M") # menghasilkan ID anggota baru
            append_line(MEM_PATH, f"{mid}|{name}|{member_number}|{prodiangkatan}|{role}|{position}") # menambahkan baris anggota ke file
            st.success(f"Anggota {name} ditambahkan (id {mid}).") # menampilkan pesan sukses
            st.rerun() # muat ulang halaman
    
    st.markdown("---")
    st.subheader("Ubah / Hapus Anggota")

    # Membuat opsi dropdown

    options = { #inisialisasi opsi dropdown
        f"{r[0]} — {r[1]}": r # menambahkan opsi dropdown dengan ID dan nama anggota sebagai label
        for r in rows # iterasi setiap baris anggota
    }

    # jika tidak ada data
    if not options:
        st.info("Tidak ada data untuk diubah/hapus.") # menampilkan informasi bahwa tidak ada data untuk diubah/hapus
        return # keluar dari fungsi
    
    # Tampilkan placeholder di atas dropdown

    placeholder = "---- PILIH MEMBER UNTUK UBAH / HAPUS ----"

    dropdown_options = [placeholder] + list(options.keys()) # menambahkan placeholder ke opsi dropdown 

     # Tampilkan dropdown dengan placeholder sebagai opsi pertama
    
    sel_label = st.selectbox( # menampilkan dropdown
        "Pilih Anggota", # label dropdown
        dropdown_options, # opsi dropdown
        index=0 # default ke placeholder
    )
    
    if sel_label == placeholder: # jika placeholder dipilih
        st.info("Silakan pilih anggota untuk mengubah atau menghapus data.") # menampilkan informasi untuk memilih anggota
        return # keluar dari fungsi
    
    sel_r = options[sel_label]
    # sel_r berisi data anggota terpilih

    with st.form("form_edit"): # membuat form edit anggota
        name2 = st.text_input("Nama", sel_r[1]) # input nama anggota
        member_number2 = st.text_input("Nomor Anggota", sel_r[2]) # input nomor anggota
        prodiangkatan2 = st.text_input("Prodi / Angkatan", sel_r[3]) # input prodi/angkatan anggota
        role2 = st.selectbox( # dropdown untuk memilih peran anggota
            "Role", 
            ["member", "pengurus"],
            index=0 if sel_r[4] == "member" else 1 # menentukan indeks default berdasarkan peran saat ini
        )
        position2 = st.text_input("Jabatan", sel_r[5]) # input jabatan anggota

        btn_update = st.form_submit_button("Simpan Perubahan") # tombol submit untuk menyimpan perubahan
        btn_delete = st.form_submit_button("Hapus Anggota") # tombol submit untuk menghapus anggota
        
    if btn_update: # jika tombol simpan perubahan ditekan
        if not name2.strip():
            st.error("❌ Nama tidak boleh kosong.")
            st.stop()

        if not member_number2.strip():
            st.error("❌ Nomor anggota tidak boleh kosong.")
            st.stop()

        if not member_number2.startswith("HCC"):
            st.error("❌ Nomor anggota harus diawali 'HCC'.")
            st.stop()

        if not prodiangkatan2.strip():
            st.error("❌ Prodi / Angkatan tidak boleh kosong.")
            st.stop()

        if not position2.strip():
            st.error("❌ Jabatan tidak boleh kosong.")
            st.stop()
            
        for i, r in enumerate(rows): # iterasi setiap baris anggota
            if r[0] == sel_r[0]: # jika ID anggota cocok
                rows[i] = [sel_r[0], name2.strip(),member_number2.strip().upper(), prodiangkatan2.strip().upper(), role2, position2.strip()] # memperbarui data anggota
                _save_members(rows) # menyimpan data anggota
                st.success("Data diperbarui.") # menampilkan pesan sukses
                st.rerun() # memuat ulang halaman

    if btn_delete: # jika tombol hapus anggota ditekan
        rows = [r for r in rows if r[0] != sel_r[0]] # menghapus anggota dari daftar
        _save_members(rows) # menyimpan data anggota
        st.success("Data dihapus.") # menampilkan pesan sukses
        st.rerun() # memuat ulang halaman
