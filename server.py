import flask
import database


DB_URL = ""
app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/tables/<name>', methods=['GET'])
def index(name=""):
    return flask.render_template('index.html')


@app.route('/api/get_tables', methods=['GET'])
def get_tables():
    tables = database.get_table_names(DB_URL)
    print(DB_URL)
    print(tables)
    return flask.jsonify(tables)


@app.route('/api/tables/<name>', methods=['GET'])
def get_table(name):
    data = []
    try:
        columns = database.get_columns(DB_URL, name)
        data = database.get_all(DB_URL, name)
        return flask.jsonify({"columns": columns, "data": data})
    except database.InvalidTable as ex:
        print(ex)
        return flask.abort(400)
    except Exception as ex:
        print(ex)
        return flask.abort(500)
