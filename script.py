import sqlite3


conn = sqlite3.connect("data.db")

username="fareedah"
password="sassarievents1234"

row = conn.execute("""
    SELECT blog_details FROM blog_data 
""").fetchall()

print(row)


# row = conn.execute("""
#     SELECT blog_details from blog_data """).fetchall()

# # for i in row:
# #     a = i[0]
# #     l = round(len(i[0])/2)
# #     a = a[0:l] + "..."
# #     print(a)


# def cut(content):
#     lis = []
#     for i in content:
#         a = i[0]
#         l = round(len(i[0])/2)
#         a = a[0:l] + "..."
#         lis.append(a)
    
#     return lis 

# print(cut(row))
# # print(row)

# conn.execute("""
#     INSERT INTO admin_details (username, password) values (?,?)
# """, ("fareedah", "sassarievents123")
# )


# conn.execute("""
#     CREATE TABLE drafts (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         blog_title TEXT,
#         blog_details TEXT
#     )
# """)


# conn.commit()

# if row == None:
#     print("nahhh")


# import uuid

# print(uuid.uuid4())
