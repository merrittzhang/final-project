import db

database = db("Not sure exactly how to intialize the database")
tables = database.get_tables()
print(tables)

columns = database.get_columns("get table")
print(columns)

rows = database.select("get table")
print(rows)

# Update, Insert, Delete, and Join can be used similarly.
