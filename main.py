# main.py
import streamlit as st # mengimpor Streamlit untuk antarmuka web
from auth import register_admin, verify_admin, load_admins, REG_SECRET # mengimpor fungsi autentikasi
from ui_members import members_page # mengimpor halaman manajemen anggota
from ui_absensi import absensi_page # mengimpor halaman absensi
from ui_materi import materi_page # mengimpor halaman materi
from ui_laporan import laporan_page # mengimpor halaman laporan

st.set_page_config(page_title="HCC LMS", layout="wide") # mengatur konfigurasi halaman Streamlit

def login_page(): # halaman login dan registrasi admin
    st.title("HCC — LMS Study Club (Pengurus)") # judul halaman
    st.write("Silakan login sebagai *pengurus* untuk mengelola sistem.") # deskripsi halaman
    col1, col2 = st.columns(2) # membuat dua kolom untuk login dan registrasi
    with col1: # kolom login
        st.subheader("Login") # subjudul login
        with st.form("login_form", clear_on_submit=False): # membuat form login
            username = st.text_input("Username", key="login_user") # input username
            password = st.text_input("Password", type="password", key="login_pass") # input password
            
            submit_login = st.form_submit_button("Login") # tombol submit login
            
        if submit_login: # jika tombol login ditekan
            ok = verify_admin(username, password) # verifikasi kredensial
            if ok: # jika verifikasi berhasil
                st.session_state['logged_in'] = True # set status login
                st.session_state['username'] = username # simpan username di session state
                st.success("Login berhasil.") # tampilkan pesan sukses
                st.rerun() # muat ulang halaman
            else:
                st.error("Login gagal. Periksa username/password.") # tampilkan pesan error
    with col2: # kolom registrasi
        st.subheader("Daftar Pengurus (Register)") # subjudul registrasi
        st.write("Jika belum ada admin, gunakan register (memerlukan secret code).") # deskripsi registrasi
        new_user = st.text_input("Username (register)", key="reg_user") # input username registrasi
        new_pass = st.text_input("Password (register)", type="password", key="reg_pass") # input password registrasi
        secret = st.text_input("Secret Code", key="reg_secret") # input secret code
        if st.button("Daftar"): # tombol daftar
            ok, msg = register_admin(new_user, new_pass, secret) # proses registrasi
            if ok: # jika registrasi berhasil
                st.success(msg + " Silakan login.") # tampilkan pesan sukses
            else: # jika registrasi gagal
                st.error(msg) # tampilkan pesan error

def logout(): # fungsi logout
    st.session_state.clear() # hapus session state
    st.rerun() # muat ulang halaman

def dashboard(): # halaman dashboard setelah login
    st.sidebar.title("Menu") # judul sidebar
    menu = st.sidebar.selectbox("Pilih fitur", ["Home", "Manajemen Anggota", "Absensi", "Materi", "Laporan", "Logout"]) # menu navigasi sidebar
    username = st.session_state.get("username", "unknown") # ambil username dari session state
    st.header(f"Dashboard — Pengurus: {username}") # header dashboard

    if menu == "Home": # halaman home
        st.write("Selamat datang di sistem LMS Study Club — Habibie Coding Club.") # sambutan
        st.write("- Gunakan menu di samping untuk mengelola data.") # instruksi
    elif menu == "Manajemen Anggota": # halaman manajemen anggota
        members_page() # panggil halaman manajemen anggota
    elif menu == "Absensi": # halaman absensi
        absensi_page(username) # panggil halaman absensi
    elif menu == "Materi": # halaman materi
        materi_page(username) # panggil halaman materi
    elif menu == "Laporan": # halaman laporan
        laporan_page(username) # panggil halaman laporan
    elif menu == "Logout": # opsi logout
        if st.button("Konfirmasi Logout"): # tombol konfirmasi logout
            logout() # panggil fungsi

def main(): # fungsi utama
    if 'logged_in' not in st.session_state or not st.session_state.get('logged_in'): # periksa status login
        login_page() # tampilkan halaman login
    else: # jika sudah login
        dashboard() # tampilkan dashboard

if __name__ == "__main__": # jalankan fungsi utama
    main() # panggil fungsi utama