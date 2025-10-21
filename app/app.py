from flask import Flask, jsonify, render_template
import psycopg2
import os
from kubernetes import client, config

app = Flask(__name__)

# YugabyteDB connection
DB_HOST = os.getenv("YB_HOST", "yugabyte.default.svc.cluster.local")
DB_PORT = os.getenv("YB_PORT", 5433)
DB_NAME = os.getenv("YB_DB", "yugabyte")
DB_USER = os.getenv("YB_USER", "yugabyte")
DB_PASS = os.getenv("YB_PASS", "yugabyte")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/musteri")
def musteri():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM musteri LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

# Kubernetes Nodes
config.load_kube_config()
v1 = client.CoreV1Api()

@app.route("/nodes")
def nodes():
    ret = v1.list_node()
    node_list = []
    for i in ret.items:
        node_list.append({
            "name": i.metadata.name,
            "status": i.status.conditions[-1].type,
            "cpu": i.status.capacity.get("cpu"),
            "memory": i.status.capacity.get("memory")
        })
    return render_template("nodes.html", nodes=node_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
