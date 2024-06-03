from package import *

# Fungsi untuk mengonversi gambar ke binary
def convert_to_binary(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

def upload_to_database(nama_karyawan, file_path, jam_masuk, nik_karyawan,keterangan, conn):
    # Konversi gambar ke binary
    foto_absen = convert_to_binary(file_path)

    # Query untuk insert data
    query = """
    INSERT INTO data_absen (nama_karyawan, foto_absen, jam_masuk, nik, keterangan)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Buka kursor baru
    cur = conn.cursor()

    try:
        # Eksekusi query
        cur.execute(query, (nama_karyawan, foto_absen, jam_masuk, nik_karyawan, keterangan))
        # Commit perubahan
        conn.commit()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup kursor
        cur.close()

# Fungsi untuk mengonversi gambar ke binary _absen pulang
def convert_to_binary_pulang(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

def upload_to_database_pulang(nama_karyawan, file_path, jam_pulang, nik_karyawan, conn):
    # Konversi gambar ke binary
    foto_absen = convert_to_binary(file_path)

    # Query untuk insert data
    query = """
    INSERT INTO data_absen_pulang (nama_karyawan, foto_absen, jam_pulang, nik)
    VALUES (%s, %s, %s, %s)
    """

    # Buka kursor baru
    cur = conn.cursor()

    try:
        # Eksekusi query
        cur.execute(query, (nama_karyawan, foto_absen, jam_pulang, nik_karyawan))
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
            cur.execute("SELECT id, nama_karyawan, foto_karyawan ,nik FROM data_karyawan")
            rows = cur.fetchall()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def fetch_data_masuk(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM ( SELECT id, nama_karyawan, jam_masuk, nik FROM data_absen ORDER BY id DESC LIMIT 5 ) AS sub ORDER BY id ASC")
        return cur.fetchall()

def fetch_data_pulang(conn):
    with conn.cursor() as cer:
        cer.execute("SELECT * FROM ( SELECT id, nama_karyawan, jam_pulang, nik FROM data_absen_pulang ORDER BY id DESC LIMIT 5 ) AS sub ORDER BY id ASC")
        return cer.fetchall()
    
# def fetch_data_absen(conn):
#     with conn.cursor() as cer:
#         cer.execute(";with tb1 as (SELECT nik, nama_karyawan,min(jam_masuk) jam_masuk,cast(jam_masuk as date) dt, 'IN' FROM public.data_absen group by nik, nama_karyawan,cast(jam_masuk as date)), tb2 as (SELECT nik, nama_karyawan,max(jam_pulang) jam_pulang,cast(jam_pulang as date) dt,'OUT' FROM public.data_absen_pulang group by nik, nama_karyawan,cast(jam_pulang as date)) select a.nik,a.nama_karyawan,jam_masuk, b.jam_pulang from tb1 a left join tb2 b on a.nik =b.nik and a.dt = b.dt where DATE(a.jam_masuk) = CURRENT_DATE LIMIT 10;")
#         return cer.fetchall()

def fetch_data_absen(conn):
    with conn.cursor() as cer:
        cer.execute("WITH tb1 AS (SELECT nik, nama_karyawan, keterangan, MIN(jam_masuk) AS jam_masuk, CAST(jam_masuk AS date) AS dt, 'IN' AS tipe FROM public.data_absen GROUP BY nik, nama_karyawan, keterangan, CAST(jam_masuk AS date)), tb2 AS (SELECT nik, nama_karyawan, MAX(jam_pulang) AS jam_pulang, CAST(jam_pulang AS date) AS dt, 'OUT' AS tipe FROM public.data_absen_pulang GROUP BY nik, nama_karyawan, CAST(jam_pulang AS date)), tb3 AS (SELECT nik, nama_karyawan, departemen, jam_kerja FROM public.data_karyawan GROUP BY nik, nama_karyawan, departemen, jam_kerja) SELECT a.nik, a.nama_karyawan, a.jam_masuk, b.jam_pulang, c.departemen, c.jam_kerja, a.keterangan FROM tb1 a LEFT JOIN tb2 b ON a.nik = b.nik AND a.dt = b.dt LEFT JOIN tb3 c ON a.nik = c.nik WHERE DATE(a.jam_masuk) = CURRENT_DATE ORDER BY CASE WHEN b.jam_pulang IS NOT NULL THEN b.jam_pulang ELSE a.jam_masuk END DESC LIMIT 10;")
        return cer.fetchall()
