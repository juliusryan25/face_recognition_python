from package import *
app = Flask(__name__)

@app.route('/')
def index():
    # Jalankan query khusus Anda
    sql_query = text("YOUR RAW SQL QUERY HERE")
    result = db.engine.execute(sql_query)
    data = [dict(row) for row in result]

    # Kirim data ke template
    return render_template('index.html', custom_data=data)