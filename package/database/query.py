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
        cer.execute("with tb1 as (SELECT nik, nama_karyawan, keterangan, min(jam_masuk) jam_masuk,cast(jam_masuk as date) dt, 'IN' FROM public.data_absen group by nik, nama_karyawan, keterangan, cast(jam_masuk as date)), tb2 as (SELECT nik, nama_karyawan,max(jam_pulang) jam_pulang,cast(jam_pulang as date) dt,'OUT'FROM public.data_absen_pulang group by nik, nama_karyawan,cast(jam_pulang as date)), tb3 as (SELECT nik, nama_karyawan, departemen, jam_kerja FROM public.data_karyawan group by nik, nama_karyawan, departemen, jam_kerja) select a.nik, a.nama_karyawan, jam_masuk, b.jam_pulang, c.departemen, c.jam_kerja, a.keterangan from tb1 a left join tb2 b on a.nik = b.nik and a.dt = b.dt left join tb3 c on a.nik = c.nik where DATE(a.jam_masuk) = CURRENT_DATE LIMIT 10;")
        return cer.fetchall()