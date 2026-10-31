
import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota", login_view=None):
        self.user_role = user_role.lower()
        self.login_view = login_view

        self.model = BukuModel()

        self.view = BukuView(
            role=self.user_role,
            login_view=self.login_view
        )

        # Menyimpan ID buku yang sedang dipilih
        self.id_buku_dipilih = None

        self.view.title(
            f"Sistem Manajemen Perpustakaan - "
            f"Mode: {self.user_role.upper()}"
        )

        # MENGHUBUNGKAN TOMBOL
        self.view.btn_simpan.configure(
            command=self.simpan_data
        )

        self.view.btn_update.configure(
            command=self.perbarui_data
        )

        self.view.btn_delete.configure(
            command=self.hapus_data
        )

        self.view.btn_logout.configure(
            command=self.logout
        )

        # MENGHUBUNGKAN TABEL DENGAN FUNGSI PEMILIHAN
        self.view.tabel.bind(
            "<<TreeviewSelect>>",
            self.pilih_buku
        )

        # MENGATUR HAK AKSES
        self.atur_hak_akses()

        # MEMUAT DATA BUKU
        self.muat_data_tabel()

        # MENANGANI TOMBOL X
        self.view.protocol(
            "WM_DELETE_WINDOW",
            self.logout
        )

    # MENGATUR HAK AKSES PENGGUNA
    def atur_hak_akses(self):
        if self.user_role != "admin":
            self.view.entry_judul.configure(
                state="disabled"
            )

            self.view.entry_penulis.configure(
                state="disabled"
            )

            self.view.entry_tahun.configure(
                state="disabled"
            )

            self.view.btn_simpan.configure(
                state="disabled"
            )

            self.view.btn_update.configure(
                state="disabled"
            )

            self.view.btn_delete.configure(
                state="disabled"
            )

    # MEMUAT DATA BUKU
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        self.id_buku_dipilih = None

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["penulis"],
                    buku["tahun_terbit"]
                )
            )

    # MEMILIH DATA BUKU
    def pilih_buku(self, event=None):
        selected = self.view.tabel.selection()

        if not selected:
            return

        data = self.view.tabel.item(
            selected[0],
            "values"
        )

        # Mengambil ID buku yang dipilih
        self.id_buku_dipilih = int(data[0])

        # Anggota hanya dapat melihat data
        if self.user_role != "admin":
            return

        # Memasukkan data ke formulir
        self.view.entry_judul.delete(0, "end")
        self.view.entry_judul.insert(0, data[1])

        self.view.entry_penulis.delete(0, "end")
        self.view.entry_penulis.insert(0, data[2])

        self.view.entry_tahun.delete(0, "end")
        self.view.entry_tahun.insert(0, data[3])

    # MENYIMPAN DATA BUKU
    def simpan_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Hanya Admin yang dapat menambahkan buku!"
            )
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        try:
            tahun = int(tahun)

            if tahun <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka positif!"
            )
            return

        berhasil = self.model.create_buku(
            judul,
            penulis,
            tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil disimpan!"
            )

            self.bersihkan_form()
            self.muat_data_tabel()

        else:
            messagebox.showerror(
                "Gagal",
                "Data buku gagal disimpan!"
            )

    # MEMPERBARUI DATA BUKU
    def perbarui_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Hanya Admin yang dapat memperbarui buku!"
            )
            return

        if self.id_buku_dipilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih buku dari tabel terlebih dahulu!"
            )
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        try:
            tahun = int(tahun)

            if tahun <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka positif!"
            )
            return

        berhasil = self.model.update_buku(
            self.id_buku_dipilih,
            judul,
            penulis,
            tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil diperbarui!"
            )

            self.bersihkan_form()
            self.muat_data_tabel()

        else:
            messagebox.showerror(
                "Gagal",
                "Data buku gagal diperbarui!"
            )

    # MENGHAPUS BUKU BESERTA RIWAYAT PEMINJAMAN
    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Hanya Admin yang dapat menghapus buku!"
            )
            return

        if self.id_buku_dipilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin dihapus!"
            )
            return

        # KONFIRMASI PENGHAPUSAN
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Penghapusan",
            "Apakah kamu yakin ingin menghapus buku ini?\n\n"
            "Seluruh riwayat peminjaman buku ini juga "
            "akan dihapus secara permanen."
        )

        if not konfirmasi:
            return

        # MENJALANKAN PROSES DELETE
        berhasil = self.model.delete_buku(
            self.id_buku_dipilih
        )

        if berhasil:
            messagebox.showinfo(
                "Berhasil",
                "Data buku dan seluruh riwayat "
                "peminjamannya berhasil dihapus!"
            )

            self.bersihkan_form()
            self.muat_data_tabel()

        else:
            messagebox.showerror(
                "Gagal",
                "Data buku gagal dihapus. "
                "Periksa pesan kesalahan pada terminal."
            )

    # MEMBERSIHKAN FORM
    def bersihkan_form(self):
        self.id_buku_dipilih = None

        selected = self.view.tabel.selection()

        if selected:
            self.view.tabel.selection_remove(*selected)

        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")

    # LOGOUT
    def logout(self):
        self.view.destroy()

        if self.login_view is not None:
            self.login_view.deiconify()

    # MENJALANKAN APLIKASI
    def run(self):
        self.view.mainloop()
