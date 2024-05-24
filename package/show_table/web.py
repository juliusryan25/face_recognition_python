from package import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sql123@localhost/xacti'
db = SQLAlchemy(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data_masuk')
def get_data_masuk():
    # Ambil data dari database
    data = fetch_data_masuk(conn)
    return jsonify(data)

@app.route('/get_data_pulang')
def get_data_pulang():
    # Ambil data dari database
    data = fetch_data_pulang(conn)
    return jsonify(data)

# @app.route('/')
# def index():
#     # Buat koneksi ke database
#     conn = get_connection()
#     # Gunakan fungsi fetch_data untuk mengambil data kehadiran
#     attendance_data = fetch_data(conn)
#     # Pastikan untuk menutup koneksi setelah selesai
#     conn.close()
#     # Kirim data kehadiran ke template
#     return render_template('index.html', attendance_data=attendance_data)

# from flask import Flask, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sql123@localhost/xacti'
# db = SQLAlchemy(app)

# def fetch_data(conn):
#     try:
#         with conn.cursor() as cur:
#             cur.execute("SELECT * FROM ( SELECT id, nama_karyawan, jam_masuk, nik FROM data_absen ORDER BY id DESC LIMIT 10 ) AS sub ORDER BY id ASC")
#             return cur.fetchall()
#     except Exception as e:
#         print("Error fetching data masuk: ", e)
#         return None

# def fetch_data_pulang(conn):
#     try:
#         with conn.cursor() as cur:
#             cur.execute("SELECT * FROM ( SELECT id, nama_karyawan, jam_pulang, nik FROM data_absen_pulang ORDER BY id DESC LIMIT 10 ) AS sub ORDER BY id ASC")
#             return cur.fetchall()
#     except Exception as e:
#         print("Error fetching data pulang: ", e)
#         return None

# # Pastikan untuk mendefinisikan 'conn' di sini
# # conn = ...

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_data_masuk')
# def get_data_masuk():
#     data = fetch_data(conn)
#     if data is not None:
#         return jsonify(data)
#     else:
#         return jsonify({"error": "Gagal mengambil data masuk"}), 500

# @app.route('/get_data_pulang')
# def get_data_pulang():
#     data = fetch_data_pulang(conn)
#     if data is not None:
#         return jsonify(data)
#     else:
#         return jsonify({"error": "Gagal mengambil data pulang"}), 500
