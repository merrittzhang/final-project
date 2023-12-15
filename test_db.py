import database

TEST_DB = "example_dbs/reg.sqlite"
TEST_DB2 = "example_dbs/reg_copy.sqlite" # Use this for anything that modifies db

def test_get_tables():
    tables = database.get_table_names(TEST_DB)
    ref = ['classes', 'courses', 'coursesprofs', 'crosslistings', 'profs']
    assert tables == ref

def test_get_columns():
    columns = database.get_columns(TEST_DB, "classes")
    ref = ['classid', 'courseid', 'days', 'starttime', 'endtime', 'bldg', 'roomnum']
    assert columns == ref

def test_get_all():
    rows = database.get_all(TEST_DB, "classes")
    ref_len = 1494
    ref_row = {
        'classid': 7838,
        'courseid': 3457,
        'days': 'M',
        'starttime': '01:30 PM',
        'endtime': '04:20 PM',
        'bldg': 'CHANC',
        'roomnum': '105'
    }
    assert len(rows) == ref_len
    for key, val in rows[0].items():
        assert ref_row[key] == val

def test_update():
    update_vals = {
        'days': 'TEST!!!',
        'roomnum': 'TEST'
    }
    id_vals = {
        'classid': 7838,
        'courseid': 3457
    }
    ref_len = 1494
    ref_row = {
        'classid': 7838,
        'courseid': 3457,
        'days': 'TEST!!!',
        'starttime': '01:30 PM',
        'endtime': '04:20 PM',
        'bldg': 'CHANC',
        'roomnum': 'TEST'
    }
    original_row = {
        'classid': 7838,
        'courseid': 3457,
        'days': 'M',
        'starttime': '01:30 PM',
        'endtime': '04:20 PM',
        'bldg': 'CHANC',
        'roomnum': '105'
    }
    database.update(TEST_DB2, "classes", update_vals, id_vals)
    
    rows = database.get_all(TEST_DB2, "classes")
    assert len(rows) == ref_len
    for key, val in rows[0].items():
        assert ref_row[key] == val
    
    database.update(TEST_DB2, "classes", original_row, rows[0])

    rows = database.get_all(TEST_DB2, "classes")
    assert len(rows) == ref_len
    for key, val in rows[0].items():
        assert original_row[key] == val




# From Database.py
# db_file = "reg.sqlite"
#     tables = get_table_names(db_file)
#     print(tables)

#     columns = get_columns(db_file, 'classes')
#     print(columns)

#     classes = get_all(db_file, 'classes')
#     print(f"Num classes: {len(classes)}")
#     print(f"First 10:")
#     for clss in classes[0:10]:
#         print(f"{clss['classid']} - {clss['courseid']}")

#     delete(db_file, 'classes', 7838)

#     classes = get_all(db_file, 'classes')
#     print(f"Num classes: {len(classes)}")
#     print(f"First 10:")
#     for clss in classes[0:10]:
#         print(f"{clss['classid']} - {clss['courseid']}")


#     class_dict = {
#         'classid' : 7838, 
#         'courseid': 3457, 
#         'days': 'M',
#         'starttime': '01:30 PM',
#         'endtime': '04:20 PM', 
#         'bldg': 'CHANC', 
#         'roomnum': 105,
#     }

#     insert(db_file, 'classes', class_dict)

#     classes = get_all(db_file, 'classes')
#     print(f"Num classes: {len(classes)}")
#     print(f"First 10:")
#     for clss in classes[0:len(classes)]:
#         print(f"{clss['classid']} - {clss['courseid']}")

#     update_dict = {
#         'courseid': 3458, 
#     }

#     update(db_file, 'classes', update_dict, 7838)

#     classes = get_all(db_file, 'classes')
#     print(f"Num classes: {len(classes)}")
#     print(f"First 10:")
#     for clss in classes[0:len(classes)]:
#         print(f"{clss['classid']} - {clss['courseid']}")

