from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                            user_id TEXT,
                            usb_data TEXT)''')
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
        cursor.execute('SELECT user_id, GROUP_CONCAT(usb_data, ",") FROM user_data GROUP BY user_id')
        data = cursor.fetchall()

    # Transpose the data to match the desired format
    user_ids = [row[0] for row in data]
    usb_data_rows = [row[1].split(',') for row in data]

    max_length = max(len(usb_data) for usb_data in usb_data_rows)
    for usb_data in usb_data_rows:
        usb_data.extend([None] * (max_length - len(usb_data)))

    usb_data_transposed = list(zip(*usb_data_rows))

    return render_template('index.html', user_ids=user_ids, usb_data=usb_data_transposed)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
