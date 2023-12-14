import database

db_file = "reg.sqlite"

def test_get_table_names():
    names = database.get_table_names(db_file)

    for name in names:
        print(name)

def test_get_column_names():
    table = "classes"
    columns = database.get_columns(db_file, table)
    for column_name in columns:
        print(column_name)

def test_column_data_types():
    table = "classes"
    column_data_types = database.get_column_data_types(db_file, table)
    for column, data_type in column_data_types.items():
        print(f"Column: {column}, Data Type: {data_type}")

def test_get_all():
    classes = database.get_all(db_file, 'classes')
    print(f"Num classes: {len(classes)}")

    for classs in classes:
        print(f"{classs['classid']} - {classs['courseid']}")

def test_update():
    table = "classes"
    update_dict = {
        'courseid': 3458, 
    }
    classid = 7838
    database.update(db_file, 'classes', update_dict, classid)
    for column in table:
        print(f"Column: {column}")

def test_insert():
    table = "classes"
    class_dict = {
        'classid' : 7838, 
        'courseid': 3457, 
        'days': 'M',
        'starttime': '01:30 PM',
        'endtime': '04:20 PM', 
        'bldg': 'CHANC', 
        'roomnum': 105,
    }
    database.insert(db_file, table, class_dict)
    for column in table:
        print(f"Column: {column}")

def test_delete():
    table = "classes"
    classid = 7838
    database.delete(db_file, table, classid)
    for column in table:
        print(f"Column: {column}")

def test_inner_join():
    joined_data = database.inner_join(db_file, 'classes', 'courses', 'classid')
    for row in joined_data:
        print(row)

def test_inner_join_multiple_tables():
    db_file = "reg.sqlite"
    tables = ['classes', 'courses', 'crosslistings']
    joined_data = database.inner_join_multiple_tables(db_file, tables, 'classid')
    for row in joined_data:
        print(row)