from package.database.koneksi import get_connection

# Buat koneksi ke database
conn = get_connection()

# Cursor untuk menjalankan query
cur = conn.cursor()

# Jalankan query untuk mengambil data wajah yang dikenal
cur.execute("SELECT id, nama_karyawan, foto_karyawan FROM data_karyawan")
rows = cur.fetchall()