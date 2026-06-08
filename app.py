# ============================================
# Portfolio Backend — Flask API
# ============================================

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder="static")
CORS(app)

DATA_FILE = "data.json"

# ── Load & Save ──────────────────────────────
def load():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def auth(body):
    return body.get("password") == load()["admin_password"]

# ── Serve Frontend ────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/admin")
def admin():
    return send_from_directory("static", "admin.html")

# ── PUBLIC API ────────────────────────────────
@app.route("/api/portfolio", methods=["GET"])
def get_portfolio():
    return jsonify(load())

# ── AUTH CHECK ────────────────────────────────
@app.route("/api/auth", methods=["POST"])
def check_auth():
    body = request.get_json()
    if auth(body):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Wrong password!"}), 401

# ── UPDATE PROFILE ────────────────────────────
@app.route("/api/update/profile", methods=["POST"])
def update_profile():
    body = request.get_json()
    if not auth(body):
        return jsonify({"success": False}), 401
    data = load()
    data["profile"].update(body.get("profile", {}))
    save(data)
    return jsonify({"success": True, "message": "Profile updated!"})

# ── UPDATE SKILLS ─────────────────────────────
@app.route("/api/update/skills", methods=["POST"])
def update_skills():
    body = request.get_json()
    if not auth(body):
        return jsonify({"success": False}), 401
    data = load()
    data["skills"] = body.get("skills", data["skills"])
    save(data)
    return jsonify({"success": True, "message": "Skills updated!"})

# ── ADD PROJECT ───────────────────────────────
@app.route("/api/update/projects/add", methods=["POST"])
def add_project():
    body = request.get_json()
    if not auth(body):
        return jsonify({"success": False}), 401
    data = load()
    project = body.get("project", {})
    project["id"] = max([p["id"] for p in data["projects"]], default=0) + 1
    data["projects"].append(project)
    save(data)
    return jsonify({"success": True, "message": "Project added!", "id": project["id"]})

# ── UPDATE PROJECT ────────────────────────────
@app.route("/api/update/projects/<int:pid>", methods=["POST"])
def update_project(pid):
    body = request.get_json()
    if not auth(body):
        return jsonify({"success": False}), 401
    data = load()
    for i, p in enumerate(data["projects"]):
        if p["id"] == pid:
            data["projects"][i].update(body.get("project", {}))
            save(data)
            return jsonify({"success": True, "message": "Project updated!"})
    return jsonify({"success": False, "message": "Project not found!"}), 404

# ── DELETE PROJECT ────────────────────────────
@app.route("/api/update/projects/<int:pid>/delete", methods=["POST"])
def delete_project(pid):
    body = request.get_json()
    if not auth(body):
        return jsonify({"success": False}), 401
    data = load()
    data["projects"] = [p for p in data["projects"] if p["id"] != pid]
    save(data)
    return jsonify({"success": True, "message": "Project deleted!"})

# ── UPDATE STATS ──────────────────────────────
@app.route("/api/update/stats", methods=["POST"])
def update_stats():
    body = request.get_json()
    if not auth(body):
        return jsonify({"success": False}), 401
    data = load()
    data["stats"] = body.get("stats", data["stats"])
    save(data)
    return jsonify({"success": True, "message": "Stats updated!"})

# ── UPDATE EDUCATION ──────────────────────────
@app.route("/api/update/education", methods=["POST"])
def update_education():
    body = request.get_json()
    if not auth(body):
        return jsonify({"success": False}), 401
    data = load()
    data["education"] = body.get("education", data["education"])
    save(data)
    return jsonify({"success": True, "message": "Education updated!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)