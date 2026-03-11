import os
import time
import requests
import random
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
SITE_URL = "http://localhost:5000"
TARGET_SCRIPT = "aether_supervision.py" # Nom corrigé
DURATION_TOTAL = 30 * 60  # 30 minutes
DURATION_NOISE_ONLY = 20 * 60  # 20 minutes de bruit pur
ATTACK_INTERVAL = 30  # Une attaque toutes les 30 secondes
DUMP_PATH = "/tmp/cybrain_dump"

# --- INITIALISATION DE LA SESSION ---
session = requests.Session()

def init_user_session():
    """Connecte l'utilisateur pour générer du vrai trafic interne"""
    try:
        # On simule un GET sur la page de login d'abord
        session.get(f"{SITE_URL}/login")
        # On poste les identifiants
        resp = session.post(f"{SITE_URL}/login", data={"username": "consultant", "password": "maintenance2026"})
        if resp.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Session Consultant initialisée avec succès.")
    except Exception as e:
        print(f"[!] Erreur de connexion au serveur: {e}")

def simulate_user():
    """Génère du bruit légitime et profond sur le site"""
    endpoints = ["/", "/api/status", "/api/status", "/api/status"] # On favorise l'API qui lit la DB
    try:
        page = random.choice(endpoints)
        session.get(f"{SITE_URL}{page}", timeout=2)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 👷 Utilisateur : visite {page}")
    except:
        pass

def run_attack():
    """Lance l'attaque de lecture mémoire avec gcore et nettoie derrière"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 CYBRAIN : Tentative de Credential Dumping (ptrace) !")
    
    # On trouve le PID, on dump la mémoire, puis on supprime le fichier pour ne pas saturer le disque
    cmd = f"pid=$(pgrep -f {TARGET_SCRIPT}) && " \
          f"if [ -n \"$pid\" ]; then " \
          f"gcore -o {DUMP_PATH} $pid > /dev/null 2>&1 && " \
          f"rm -f {DUMP_PATH}.$pid; " \
          f"else echo 'Processus non trouvé'; fi"
          
    subprocess.run(cmd, shell=True)

# --- BOUCLE PRINCIPALE ---
print("🚀 Début de la simulation. Va prendre ta douche, je gère le dataset.")
init_user_session()

start_time = time.time()
last_attack_time = 0

while (time.time() - start_time) < DURATION_TOTAL:
    current_time = time.time()
    elapsed = current_time - start_time
    
    # 1. Bruit de fond (requêtes web + I/O SQLite)
    simulate_user()
    
    # 2. Injection de l'attaque de manière fiable
    if elapsed > DURATION_NOISE_ONLY:
        if (current_time - last_attack_time) >= ATTACK_INTERVAL:
            run_attack()
            last_attack_time = current_time
            
    # Pause aléatoire pour imiter un humain/script asynchrone
    time.sleep(random.uniform(0.5, 2.5))

print("✅ Simulation terminée. Logs Tetragon prêts pour l'entraînement !")
