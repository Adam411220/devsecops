import sqlite3
from flask import Flask, request

app = Flask(__name__)

# 1. HARDCODED SECRET (Sonar wyłapie to jako krytyczny błąd bezpieczeństwa)
# Nigdy nie trzymaj kluczy w kodzie!
app.config['SECRET_KEY'] = 'SUPER-TAJNE-HASLO-12345'

@app.route('/user')
def get_user():
    # 2. SQL INJECTION (OWASP A03: Injection)
    # Pobieramy dane z adresu URL i wstawiamy je bezpośrednio do zapytania SQL.
    # Haker może wpisać: /user?id=1 OR 1=1
    user_id = request.args.get('id')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # BŁĄD: Zamiast użyć parametrów (?), używamy f-stringa.
    query = f"SELECT username FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    user = cursor.fetchone()
    return f"Użytkownik: {user}"

@app.route('/debug')
def debug():
    # 3. SENSITIVE DATA EXPOSURE
    # Zwracanie całej konfiguracji aplikacji (w tym haseł) do przeglądarki.
    return str(app.config)

if __name__ == '__main__':
    # 4. INSECURE DEPLOYMENT
    # Odpalanie aplikacji w trybie debug=True na produkcji to samobójstwo.
    app.run(debug=True, host='0.0.0.0')