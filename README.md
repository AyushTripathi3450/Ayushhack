# ⚡ PulseRate — Real-Time Feedback Portal

> A full-stack real-time feedback intelligence portal built for **Code Sprint 2.0** Hackathon by **Reboot Club**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=for-the-badge&logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)
![SocketIO](https://img.shields.io/badge/Socket.IO-Realtime-white?style=for-the-badge&logo=socketdotio)

---

## 🌐 Live Demo

🔗 **Deployed Website →** `your deployed link here`
🔗 **GitHub Repository →** `your github link here`

---

## 📌 About The Project

**PulseRate** is a real-time feedback intelligence portal where users submit star ratings across multiple categories and instantly see live averages update across all connected screens — powered by WebSockets with zero page refresh.

Built as part of **Round 3 (Build a Website)** of **Code Sprint 2.0** hackathon organized under **Reboot Club**.

---

## 🏅 Hackathon Journey

| Round | Challenge | Result |
|-------|-----------|--------|
| Round 1 | Problem Solving & Logic | ✅ Qualified |
| Round 2 | Technical & Teamwork Challenge | ✅ Qualified |
| Round 3 | Build a Complete Website | ✅ Delivered |

---

## ✨ Key Features

- 🔐 **Secure Authentication** — Login & Registration with SHA-256 password encryption and Flask session management
- 📡 **Real-Time WebSocket Sync** — Live ratings and averages update instantly across all connected users simultaneously
- ⭐ **Interactive Star Ratings** — 5-star rating system across 6 unique feedback categories
- 📊 **Live Analytics Dashboard** — Bar, Line, Donut and Polar Area charts powered by Chart.js updating in real time
- 🔴 **Live Feedback Feed** — Watch new feedback appear instantly as it is submitted
- 📋 **Personal History** — Track every rating you have submitted with sentiment analysis
- 💎 **Premium UI Design** — Dark luxury theme with gold accents, Cormorant Garamond serif typography
- ✅ **Fully Deployed** — Live on the internet, not just running locally

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Real-Time** | Flask-SocketIO, WebSockets |
| **Database** | SQLite |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Charts** | Chart.js 4.x |
| **Authentication** | SHA-256 Hashing, Flask Sessions |
| **Typography** | Cormorant Garamond, DM Sans |

---

## 📁 Project Structure

```
feedback_portal/
│
├── app.py                        ← Flask backend + Socket.IO + SQLite
├── requirements.txt              ← Python dependencies
├── feedback.db                   ← SQLite database (auto-created)
├── README.md                     ← You are here
│
├── templates/
│   ├── login.html                ← Login page
│   ├── register.html             ← Registration page
│   └── dashboard.html            ← Full dashboard
│
└── static/
    ├── css/                      ← Static stylesheets (optional)
    └── js/                       ← Static scripts (optional)
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.9 or above → [Download here](https://www.python.org/downloads/)
- VS Code → [Download here](https://code.visualstudio.com/)

### Installation

**Step 1 — Clone the repository**
```bash
git clone https://github.com/yourusername/feedback_portal.git
cd feedback_portal
```

**Step 2 — Create a virtual environment**
```bash
python -m venv venv
```

**Step 3 — Activate virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

**Step 4 — Install dependencies**
```bash
pip install flask flask-socketio eventlet
```

**Step 5 — Run the application**
```bash
python app.py
```

**Step 6 — Open in browser**
```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirects to login or dashboard |
| GET | `/login` | Login page |
| GET | `/register` | Registration page |
| GET | `/dashboard` | Main dashboard (auth required) |
| GET | `/logout` | Clears session and redirects |
| POST | `/api/register` | Register new user |
| POST | `/api/login` | Authenticate user |
| POST | `/api/feedback` | Submit feedback (auth required) |
| GET | `/api/stats` | Get live stats (auth required) |
| GET | `/api/my-feedback` | Get personal feedback history |

---

## 🔌 WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | Initial connection, triggers stats push |
| `stats_update` | Server → Client | Live dashboard stats broadcast |
| `new_feedback` | Server → Client | New feedback item broadcast |

---

## 📸 Pages Overview

| Page | Route | Description |
|------|-------|-------------|
| Login | `/login` | Dark luxury login with animated background |
| Register | `/register` | Two-panel registration with feature highlights |
| Dashboard | `/dashboard` | Full featured dashboard with 6 sections |

### Dashboard Sections

| Section | Features |
|---------|----------|
| 📊 Overview | KPI cards, trend chart, category bars, live feed, donut chart |
| 📈 Analytics | Bar chart, polar area, extended trend line, sentiment KPIs |
| 📡 Live Feed | Real-time table auto-populated via WebSocket |
| ✍️ Submit Feedback | Interactive 5-star rater, category selector, live score sidebar |
| 📋 My History | Personal feedback log with sentiment chips |
| ⚙️ Settings | Account info and notification preferences |

---

## 🏷️ Feedback Categories

| Category | Icon |
|----------|------|
| Product Quality | 📦 |
| Customer Support | 🎧 |
| Delivery Speed | 🚀 |
| User Experience | ✨ |
| Value for Money | 💎 |
| Overall Experience | 🌟 |

---

## 👨‍💻 Team

| Role | Name |
|------|------|
| 👑 Team Leader | Ayush Tripathi |
| 🤝 Team Member | Alok Kumar Pandey |

> Built with 💛 by **Reboot Club** at **Code Sprint 2.0**

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <b>⚡ PulseRate — Listen to what really matters.</b>
</p>
