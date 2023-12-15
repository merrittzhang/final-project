import os
import shutil

import database

import pytest


TEST_DB = "example_dbs/reg.sqlite"
TEST_DB2 = "example_dbs/reg_test.sqlite" # Use this for anything that modifies db


class TestDatabase:
    @pytest.fixture
    def setup(self):
        if not os.path.exists(TEST_DB2):
            shutil.copy(TEST_DB, TEST_DB2)
        yield
        os.remove(TEST_DB2)

    def test_get_tables(self):
        tables = database.get_table_names(TEST_DB)
        ref = ['classes', 'courses', 'coursesprofs', 'crosslistings', 'profs']
        assert tables == ref

    def test_get_columns(self):
        columns = database.get_columns(TEST_DB, "classes")
        ref = ['classid', 'courseid', 'days', 'starttime', 'endtime', 'bldg', 'roomnum']
        assert columns == ref
    
    def test_get_types(self):
        columns = database.get_columns(TEST_DB, "classes")
        ref = {
            'classid': "INTEGER",
            'courseid': "INTEGER",
            'days': "TEXT",
            'starttime': "TEXT",
            'endtime': "TEXT",
            'bldg': "TEXT",
            'roomnum': "TEXT"}
        types = database.get_column_data_types(TEST_DB, "classes")
        assert len(types) == len(ref)
        for key, val in ref.items():
            assert types[key] == val

    def test_get_all(self):
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

    def test_update(self, setup):
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
    
    def test_delete(self, setup):
        ref_len = 1493
        del_row = {
            'classid': 7838,
            'courseid': 3457,
            'days': 'M',
            'starttime': '01:30 PM',
            'endtime': '04:20 PM',
            'bldg': 'CHANC',
            'roomnum': '105'
        }
        ref_row = {
            'classid': 7839,
            'courseid': 3458,
            'days': 'W',
            'starttime': '07:30 PM',
            'endtime': '10:20 PM',
            'bldg': 'MARXH',
            'roomnum': '101'
        }

        database.delete(TEST_DB2, "classes", del_row)
        rows = database.get_all(TEST_DB2, "classes")
        assert len(rows) == ref_len
        for key, val in rows[0].items():
            assert ref_row[key] == val
    
    def test_create(self, setup):
        ref_len = 1495
        new_row = {
            'classid': 0000,
            'courseid': 0000,
            'days': 'TEST',
            'starttime': '00:00 PM',
            'endtime': '00:00 PM',
            'bldg': 'TEST',
            'roomnum': '1234'
        }
        ref_row = {
            'classid': 7838,
            'courseid': 3457,
            'days': 'M',
            'starttime': '01:30 PM',
            'endtime': '04:20 PM',
            'bldg': 'CHANC',
            'roomnum': '105'
        }
        database.insert(TEST_DB2, "classes", new_row)
        rows = database.get_all(TEST_DB2, "classes")
        assert len(rows) == ref_len
        for key, val in rows[0].items():
            assert ref_row[key] == val
        for key, val in rows[-1].items():
            assert new_row[key] == val
    
    def test_join(self):
        ref_len = 1648
        ref_row = {
            'courseid': 3457,
            'area': "LA",
            'title': 'Music from the Hispanophone Caribbean',
            'prereqs': '',
            'dept': 'AAS',
            'coursenum': '310',
            'profid': 481,
            'profname': 'Alexandra T. Vazquez'
        }
        prim_table = 'courses'
        tables = ['crosslistings', 'coursesprofs', 'profs']
        identifiers = [[('courses', 'courseid', 'crosslistings', 'courseid')], 
                       [('courses', 'courseid', 'coursesprofs', 'courseid')], 
                       [('coursesprofs', 'profid', 'profs', 'profid')]]
        rows = database.join(TEST_DB, prim_table, tables, identifiers)
        assert len(rows) == ref_len
        for key, val in ref_row.items():
            assert rows[0][key] == val
    
    @pytest.mark.stress
    def test_stress1(self, setup):
        iters = 1
        ref_len = 1494
        for i in range(iters):
            rows = database.get_all(TEST_DB2, 'classes')
            for row in rows:
                database.delete(TEST_DB2, 'classes', row)
            rows_deleted = database.get_all(TEST_DB2, 'classes')
            assert len(rows_deleted) == 0
            for row in rows:
                database.insert(TEST_DB2, 'classes', row)
            rows_restored = database.get_all(TEST_DB2, 'classes')
            assert len(rows_restored) == ref_len
    
    @pytest.mark.stress
    def test_stress2(self, setup):
        iters = 2
        ref_len = 1494
        for i in range(iters):
            rows = database.get_all(TEST_DB2, 'classes')
            for row in rows:
                database.delete(TEST_DB2, 'classes', row)
            rows_deleted = database.get_all(TEST_DB2, 'classes')
            assert len(rows_deleted) == 0
            for row in rows:
                database.insert(TEST_DB2, 'classes', row)
            rows_restored = database.get_all(TEST_DB2, 'classes')
            assert len(rows_restored) == ref_len
