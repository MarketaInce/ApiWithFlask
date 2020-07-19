"""
TEST
"""

import sqlite3

# -- Starting Boilerplate/Setup -- #
# Create a connection
connection = sqlite3.connect('data.db')

# Create a cursor into the database
cursor = connection.cursor()

# -- SQL QUERIES -- #
# Create table query: Create a table from scratch.
create_table = "CREATE TABLE users (id int, username text, password text)"
# Insert into table query: Create one or more new rows
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# Select all rows from query: to show all the rows one by one.
select_query = "SELECT * FROM users"

# -- QUERY EXECUTION -- #
# Execute the cursor to create table.
cursor.execute(create_table)

# Execute the cursor to insert into table.
user = (1, 'jose', 'asdf')
cursor.execute(insert_query, user)

# Execute the cursor to insert multiple rows into table.
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')
]
cursor.executemany(insert_query, users)

# Select from the table.
for row in cursor.execute(select_query):
    print(row)

# -- Ending Boilerplate/Teardown -- #
# Connection commit
connection.commit()

# Close Connection
connection.close()



