
import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota", login_view=None):
        self.user_role = user_role.lower()
        self.login_view = login_view

        self.model = BukuModel()

        # Mengirim role ke halaman buku
        self.view = BukuView(
            role=self.user_role,
            login_view=self.login_view
        )

        self.id_buku_dipilih = None

        # Menghubungkan tombol
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

        # Menghubungkan tabel
        self.view.tabel.bind(
            "<<TreeviewSelect>>",
            self.pilih_buku
        )

        self.muat_data_tabel()

        self.view.protocol(
            "WM_DELETE_WINDOW",
            self.logout
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

    # MEMILIH BUKU
    def pilih_buku(self, event=None):
        selected = self.view.tabel.selection()

        if not selected:
            return

        data = self.view.tabel.item(
            selected[0], "values"
        )

        self.id_buku_dipilih = int(data[0])

        # Anggota hanya melihat tabel,
        # tidak mengisi formulir.
        if self.user_role == "anggota":
            return

        self.view.entry_judul.delete(0, "end")
        self.view.entry_judul.insert(0, data[1])

        self.view.entry_penulis.delete(0, "end")
        self.view.entry_penulis.insert(0, data[2])

        self.view.entry_tahun.delete(0, "end")
        self.view.entry_tahun.insert(0, data[3])

    # MENYIMPAN BUKU
    def simpan_data(self):
        if self.user_role != "admin":
            messagebox.showwarning(
                "Akses Ditolak",
                "Fitur ini hanya untuk Admin!"
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
                "Tahun harus berupa angka positif!"
            )
            return

        berhasil = self.model.create_buku(
            judul, penulis, tahun
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

    # UPDATE BUKU
    def perbarui_data(self):
        if self.user_role != "admin":
            messagebox.showwarning(
                "Akses Ditolak",
                "Fitur ini hanya untuk Admin!"
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
                "Tahun harus berupa angka positif!"
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

    # DELETE BUKU
    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showwarning(
                "Akses Ditolak",
                "Fitur ini hanya untuk Admin!"
            )
            return

        if self.id_buku_dipilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin dihapus!"
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah kamu yakin ingin menghapus buku ini?"
        )

        if not konfirmasi:
            return

        berhasil = self.model.delete_buku(
            self.id_buku_dipilih
        )

        if berhasil:
            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil dihapus!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Gagal",
                "Data buku gagal dihapus!"
            )

    # MEMBERSIHKAN FORM
    def bersihkan_form(self):
        self.id_buku_dipilih = None

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
