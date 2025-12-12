# ui_members.py
import streamlit as st # mengimpor Streamlit untuk antarmuka web
from data_utils import read_lines, write_lines, append_line # mengimpor fungsi dari data_utils.py
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

    rows = _read_members() # membaca data anggota
    st.subheader("Daftar Anggota") # subjudul untuk daftar anggota
    if rows: # jika ada anggota
        for r in rows: # iterasi setiap anggota
            st.write(f"- **{r[1]}** (No: {r[2]}) — {r[3]} - {r[4]} / {r[5]} — id: {r[0]}") # menampilkan informasi anggota
    else: # jika tidak ada anggota
        st.info("Belum ada anggota. Tambahkan anggota baru.") # menampilkan informasi bahwa belum ada anggota

    st.markdown("---") # garis pemisah
    st.subheader("Tambah Anggota / Pengurus") # subjudul untuk menambah anggota
    with st.form("form_add"): # membuat form tambah anggota
        name = st.text_input("Nama") # input nama anggota
        member_number = st.text_input("Nomor Anggota") # input nomor anggota
        prodiangkatan = st.text_input("Prodi / Angkatan (ex: IK25)") # input prodi/angkatan
        role = st.selectbox("Role", ["member", "pengurus"]) # dropdown untuk memilih role
        position = st.text_input("Jabatan (contoh: Ketua, Sekretaris, Dept X)") # input jabatan
        submitted = st.form_submit_button("Tambah") # tombol submit untuk menambah anggota
    if submitted: # jika tombol submit ditekan
        if not (name and member_number and position): # memeriksa apakah semua field diisi
            st.error("Isi semua field.") # menampilkan pesan error
        else: # jika valid
            mid = generate_id("M") # menghasilkan ID anggota baru
            append_line(MEM_PATH, f"{mid}|{name}|{member_number}|{prodiangkatan}|{role}|{position}") # menambahkan baris anggota ke file
            st.success(f"Anggota {name} ditambahkan (id {mid}).") # menampilkan pesan sukses
            st.rerun() # muat ulang halaman

    st.markdown("---") # garis pemisah
    st.subheader("Ubah / Hapus Anggota") # subjudul untuk mengubah atau menghapus anggota
    ids_map = {r[0]: r for r in rows} # membuat peta anggota dengan ID sebagai kunci
    if not ids_map: # jika tidak ada anggota
        st.info("Tidak ada data untuk diubah/hapus.") # menampilkan informasi bahwa tidak ada data
        return # keluar dari fungsi
    sel = st.selectbox("Pilih ID untuk edit/hapus", list(ids_map.keys())) # dropdown untuk memilih ID anggota
    sel_r = ids_map.get(sel) # mendapatkan data anggota yang dipilih
    if sel_r: # jika ada anggota yang dipilih
        with st.form("form_edit"): # membuat form edit anggota
            name2 = st.text_input("Nama", sel_r[1]) # input nama anggota
            member_number2 = st.text_input("Nomor Anggota", sel_r[2]) # input nomor anggota
            prodiangkatan2 = st.text_input("Prodi / Angkatan", sel_r[3]) # input prodi/angkatan
            role2 = st.selectbox("Role", ["member", "pengurus"], index=0 if sel_r[4]=="member" else 1) # dropdown untuk memilih role
            position2 = st.text_input("Jabatan", sel_r[5]) # input jabatan
            btn_update = st.form_submit_button("Simpan Perubahan") # tombol submit untuk menyimpan perubahan
            btn_delete = st.form_submit_button("Hapus Anggota") # tombol submit untuk menghapus anggota
        if btn_update: # jika tombol simpan perubahan ditekan
            # update 
            for i, r in enumerate(rows): # iterasi setiap baris anggota
                if r[0] == sel: # jika ID anggota cocok
                    rows[i] = [sel, name2, member_number2, prodiangkatan2, role2, position2] # memperbarui data anggota
                    _save_members(rows) # menyimpan data anggota
                    st.success("Data diperbarui.") # menampilkan pesan sukses
                    st.rerun() # muat ulang halaman
        if btn_delete: # jika tombol hapus anggota ditekan
            rows = [r for r in rows if r[0] != sel] # menghapus anggota dari daftar
            _save_members(rows) # menyimpan data anggota
            st.success("Data dihapus.") # menampilkan pesan sukses
            st.rerun() # muat ulang halaman
