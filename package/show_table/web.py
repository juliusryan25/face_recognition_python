from package import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:juliusryanlistianto25@localhost/data_absen'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data_masuk')

def get_data_masuk():
    # Ambil data dari database
    data = fetch_data(conn)
    return jsonify(data)
