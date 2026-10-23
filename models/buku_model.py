
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
            if cursor:
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
            if cursor:
                cursor.close()

    # MENGUBAH DATA BUKU
    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if not self.conn:
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
                (judul, penulis, int(tahun_terbit), id_buku)
            )

            self.conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            self.conn.rollback()
            print("Gagal mengubah data:", repr(e))
            return False

        finally:
            if cursor:
                cursor.close()

    # MENGHAPUS DATA BUKU
    def delete_buku(self, id_buku):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()

            query = f"""
                DELETE FROM {self.table_name}
                WHERE id_buku = %s
            """

            cursor.execute(query, (id_buku,))
            self.conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            self.conn.rollback()
            print("Gagal menghapus data:", repr(e))
            return False

        finally:
            if cursor:
                cursor.close()
