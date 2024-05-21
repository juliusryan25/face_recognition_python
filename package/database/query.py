from package import *

# Fungsi untuk mengonversi gambar ke binary
def convert_to_binary(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

def upload_to_database(nama_karyawan, file_path, jam_masuk, conn):
    # Konversi gambar ke binary
    foto_absen = convert_to_binary(file_path)

    # Query untuk insert data
    query = """
    INSERT INTO data_absen (nama_karyawan, foto_absen, jam_masuk)
    VALUES (%s, %s, %s)
    """

    # Buka kursor baru
    cur = conn.cursor()

    try:
        # Eksekusi query
        cur.execute(query, (nama_karyawan, foto_absen, jam_masuk))
        # Commit perubahan
        conn.commit()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup kursor
        cur.close()

# Buat koneksi ke database
conn = get_connection()

with get_connection() as conn:
    try:
        # Jalankan query untuk mengambil data wajah yang dikenal
        with conn.cursor() as cur:
            cur.execute("SELECT id, nama_karyawan, foto_karyawan FROM data_karyawan")
            rows = cur.fetchall()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")