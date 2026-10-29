
from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi model
    model = BukuModel()

    # Membuat mock koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Menjalankan fungsi simpan buku
    hasil = model.create_buku(
        "Buku Testing",
        "Penulis QA",
        2026
    )

    # Memastikan fungsi berhasil
    assert hasil is True

    # Memastikan query dijalankan
    mock_cursor.execute.assert_called_once()

    # Memastikan commit dipanggil
    model.conn.commit.assert_called_once()
