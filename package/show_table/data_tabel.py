# from package import *
# app = Flask(__name__)

# @app.route('/')
# def index():
#     # Jalankan query khusus Anda
#     sql_query = text("SELECT * FROM ( SELECT id, nama_karyawan, jam_pulang, nik FROM data_absen_pulang ORDER BY id DESC LIMIT 10 ) AS sub ORDER BY id ASC")
#     result = db.engine.execute(sql_query)
#     data = [dict(row) for row in result]

#     # Kirim data ke template
#     return render_template('index.html', custom_data=data)