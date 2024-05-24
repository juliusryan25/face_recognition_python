from package import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sql123@localhost/xacti'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data_masuk')
def get_data():
    # Ambil data dari database
    data = fetch_data_pulang(conn)
    return jsonify(data)

@app.route('/get_data_pulang')
def get_data_pulang():
    # Ambil data dari database
    data = fetch_data_pulang(conn)
    return jsonify(data)
