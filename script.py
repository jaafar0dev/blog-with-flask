import sqlite3


conn = sqlite3.connect("data.db")

username="fareedah"
password="sassarievents1234"

# row = conn.execute("""
#     SELECT * FROM blog_data 
# """).fetchall()

# print(row)


# row = conn.execute("""
#     SELECT * FROM admin_details """).fetchall()

# conn.execute("""
#     INSERT INTO admin_details (username, password) values (?,?)
# """, ("fareedah", "sassarievents123")
# )


conn.execute("""
    CREATE TABLE drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blog_title TEXT,
        blog_details TEXT
    )
""")


conn.commit()

# if row == None:
#     print("nahhh")


# import uuid

# print(uuid.uuid4())
