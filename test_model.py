from models.buku_model import BukuModel

model = BukuModel()

# 1. Menambahkan buku baru
print("=== Menambahkan Buku ===")
model.create_buku("Pemrograman Python MVC", "Guido van Rossum", 2023)
print("Data berhasil disimpan!")

# 2. Menampilkan semua buku
print("\n=== Daftar Buku ===")
daftar_buku = model.get_all_buku()

for i, buku in enumerate(daftar_buku, start=1):
    print(f"[{i}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")

# Mengambil ID buku terakhir yang baru ditambahkan
id_terakhir = daftar_buku[-1]['id_buku']

# 3. Menguji UPDATE
print("\n=== Update Buku ===")
if model.update_buku(id_terakhir, "Belajar Python", "Guido van Rossum", 2024):
    print("Data berhasil diupdate!")
else:
    print("Data gagal diupdate!")

# Menampilkan data setelah update
print("\n=== Data Setelah Update ===")
daftar_buku = model.get_all_buku()

for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")

# 4. Menguji DELETE
print("\n=== Delete Buku ===")
if model.delete_buku(id_terakhir):
    print("Data berhasil dihapus!")
else:
    print("Data gagal dihapus!")

# Menampilkan data setelah delete
print("\n=== Data Setelah Delete ===")
daftar_buku = model.get_all_buku()

for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")