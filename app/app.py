from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

YB_HOST = os.getenv("YUGABYTE_HOST", "yugabyte")
YB_PORT = os.getenv("YUGABYTE_PORT", 5433)
YB_DB = os.getenv("YUGABYTE_DB", "yugabyte")
YB_USER = os.getenv("YUGABYTE_USER", "yugabyte")
YB_PASSWORD = os.getenv("YUGABYTE_PASSWORD", "")

def get_connection():
    return psycopg2.connect(
        host=YB_HOST,
        port=YB_PORT,
        dbname=YB_DB,
        user=YB_USER,
        password=YB_PASSWORD
    )

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);")
        cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()
        cur.close()
        conn.close()
        message = f"Added {name}!"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
