# LMS HCC (Simple Local LMS)

Deskripsi singkat
-----------------
LMS HCC adalah aplikasi LMS sederhana berbasis file yang dibuat untuk keperluan pembelajaran dan ujian. Aplikasi ini menyimpan data pengguna, materi, absensi, dan laporan dalam berkas teks di folder `data/` dan menyediakan antarmuka Python sederhana untuk mengelola data tersebut.

Fitur utama
-----------
- Manajemen admin (registrasi dan verifikasi)
- Penyimpanan materi pelajaran di `data/materi.txt`
- Pencatatan absensi di `data/absensi.txt`
- Penyimpanan laporan di `data/laporan.txt`
- Daftar anggota di `data/members.txt`

Struktur proyek
---------------
- `main.py` : Entrypoint aplikasi (jalankan dengan Python).
- `auth.py` : Logika autentikasi admin (hashing, pendaftaran, verifikasi).
- `data_utils.py` : Utilitas pembacaan/penulisan berkas teks.
- `utils.py` : Fungsi utilitas tambahan.
- `ui_*.py` : Modul UI (mis. `ui_absensi.py`, `ui_materi.py`, `ui_members.py`, `ui_laporan.py`).
- `data/` : Folder yang menyimpan berkas data:
  - `admins.txt` — daftar admin (format: `username|password_hash`).
  - `members.txt` — daftar anggota.
  - `materi.txt` — materi pembelajaran.
  - `absensi.txt` — catatan absensi.
  - `laporan.txt` — catatan laporan.

Persyaratan
-----------
- Python 3.10 atau lebih baru direkomendasikan.
- Paket Python yang diperlukan tercantum di `requirements.txt`.

Instalasi
---------
1. Buat virtual environment (opsional tetapi direkomendasikan):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Pasang dependensi:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Menjalankan aplikasi
--------------------
Jalankan aplikasi dengan perintah berikut di PowerShell dari direktori proyek:

```powershell
streamlit run main.py
```

Administrasi (registrasi dan login admin)
----------------------------------------
- Kode rahasia registrasi admin saat ini disimpan langsung di `auth.py` pada variabel `REG_SECRET` (nilai default: `HCC2025`).
- Untuk mendaftarkan admin baru, jalankan alur pendaftaran di UI atau panggil fungsi `register_admin(username, password, secret)` dari `auth.py` dengan `secret` yang benar.
- Setelah terdaftar, kredensial disimpan di `data/admins.txt` dalam format `username|password_hash`.

Deskripsi file data
-------------------
- `data/admins.txt`: setiap baris berisi `username|password_hash`.
- `data/members.txt`: daftar anggota, satu per baris (format tergantung implementasi UI/utility).
- `data/materi.txt`: daftar materi/pelajaran.
- `data/absensi.txt`: catatan absensi.
- `data/laporan.txt`: catatan laporan.

Pengembangan
------------
- Jika Anda ingin menambah fitur baru, contoh langkah:
  1. Tinjau `data_utils.py` untuk fungsi pembacaan/penulisan file.
  2. Tambahkan route/command di `main.py` atau modul UI terkait.
  3. Tambahkan/ubah format berkas di `data/` jika diperlukan (beri migrasi jika data penting).

Tes cepat
---------
- Pastikan Python dan dependensi terpasang, lalu jalankan `main.py`.
- Coba mendaftar admin baru (perhatikan `REG_SECRET`) melalui UI atau panggilan fungsi.

Kontak & Lisensi
----------------
Proyek ini dibuat untuk keperluan pembelajaran. Sesuaikan lisensi sesuai kebutuhan institusi Anda.

Catatan akhir
------------
README ini memberikan panduan dasar untuk memahami, menjalankan, dan mengembangkan aplikasi sederhana ini.
