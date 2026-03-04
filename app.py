from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="myappdb",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)

def init_db():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """)
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
        return redirect("/")

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users ORDER BY id DESC")
        users = cur.fetchall()

    return render_template("index.html", users=users)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
    