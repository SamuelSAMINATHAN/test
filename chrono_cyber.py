import os
import time
import requests
import random
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
SITE_URL = "http://localhost:5000"
DURATION_TOTAL = 30 * 60  # 30 minutes
DURATION_NOISE_ONLY = 20 * 60  # 20 minutes de bruit pur
ATTACK_INTERVAL = 30  # Une attaque toutes les 30 secondes à la fin

def simulate_user():
    """Génère du bruit légitime sur le site"""
    endpoints = ["/", "/api/status", "/dashboard", "/login"]
    try:
        page = random.choice(endpoints)
        requests.get(f"{SITE_URL}{page}", timeout=1)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Utilisateur : visite {page}")
    except:
        pass

def run_attack():
    """Lance l'attaque de lecture mémoire (T1003.001 Linux)"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🛡️ CYBRAIN : Tentative d'attaque détectée !")
    # On utilise une commande système qui fait réagir eBPF/Tetragon
    # On essaie de dumper la mémoire du processus site_aether.py
    cmd = "pid=$(pgrep -f site_aether.py) && gcore -o /tmp/attack_dump $pid"
    subprocess.run(cmd, shell=True, capture_output=True)

# --- BOUCLE PRINCIPALE ---
start_time = time.time()
print("🚀 Début de la simulation. Va prendre ta douche, je gère.")

while (time.time() - start_time) < DURATION_TOTAL:
    elapsed = time.time() - start_time
    
    # 1. Toujours simuler des utilisateurs (pour avoir du bruit même pendant l'attaque)
    simulate_user()
    
    # 2. Si on a dépassé les 20 minutes, on commence les attaques
    if elapsed > DURATION_NOISE_ONLY:
        if int(elapsed) % ATTACK_INTERVAL == 0:
            run_attack()
            
    time.sleep(random.uniform(1, 3))

print("✅ Simulation terminée. Logs prêts pour Tetragon !")
