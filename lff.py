from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# =====================================
# DATABASE CONNECTION
# =====================================
def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


# =====================================
# INIT DATABASE
# =====================================
@app.route("/init_db")
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

    return jsonify({"message": "database initialized"})


# =====================================
# GET ALL TASKS
# =====================================
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return jsonify([dict(task) for task in tasks])


# =====================================
# ADD TASK
# =====================================
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (data.get("title"), data.get("done", False))
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "task added"}), 201


# =====================================
# DELETE TASK
# =====================================
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db_connection()

    result = conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "task not found"}), 404

    return jsonify({"message": "deleted"})


# =====================================
# UPDATE TASK
# =====================================
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()

    conn = get_db_connection()

    result = conn.execute(
        "UPDATE tasks SET done = ? WHERE id = ?",
        (data.get("done", False), id)
    )

    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "task not found"}), 404

    return jsonify({"message": "task updated"})


# =====================================
# RUN APP
# =====================================
if __name__ == "__main__":
    app.run(debug=True)