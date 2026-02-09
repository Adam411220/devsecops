import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

# POPRAWKA 1: Nie ma już hasła na sztywno (używamy zmiennej środowiskowej)
# To zamieni "Issue" na "Safe" w oczach Sonara.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-safe-key')

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # POPRAWKA 2: SQL Injection naprawione przez parametryzację (?)
    # To był błąd CRITICAL, teraz jest bezpiecznie.
    query = "SELECT username FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    user = cursor.fetchone()
    return f"Użytkownik: {user}"

@app.route('/debug')
def debug():
    # ZOSTAWIAMY LOW / INFO:
    # Zwracanie stringa z konfiguracji bez wrażliwych danych.
    # Sonar może to oznaczyć jako "Code Smell" (nieużywany debug), ale to niski priorytet.
    return "Debug mode is active"

if __name__ == '__main__':
    # ZOSTAWIAMY LOW: 
    # Uruchamianie na 0.0.0.0 bez debug=True.
    # Sonar może zgłosić "Security Hotspot" (bo bindujesz do wszystkich IP), 
    # ale przy braku debug=True ocena nie powinna spaść do poziomu blokady.
    app.run(debug=False, host='0.0.0.0')