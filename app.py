from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
import sqlite3
import datetime
import uuid
import os
from werkzeug.security import safe_join

app = Flask(__name__)
DB_PATH = "data.db"
app.secret_key = "4c687e38-642c-4c94-90b9-e1424c6997a1"  # Required for session management
directory = "templates/blogs"
upload_folder = "static/uploads"
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(directory, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Create blog info table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blog_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blog_title TEXT,
                blog_details TEXT,
                blog_date TEXT,
                blog_id TEXT,
                blog_thumbnail TEXT
            )
        """)
        # Create admin_details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        """)
try:
    init_db()
except Exception as e:
    print(str(e))
    

@app.route('/')
def hello():
    return "Hello"


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            row = cursor.execute("""
                SELECT * FROM admin_details WHERE username =? and password = ? 
            """, (username, password)).fetchone()
            
            if row:
                session["admin_logged_in"] = True
                return redirect(url_for("dashboard"))  # Redirect to the dashboard
            else:
                return {"Output": "Wrong Admin Details"}

    return render_template("admin.html")

@app.route('/dashboard')
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))  # Redirect back if not logged in
    return render_template("dashboard.html")

@app.route('/blogs')
def blogs():
    with sqlite3.connect(DB_PATH) as conn:
        blogs = conn.execute(
        """
            SELECT * FROM blog_data ORDER BY id DESC
        """).fetchall()

    return render_template('bloglist.html', blogs=blogs)

@app.route('/view_blog/<blog_id>')
def view_blog(blog_id):
    file_path = os.path.join("templates", "blogs", f"{blog_id}.html")
    if not os.path.exists(file_path):
        return "Blog Not Found", 404
    return render_template(f"blogs/{blog_id}.html")

@app.route('/publish_blog', methods=["POST"])
def publish():
        if request.method == "POST":
            blog_title = request.form.get("blog_title")
            blog_details = request.form.get("blog_details")
            blog_date = datetime.date.today()
            blog_id = str(uuid.uuid4())
            filename = blog_id+'.html'
            blog_thumbnail = request.files["thumbnail"]

            if blog_thumbnail:
                image_filename = f"{blog_id}_{blog_thumbnail.filename}"
                image_path = os.path.join(upload_folder, image_filename)
                blog_thumbnail.save(image_path)

            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
            """
                INSERT INTO blog_data (blog_title, blog_details, blog_date, blog_id, blog_thumbnail) values (?, ?, ?, ?, ?)

            """, (blog_title, blog_details, blog_date, blog_id, image_filename))

            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            with open(file_path, 'w') as blog_file:
                blog_file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{blog_title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .container {{
                    max-width: 800px;
                    margin: auto;
                    padding: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #007bff;
                }}
                .date {{
                    color: #6c757d;
                    font-size: 0.9em;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <img src="/static/uploads/{image_filename}" style="width: 70vw">
                <h1>{blog_title}</h1>
                <p class="date">Published on: {blog_date}</p>
                <p>{blog_details}</p>
            </div>
        </body>
        </html>
        """)
            return redirect(url_for("dashboard"))
        return redirect(url_for("dashboard"))

@app.route('/drafts')
def drafts():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))  # Redirect back if not logged in
    with sqlite3.connect(DB_PATH) as conn:
        drafts = conn.execute(
    """
        SELECT * FROM drafts
    """).fetchall()
    
    return render_template('drafts.html', drafts=drafts)

@app.route('/edit-draft/<id>')
def edit_draft(id):
    with sqlite3.connect(DB_PATH) as conn:
       draft = conn.execute(
    """
        SELECT * FROM drafts WHERE id = ?
    """, id).fetchone()
    return render_template('edit_draft.html', draft=draft)

@app.route('/save_draft', methods=['POST'])
def save_draft():
    blog_title = request.form.get("blog_title")
    blog_details = request.form.get("blog_details")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
        """
            INSERT INTO drafts (blog_title, blog_details) values (?,?)
        """, (blog_title, blog_details))
        conn.commit()
    return redirect("dashboard")
@app.route('/logout')
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin"))

if __name__ == '__main__':
    app.run(debug=True)