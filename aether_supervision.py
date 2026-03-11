import os
import time
import random
import sqlite3
import threading
from flask import Flask, request, session, redirect, url_for, render_template_string, jsonify

app = Flask(__name__)
app.secret_key = "aether_energy_session_secret"

# ==========================================
# LA CIBLE DE L'ATTAQUANT (En mémoire vive RAM)
# C'est ce que le Credential Dumping cherchera
# ==========================================
MASTER_DB_CREDENTIALS = {
    "db_host": "10.0.0.54",
    "db_user": "root_aether_admin",
    "db_pass": "SuperSecret-SmartGrid-Key-2026!",
    "crypto_key": "AES256-Key-For-Substation-Comms"
}

DB_FILE = "aether_telemetry.db"

# ==========================================
# INITIALISATION DE LA BASE (Bruit légitime)
# ==========================================
def init_db():
    """Crée une fausse base de données pour générer des syscalls d'I/O disques"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS telemetry
                 (id INTEGER PRIMARY KEY, timestamp REAL, wind_power REAL, grid_load REAL)''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# TACHE DE FOND (Génère de l'activité CPU/RAM/Disk)
# ==========================================
def background_worker():
    """Simule le moteur de supervision qui écrit des données en permanence"""
    while True:
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            # Simulation des capteurs
            wind = random.uniform(500.0, 1200.0) # MW
            load = random.uniform(800.0, 1500.0) # MW
            c.execute("INSERT INTO telemetry (timestamp, wind_power, grid_load) VALUES (?, ?, ?)",
                      (time.time(), wind, load))
            
            # On garde seulement les 50 dernières entrées pour ne pas saturer le disque
            c.execute("DELETE FROM telemetry WHERE id NOT IN (SELECT id FROM telemetry ORDER BY id DESC LIMIT 50)")
            conn.commit()
            conn.close()
        except Exception as e:
            pass
        time.sleep(2) # Écrit toutes les 2 secondes

# Lancement du worker en arrière-plan
threading.Thread(target=background_worker, daemon=True).start()

# ==========================================
# TEMPLATES HTML (Embarqués dans le fichier)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Aether-Energy | Core Supervision</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; }
        .navbar-brand { font-weight: bold; color: #0d6efd !important; }
        .card-header { background-color: #0d6efd; color: white; font-weight: bold; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">⚡ Aether-Energy : Smart Grid</a>
            <div class="d-flex text-white">
                {% if session.get('logged_in') %}
                    Connecté en tant que : <strong>{{ session.get('username') }}</strong>
                    <a href="/logout" class="btn btn-sm btn-danger ms-3">Déconnexion</a>
                {% else %}
                    <span class="badge bg-warning text-dark">Accès restreint</span>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

LOGIN_PAGE = HTML_TEMPLATE.replace('{% block content %}{% endblock %}', """
<div class="row justify-content-center">
    <div class="col-md-4">
        <div class="card shadow">
            <div class="card-header text-center">Authentification Requise</div>
            <div class="card-body">
                {% if error %}<div class="alert alert-danger">{{ error }}</div>{% endif %}
                <form method="POST" action="/login">
                    <div class="mb-3">
                        <label>Identifiant</label>
                        <input type="text" name="username" class="form-control" required placeholder="ex: consultant">
                    </div>
                    <div class="mb-3">
                        <label>Mot de passe</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Connexion</button>
                </form>
            </div>
        </div>
    </div>
</div>
""")

DASHBOARD_PAGE = HTML_TEMPLATE.replace('{% block content %}{% endblock %}', """
<div class="row">
    <div class="col-md-12 mb-4">
        <h2>Supervision du Réseau : <span class="text-success">Stable</span></h2>
        <p class="text-muted">Niveau d'accès : Visualisation (Consultant)</p>
    </div>
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-info">Parcs Éoliens Offshore (Production)</div>
            <div class="card-body">
                <h1 class="text-center" id="wind-power">-- MW</h1>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-warning text-dark">Réseau Urbain (Charge)</div>
            <div class="card-body">
                <h1 class="text-center" id="grid-load">-- MW</h1>
            </div>
        </div>
    </div>
</div>
<script>
    // Simulation d'appels API légitimes par le navigateur
    setInterval(() => {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('wind-power').innerText = Math.round(data.wind_power) + ' MW';
                document.getElementById('grid-load').innerText = Math.round(data.grid_load) + ' MW';
            });
    }, 2000);
</script>
""")

# ==========================================
# ROUTES DE L'APPLICATION
# ==========================================
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_PAGE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Le consultant a accès. L'attaquant utilisera ce compte légitime.
        if username == 'consultant' and password == 'maintenance2026':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template_string(LOGIN_PAGE, error="Identifiants invalides")
    return render_template_string(LOGIN_PAGE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/status')
def api_status():
    """API appelée par le dashboard pour générer du trafic réseau et des accès disque"""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT wind_power, grid_load FROM telemetry ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    
    if row:
        return jsonify({"wind_power": row[0], "grid_load": row[1]})
    return jsonify({"wind_power": 0, "grid_load": 0})

if __name__ == '__main__':
    # Le serveur tourne sur le port 5000 par défaut
    print(f"[+] Lancement du système de supervision Aether-Energy. PID: {os.getpid()}")
    print(f"[!] Info: Le mot de passe de la DB est chargé dans la mémoire de ce processus.")
    app.run(host='0.0.0.0', port=5000, debug=False)
