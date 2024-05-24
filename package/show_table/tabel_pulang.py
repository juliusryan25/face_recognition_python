from package import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:juliusryanlistianto25@localhost/data_absen_pulang'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data_pulang')
def get_data_pulang():
    # Ambil data dari database
    data_pulang = fetch_data_pulang(conn)
    return jsonify(data_pulang)
