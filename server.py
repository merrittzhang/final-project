import flask
import database


DB_URL = ""
app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/tables/<name>', methods=['GET'])
@app.route('/join', methods=['GET'])
@app.route('/join/result', methods=['GET'])
def index(name=""):
    return flask.render_template('index.html')


@app.route('/api/get_tables', methods=['GET'])
def get_tables():
    tables = database.get_table_names(DB_URL)
    return flask.jsonify(tables)


@app.route('/api/get_columns')
def get_all_columns():
    data = []
    try:
        tables = database.get_table_names(DB_URL)
        columns = {}
        for table in tables:
            columns[table] = database.get_columns(DB_URL, table)
        return flask.jsonify(columns)
    except database.InvalidTable as ex:
        print(ex)
        return flask.abort(400)
    except Exception as ex:
        print(ex)
        return flask.abort(500)


@app.route('/api/get_all/<table>', methods=['GET'])
def get_table(table):
    data = []
    try:
        columns = database.get_columns(DB_URL, table)
        data = database.get_all(DB_URL, table)
        return flask.jsonify({"columns": columns, "data": data})
    except database.InvalidTable as ex:
        print(ex)
        return flask.abort(400)
    except Exception as ex:
        print(ex)
        return flask.abort(500)


@app.route('/api/join', methods=['POST'])
def join():
    try:
        data = flask.request.json
        prim_table = data["prim_table"]
        tables = data["tables"]
        identifiers = data["identifiers"]
        print(prim_table)
        print(tables)
        print(identifiers)
        result = database.join(DB_URL, prim_table, tables, identifiers)
        return flask.jsonify(result)
    except database.DatabaseError as ex:
        print(ex)
        flask.abort(500)
    except Exception as ex:
        print(ex)
        flask.abort(400)
