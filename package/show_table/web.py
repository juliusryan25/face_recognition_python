from package import *

app = Flask(__name__)

@app.route('/')
def index():
    attendance_data = fetch_data()
    return render_template('index.html', attendance_data=attendance_data)

if __name__ == '__main__':
    app.run(debug=True)