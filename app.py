from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import sqlite3
import hashlib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

DB_PATH = "feedback.db"

# ─────────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            company TEXT,
            role TEXT DEFAULT 'customer',
            avatar TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comment TEXT,
            sentiment TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            icon TEXT DEFAULT '⭐',
            description TEXT
        )
    """)
    # Seed default categories
    cats = [
        ("Product Quality", "📦", "Rate our product quality"),
        ("Customer Support", "🎧", "Rate your support experience"),
        ("Delivery Speed", "🚀", "Rate our delivery performance"),
        ("User Experience", "✨", "Rate the overall UX/UI"),
        ("Value for Money", "💎", "Rate the pricing & value"),
        ("Overall Experience", "🌟", "Rate your overall experience"),
    ]
    for cat in cats:
        c.execute("INSERT OR IGNORE INTO categories (name, icon, description) VALUES (?, ?, ?)", cat)
    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_stats():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as total, AVG(rating) as avg_rating FROM feedback")
    overall = c.fetchone()
    c.execute("""
        SELECT category, COUNT(*) as count, AVG(rating) as avg, MIN(rating) as min_r, MAX(rating) as max_r
        FROM feedback GROUP BY category
    """)
    by_cat = [dict(r) for r in c.fetchall()]
    c.execute("""
        SELECT strftime('%Y-%m-%d', created_at) as day, AVG(rating) as avg, COUNT(*) as cnt
        FROM feedback GROUP BY day ORDER BY day DESC LIMIT 30
    """)
    trend = [dict(r) for r in c.fetchall()]
    c.execute("""
        SELECT f.rating, f.comment, f.category, f.created_at, u.name, u.company
        FROM feedback f JOIN users u ON f.user_id = u.id
        ORDER BY f.created_at DESC LIMIT 10
    """)
    recent = [dict(r) for r in c.fetchall()]
    c.execute("SELECT COUNT(*) as total FROM users")
    user_count = c.fetchone()["total"]
    conn.close()
    return {
        "total": overall["total"] or 0,
        "avg_rating": round(overall["avg_rating"] or 0, 2),
        "by_category": by_cat,
        "trend": list(reversed(trend)),
        "recent": recent,
        "user_count": user_count
    }

def get_sentiment(rating):
    if rating >= 5: return "excellent"
    if rating >= 4: return "good"
    if rating >= 3: return "neutral"
    if rating >= 2: return "poor"
    return "terrible"

# ─────────────────────────────────────────────
# ROUTES – PAGES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login")
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register")
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM categories")
    cats = [dict(r) for r in c.fetchall()]
    conn.close()
    return render_template("dashboard.html",
        user=session.get("user"),
        categories=cats
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ─────────────────────────────────────────────
# ROUTES – API
# ─────────────────────────────────────────────

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    company = data.get("company", "").strip()
    if not all([name, email, password]):
        return jsonify({"ok": False, "error": "All fields are required"}), 400
    if len(password) < 6:
        return jsonify({"ok": False, "error": "Password must be at least 6 characters"}), 400
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (name, email, password, company) VALUES (?, ?, ?, ?)",
            (name, email, hash_password(password), company)
        )
        conn.commit()
        user_id = c.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"ok": False, "error": "Email already registered"}), 409
    conn.close()
    return jsonify({"ok": True, "message": "Registration successful"})

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    if not user:
        return jsonify({"ok": False, "error": "Invalid email or password"}), 401
    user = dict(user)
    session["user_id"] = user["id"]
    session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"],
                       "company": user["company"], "role": user["role"]}
    return jsonify({"ok": True, "user": session["user"]})

@app.route("/api/feedback", methods=["POST"])
def api_submit_feedback():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    data = request.get_json()
    category = data.get("category", "").strip()
    rating = data.get("rating")
    comment = data.get("comment", "").strip()
    if not category or not rating:
        return jsonify({"ok": False, "error": "Category and rating required"}), 400
    try:
        rating = int(rating)
        if not 1 <= rating <= 5:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"ok": False, "error": "Rating must be 1-5"}), 400
    sentiment = get_sentiment(rating)
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO feedback (user_id, category, rating, comment, sentiment) VALUES (?, ?, ?, ?, ?)",
        (session["user_id"], category, rating, comment, sentiment)
    )
    conn.commit()
    feedback_id = c.lastrowid
    conn.close()
    stats = get_stats()
    socketio.emit("stats_update", stats)
    socketio.emit("new_feedback", {
        "id": feedback_id,
        "name": session["user"]["name"],
        "company": session["user"].get("company", ""),
        "category": category,
        "rating": rating,
        "comment": comment,
        "sentiment": sentiment,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return jsonify({"ok": True, "message": "Feedback submitted!", "stats": stats})

@app.route("/api/stats")
def api_stats():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    return jsonify(get_stats())

@app.route("/api/my-feedback")
def api_my_feedback():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM feedback WHERE user_id=? ORDER BY created_at DESC", (session["user_id"],))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(rows)

# ─────────────────────────────────────────────
# WEBSOCKET EVENTS
# ─────────────────────────────────────────────

@socketio.on("connect")
def on_connect():
    emit("stats_update", get_stats())

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)