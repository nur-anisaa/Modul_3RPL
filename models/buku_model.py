
from config.database import Database


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    # MENAMPILKAN SEMUA DATA BUKU
    def get_all_buku(self):
        if not self.conn:
            print("Koneksi database gagal!")
            return []

        cursor = None

        try:
            cursor = self.conn.cursor(dictionary=True)

            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)

            return cursor.fetchall()

        except Exception as e:
            print("Gagal mengambil data buku:", repr(e))
            return []

        finally:
            if cursor is not None:
                cursor.close()

    # MENYIMPAN DATA BUKU
    def create_buku(self, judul, penulis, tahun_terbit):
        if not self.conn:
            print("Koneksi database gagal!")
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = f"""
                INSERT INTO {self.table_name}
                (judul, penulis, tahun_terbit)
                VALUES (%s, %s, %s)
            """

            values = (
                judul,
                penulis,
                int(tahun_terbit)
            )

            cursor.execute(query, values)
            self.conn.commit()

            print("Data buku berhasil disimpan!")
            return True

        except Exception as e:
            self.conn.rollback()
            print("Gagal menyimpan data buku:", repr(e))
            return False

        finally:
            if cursor is not None:
                cursor.close()

    # MEMPERBARUI DATA BUKU
    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if not self.conn:
            print("Koneksi database gagal!")
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = f"""
                UPDATE {self.table_name}
                SET judul = %s,
                    penulis = %s,
                    tahun_terbit = %s
                WHERE id_buku = %s
            """

            values = (
                judul,
                penulis,
                int(tahun_terbit),
                int(id_buku)
            )

            cursor.execute(query, values)

            jumlah_perubahan = cursor.rowcount

            self.conn.commit()

            if jumlah_perubahan > 0:
                print("Data buku berhasil diperbarui!")
                return True

            # Memeriksa apakah ID buku masih tersedia
            cursor.execute(
                f"""
                SELECT id_buku
                FROM {self.table_name}
                WHERE id_buku = %s
                """,
                (int(id_buku),)
            )

            buku_ditemukan = cursor.fetchone() is not None

            if buku_ditemukan:
                print("Data buku tidak mengalami perubahan.")
                return True

            print(f"Buku dengan ID {id_buku} tidak ditemukan.")
            return False

        except Exception as e:
            self.conn.rollback()
            print("Gagal memperbarui data buku:", repr(e))
            return False

        finally:
            if cursor is not None:
                cursor.close()

    # MENGHITUNG RIWAYAT PEMINJAMAN
    def hitung_peminjaman_buku(self, id_buku):
        if not self.conn:
            print("Koneksi database gagal!")
            return None

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = """
                SELECT COUNT(*)
                FROM peminjaman
                WHERE id_buku = %s
            """

            cursor.execute(query, (int(id_buku),))

            hasil = cursor.fetchone()

            return hasil[0] if hasil else 0

        except Exception as e:
            print("Gagal memeriksa riwayat peminjaman:", repr(e))
            return None

        finally:
            if cursor is not None:
                cursor.close()

    # MENGHAPUS BUKU BESERTA RIWAYAT PEMINJAMAN
    def delete_buku(self, id_buku):
        if not self.conn:
            print("Koneksi database gagal!")
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            # 1. Menghapus riwayat peminjaman buku terlebih dahulu
            query_peminjaman = """
                DELETE FROM peminjaman
                WHERE id_buku = %s
            """

            cursor.execute(
                query_peminjaman,
                (int(id_buku),)
            )

            jumlah_peminjaman = cursor.rowcount

            # 2. Menghapus data buku
            query_buku = f"""
                DELETE FROM {self.table_name}
                WHERE id_buku = %s
            """

            cursor.execute(
                query_buku,
                (int(id_buku),)
            )

            jumlah_buku = cursor.rowcount

            # Memastikan buku ditemukan
            if jumlah_buku == 0:
                self.conn.rollback()
                print(f"Buku ID {id_buku} tidak ditemukan.")
                return False

            # 3. Menyimpan kedua proses penghapusan
            self.conn.commit()

            print(
                f"Buku ID {id_buku} berhasil dihapus "
                f"beserta {jumlah_peminjaman} riwayat peminjaman."
            )

            return True

        except Exception as e:
            # Membatalkan seluruh penghapusan jika terjadi kesalahan
            self.conn.rollback()
            print("Gagal menghapus data buku:", repr(e))
            return False

        finally:
            if cursor is not None:
                cursor.close()
