
# Sistem Manajemen Perpustakaan

## 1. Deskripsi Aplikasi

Sistem Manajemen Perpustakaan merupakan aplikasi desktop berbasis Python yang dikembangkan untuk membantu pengelolaan data koleksi buku perpustakaan.

Aplikasi ini menggunakan konsep Model-View-Controller (MVC), CustomTkinter sebagai antarmuka pengguna, dan MySQL sebagai database untuk menyimpan data.

Aplikasi menyediakan fitur autentikasi pengguna dengan dua jenis hak akses, yaitu:

- **Admin:** Memiliki hak akses penuh untuk menambahkan, memperbarui, dan menghapus data buku.
- **Anggota/Mahasiswa:** Memiliki hak akses untuk melihat daftar koleksi buku, tetapi tidak dapat menambahkan, memperbarui, atau menghapus data buku.

Fitur utama aplikasi:

- Login dan autentikasi pengguna.
- Pengelolaan data buku (Create, Read, Update, Delete).
- Pembatasan hak akses berdasarkan role pengguna.
- Logout dan kembali ke halaman login.
- Penyimpanan data menggunakan database MySQL.

## 2. Struktur Direktori MVC

Proyek ini menggunakan pola arsitektur Model-View-Controller (MVC) untuk memisahkan pengelolaan data, tampilan antarmuka, dan logika aplikasi.

Struktur direktori proyek:

```text
Modul_3RPL/
|
|-- .github/
|   |-- workflows/
|       |-- ci_pipeline.yml
|
|-- config/
|   |-- database.py
|
|-- controllers/
|   |-- auth_controller.py
|   |-- buku_controller.py
|
|-- models/
|   |-- user_model.py
|   |-- buku_model.py
|
|-- views/
|   |-- login_view.py
|   |-- buku_view.py
|
|-- tests/
|   |-- test_auth.py
|   |-- test_buku.py
|
|-- dist/
|   |-- AplikasiPerpustakaan.exe
|
|-- AplikasiPerpustakaan.spec
|-- demo_crud_buku.py
|-- main.py
|-- requirements.txt
|-- README.md
|-- .gitignore
```

### A. Models

Folder `models` berisi kode yang mengelola data dan berinteraksi dengan database MySQL.

- `user_model.py`: Mengelola autentikasi pengguna dan pemeriksaan password.
- `buku_model.py`: Mengelola data buku, termasuk menambahkan, menampilkan, memperbarui, dan menghapus data.

### B. Views

Folder `views` berisi tampilan antarmuka aplikasi yang digunakan oleh pengguna.

- `login_view.py`: Menampilkan halaman login.
- `buku_view.py`: Menampilkan formulir, tabel koleksi buku, serta tombol pengelolaan data.

### C. Controllers

Folder `controllers` berisi logika yang menghubungkan Model dan View.

- `auth_controller.py`: Mengatur proses login dan autentikasi pengguna.
- `buku_controller.py`: Mengatur proses CRUD buku serta pembatasan hak akses berdasarkan role pengguna.

### D. Config

Folder `config` berisi konfigurasi koneksi database MySQL melalui file `database.py`.

### E. Tests

Folder `tests` berisi file pengujian otomatis untuk memeriksa fitur autentikasi dan pengelolaan buku.

### F. Main.py

File `main.py` merupakan titik awal untuk menjalankan aplikasi perpustakaan.

## 3. Instalasi dan Konfigurasi Database MySQL

### A. Persiapan

Sebelum menjalankan aplikasi, pastikan perangkat telah memiliki:

- Python.
- Visual Studio Code.
- Laragon.
- MySQL.
- Git.

### B. Mengunduh Proyek

Clone repository GitHub menggunakan perintah berikut:

```bash
git clone https://github.com/nur-anisaa/Modul_3RPL.git
```

Masuk ke direktori proyek:

```bash
cd Modul_3RPL
```

### C. Membuat Virtual Environment

Buat lingkungan virtual Python dengan perintah:

```bash
python -m venv .venv
```

Aktifkan virtual environment pada Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### D. Menginstal Dependensi

Pastikan virtual environment sudah aktif. Kemudian jalankan perintah berikut untuk menginstal seluruh library yang dibutuhkan:

```bash
python -m pip install -r requirements.txt
```

Beberapa library yang digunakan dalam aplikasi antara lain:

- `customtkinter`
- `mysql-connector-python`
- `pytest`
- `flake8`

### E. Konfigurasi Database MySQL

Ikuti langkah berikut:

1. Buka aplikasi Laragon.
2. Jalankan layanan MySQL.
3. Buka HeidiSQL atau MySQL Terminal.
4. Buat database dengan nama `perpustakaan`.

Jalankan perintah SQL berikut:

```sql
CREATE DATABASE IF NOT EXISTS perpustakaan;
```

Pastikan tabel `users` dan `buku` sudah tersedia sesuai kebutuhan program pada masing-masing Model.

Tabel `buku` menggunakan kolom:

- `id_buku`
- `judul`
- `penulis`
- `tahun_terbit`

Tabel `users` menggunakan kolom:

- `username`
- `password`
- `role`

Password pengguna disimpan dalam bentuk hash sesuai metode hashing yang diterapkan pada `user_model.py`.

### F. Konfigurasi Koneksi Database

Pengaturan koneksi database berada pada file:

`config/database.py`

Konfigurasi yang digunakan dalam proyek ini adalah:

```python
self.host = "localhost"
self.db_name = "perpustakaan"
self.username = "root"
self.password = ""
```

Konfigurasi tersebut dapat disesuaikan apabila pengaturan MySQL pada komputer berbeda.

## 4. Cara Menjalankan Aplikasi

### A. Menjalankan Aplikasi melalui Python

Untuk menjalankan aplikasi melalui Visual Studio Code, lakukan langkah berikut:

1. Pastikan Laragon dan layanan MySQL sudah berjalan.
2. Buka terminal pada folder utama proyek.
3. Aktifkan virtual environment.
4. Jalankan perintah berikut:

```bash
python main.py
```

Aplikasi akan menampilkan halaman login.

Masukkan username dan password pengguna yang sudah terdaftar pada database.

### B. Menjalankan Pengujian Otomatis

Untuk menjalankan pengujian aplikasi menggunakan Pytest, gunakan perintah:

```bash
python -m pytest -v
```

Untuk memeriksa kualitas kode menggunakan Flake8, jalankan:

```bash
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

### C. Menjalankan Aplikasi dalam Bentuk EXE

Aplikasi juga dapat dijalankan melalui file eksekusi Windows yang dihasilkan menggunakan PyInstaller.

Lokasi file aplikasi:

```text
dist/AplikasiPerpustakaan.exe
```

Untuk menjalankannya:

1. Pastikan layanan MySQL pada Laragon sudah menyala.
2. Buka folder `dist` melalui Windows File Explorer.
3. Klik dua kali file `AplikasiPerpustakaan.exe`.
4. Aplikasi akan terbuka dan menampilkan halaman login.

Pengguna dapat menggunakan aplikasi tanpa harus menjalankan perintah Python melalui terminal, selama database dan layanan MySQL sudah dikonfigurasi dengan benar.
