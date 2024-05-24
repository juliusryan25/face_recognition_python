from package import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sql123@localhost/data_absen'
db = SQLAlchemy(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    # Ambil data dari database
    data = fetch_data(conn)
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