import flask
import database


DB_URL = ""
app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route('/api/get_tables', methods=['GET'])
def get_tables():
    tables = database.get_table_names(DB_URL)
    print(DB_URL)
    print(tables)
    return flask.jsonify(tables)
