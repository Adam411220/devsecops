import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

# --- NAPRAWA BLOCKERA ---
# Sonar nie widzi już hasła wpisanego "na sztywno". 
# Pobieramy je ze zmiennej środowiskowej systemu.
app.config['KEY'] = os.getenv('MY_APP', 'dev-key-placeholder')

# NAPRAWA: Dodajemy metody HTTP tutaj
@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT username FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    return f"Użytkownik: {user}"

# NAPRAWA: I tutaj też
@app.route('/debug', methods=['GET'])
def debug():
    return "App is running"

if __name__ == '__main__':
    app.run()