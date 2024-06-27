from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT NOT NULL,
                            usb_data TEXT NOT NULL)''')
        conn.commit()

# Initialize the database
init_db()

# API endpoint to receive data
@app.route('/api/data', methods=['POST'])
def receive_data():
    user_id = request.json.get('user_id')
    usb_data = request.json.get('usb_data')

    if not user_id or not usb_data:
        return jsonify({"error": "Invalid input"}), 400

    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_data (user_id, usb_data) VALUES (?, ?)', (user_id, usb_data))
        conn.commit()

    return jsonify({"message": "Data received successfully"}), 201

# Webpage to display data
@app.route('/')
def index():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, usb_data FROM user_data')
        data = cursor.fetchall()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
