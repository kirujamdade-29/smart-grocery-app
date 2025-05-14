from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from datetime import datetime
from utils.expiry_check import check_expiry  # ✅ Expiry check

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 🔐 Required for session

DATA_FILE = 'data/grocery_data.json'

# 🔐 Dummy credentials
USER_CREDENTIALS = {
    "admin": "admin123"
}

# 🔁 Load and Save functions
def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_items(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=4)

# 🏠 Home redirects to login or index
@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

# 🔐 Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in USER_CREDENTIALS and USER_CREDENTIALS[uname] == pwd:
            session['username'] = uname
            return redirect(url_for('index'))
        else:
            return "<h3>Invalid credentials. Try again.</h3>"
    return render_template('login.html')

# 🔓 Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# 📋 Show Grocery Items (Home)
@app.route('/index')
def index():
    if "username" not in session:
        return redirect(url_for('login'))

    items = load_items()
    check_expiry(items)
    return render_template('index.html', items=items)

# ➕ Add New Item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if "username" not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        expiry = request.form['expiry']
        item = {
            'name': name,
            'expiry': expiry,
            'expired': False
        }
        items = load_items()
        items.append(item)
        save_items(items)
        return redirect(url_for('index'))
    return render_template('add_item.html')

# 📃 View All Items (separate route if needed)
@app.route('/items')
def show_items():
    if "username" not in session:
        return redirect(url_for('login'))

    items = load_items()
    check_expiry(items)
    return render_template('items.html', items=items)

# ❌ Delete Item
@app.route('/delete/<int:index>', methods=['POST'])
def delete_item(index):
    if "username" not in session:
        return redirect(url_for('login'))

    items = load_items()
    if 0 <= index < len(items):
        del items[index]
        save_items(items)
    return redirect(url_for('index'))

# ▶ Run the App
if __name__ == '__main__':
    app.run(debug=True)
