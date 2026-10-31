
import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTk):
    def __init__(self, role="admin", login_view=None):
        super().__init__()

        self.role = role.lower()
        self.login_view = login_view

        self.title(
            f"Sistem Manajemen Perpustakaan - "
            f"Mode: {self.role.upper()}"
        )
        self.geometry("1000x600")
        self.minsize(850, 500)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # FRAME KIRI
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(
            row=0, column=0,
            padx=10, pady=10, sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Buku",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        self.label_role = ctk.CTkLabel(
            self.frame_kiri,
            text=f"Role: {self.role.upper()}",
            font=("Arial", 14)
        )
        self.label_role.pack(pady=5)

        # Pesan hak akses
        self.label_akses = ctk.CTkLabel(
            self.frame_kiri,
            text="",
            text_color="green",
            wraplength=350
        )
        self.label_akses.pack(pady=5, padx=10)

        # INPUT JUDUL
        self.entry_judul = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Judul Buku"
        )
        self.entry_judul.pack(
            pady=10, padx=15, fill="x"
        )

        # INPUT PENULIS
        self.entry_penulis = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Penulis"
        )
        self.entry_penulis.pack(
            pady=10, padx=15, fill="x"
        )

        # INPUT TAHUN
        self.entry_tahun = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Tahun Terbit (Misal: 2024)"
        )
        self.entry_tahun.pack(
            pady=10, padx=15, fill="x"
        )

        # TOMBOL SIMPAN
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color="green"
        )
        self.btn_simpan.pack(
            pady=(20, 5), padx=15, fill="x"
        )

        # TOMBOL UPDATE
        self.btn_update = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Data (Update)",
            fg_color="blue"
        )
        self.btn_update.pack(
            pady=5, padx=15, fill="x"
        )

        # TOMBOL DELETE
        self.btn_delete = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data (Delete)",
            fg_color="red"
        )
        self.btn_delete.pack(
            pady=5, padx=15, fill="x"
        )

        # TOMBOL LOGOUT
        self.btn_logout = ctk.CTkButton(
            self.frame_kiri,
            text="Logout",
            fg_color="#555555",
            hover_color="#333333",
            command=self.logout
        )
        self.btn_logout.pack(
            pady=(15, 10), padx=15, fill="x"
        )

        # FRAME KANAN: TABEL BUKU
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(
            row=0, column=1,
            padx=10, pady=10, sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Koleksi Buku",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        kolom = ("id", "judul", "penulis", "tahun")

        self.tabel = ttk.Treeview(
            self.frame_kanan,
            columns=kolom,
            show="headings",
            height=15
        )

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        self.tabel.column(
            "id", width=50, anchor="center"
        )
        self.tabel.column("judul", width=200)
        self.tabel.column("penulis", width=150)
        self.tabel.column(
            "tahun", width=100, anchor="center"
        )

        self.tabel.pack(
            fill="both", expand=True,
            padx=15, pady=10
        )

        # PENGATURAN HAK AKSES
        if self.role != "admin":

            self.label_akses.configure(
                text="AKSES TERKUNCI\n"
                     "Fitur ini hanya dapat digunakan oleh Admin.",
                text_color="red"
            )

            # Mengunci formulir
            self.entry_judul.configure(state="disabled")
            self.entry_penulis.configure(state="disabled")
            self.entry_tahun.configure(state="disabled")

            # Mengunci tombol pengelolaan buku
            self.btn_simpan.configure(
                state="disabled",
                text="Simpan (Khusus Admin)"
            )

            self.btn_update.configure(
                state="disabled",
                text="Update (Khusus Admin)"
            )

            self.btn_delete.configure(
                state="disabled",
                text="Delete (Khusus Admin)"
            )

        else:
            self.label_akses.configure(
                text="Anda memiliki akses penuh sebagai Admin.",
                text_color="green"
            )

    # LOGOUT
    def logout(self):
        self.destroy()

        if self.login_view is not None:
            self.login_view.deiconify()


if __name__ == "__main__":
    app = BukuView(role="anggota")
    app.mainloop()
