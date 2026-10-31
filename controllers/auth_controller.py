
import tkinter.messagebox as messagebox

from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()

        self.view.btn_login.configure(
            command=self.proses_login
        )

    # Proses login pengguna
    def proses_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Peringatan",
                "Username dan Password wajib diisi!"
            )
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {user['username']} "
                f"({user['role']})!"
            )

            # Menyembunyikan halaman login
            self.view.withdraw()

            try:
                # Membuka halaman buku sesuai role pengguna
                app_utama = BukuController(
                    user_role=user['role'],
                    login_view=self.view
                )

                app_utama.run()

            except Exception as e:
                self.view.deiconify()

                messagebox.showerror(
                    "Kesalahan",
                    f"Gagal membuka halaman buku:\n{e}"
                )

        else:
            messagebox.showerror(
                "Login Gagal",
                "Username atau Password salah!"
            )

    # Menjalankan halaman login
    def run(self):
        self.view.mainloop()
