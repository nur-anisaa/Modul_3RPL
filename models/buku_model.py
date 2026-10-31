
from config.database import Database


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    # MENAMPILKAN DATA BUKU
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
            print("Gagal mengambil data:", repr(e))
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

            cursor.execute(
                query,
                (judul, penulis, int(tahun_terbit))
            )

            self.conn.commit()

            print("Data buku berhasil disimpan!")
            return True

        except Exception as e:
            self.conn.rollback()
            print("Gagal menyimpan data:", repr(e))
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

            cursor.execute(
                query,
                (
                    judul,
                    penulis,
                    int(tahun_terbit),
                    int(id_buku)
                )
            )

            jumlah_perubahan = cursor.rowcount

            self.conn.commit()

            # Jika ada perubahan, Update berhasil
            if jumlah_perubahan > 0:
                print("Data buku berhasil diperbarui!")
                return True

            # Memeriksa apakah ID buku masih tersedia
            query_cek = f"""
                SELECT id_buku
                FROM {self.table_name}
                WHERE id_buku = %s
            """

            cursor.execute(query_cek, (int(id_buku),))

            buku_ditemukan = cursor.fetchone() is not None

            if buku_ditemukan:
                print("Data buku ditemukan dan tidak mengalami perubahan.")
                return True

            print(f"Buku dengan ID {id_buku} tidak ditemukan.")
            return False

        except Exception as e:
            self.conn.rollback()
            print("Gagal memperbarui data:", repr(e))
            return False

        finally:
            if cursor is not None:
                cursor.close()

    # MENGHAPUS DATA BUKU
    def delete_buku(self, id_buku):
        if not self.conn:
            print("Koneksi database gagal!")
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = f"""
                DELETE FROM {self.table_name}
                WHERE id_buku = %s
            """

            cursor.execute(query, (int(id_buku),))

            jumlah_dihapus = cursor.rowcount

            self.conn.commit()

            if jumlah_dihapus > 0:
                print("Data buku berhasil dihapus!")
                return True

            print(f"Buku dengan ID {id_buku} tidak ditemukan.")
            return False

        except Exception as e:
            self.conn.rollback()
            print("Gagal menghapus data:", repr(e))
            return False

        finally:
            if cursor is not None:
                cursor.close()
