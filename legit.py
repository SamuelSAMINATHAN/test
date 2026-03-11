import time
import requests
import random
from datetime import datetime

# --- CONFIGURATION ---
SITE_URL = "http://localhost:5000"
DURATION_TOTAL = 30 * 60  # 30 minutes de trafic pur
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

# --- INITIALISATION DE LA SESSION ---
session = requests.Session()

def simulate_login():
    """Simule une connexion utilisateur légitime"""
    try:
        # On définit un User-Agent aléatoire pour le réalisme
        session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
        
        # Passage sur la page de login
        session.get(f"{SITE_URL}/login", timeout=5)
        
        # Authentification
        payload = {"username": "consultant", "password": "maintenance2026"}
        resp = session.post(f"{SITE_URL}/login", data=payload, timeout=5)
        
        if resp.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Connexion réussie.")
            return True
    except Exception as e:
        print(f"[!] Erreur serveur (est-il lancé ?) : {e}")
    return False

def simulate_activity():
    """Simule la navigation sur le dashboard et les appels API"""
    try:
        # 1. On consulte le dashboard
        session.get(f"{SITE_URL}/", timeout=2)
        
        # 2. On simule plusieurs appels API successifs (comme le JS du site le ferait)
        for _ in range(random.randint(3, 8)):
            resp = session.get(f"{SITE_URL}/api/status", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Télémétrie reçue : {data['wind_power']:.2f} MW")
            time.sleep(random.uniform(1.5, 3.0)) # Intervalle régulier
            
    except Exception as e:
        print(f"[!] Erreur durant l'activité : {e}")

def simulate_logout():
    """Déconnexion propre"""
    try:
        session.get(f"{SITE_URL}/logout", timeout=2)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚪 Déconnexion de l'utilisateur.")
    except:
        pass

# --- BOUCLE PRINCIPALE (TRAFIC SAIN UNIQUEMENT) ---
print("🚀 Lancement du générateur de trafic légitime (Baseline)...")
start_time = time.time()

while (time.time() - start_time) < DURATION_TOTAL:
    # Simule un cycle de travail complet
    if simulate_login():
        # L'utilisateur reste connecté un certain temps
        session_duration = random.randint(60, 180) # Reste entre 1 et 3 min
        session_start = time.time()
        
        while (time.time() - session_start) < session_duration:
            simulate_activity()
            
        simulate_logout()
    
    # Pause entre deux sessions utilisateur
    wait_time = random.randint(10, 30)
    print(f"--- Attente de {wait_time}s avant la prochaine session ---")
    time.sleep(wait_time)

print("✅ Simulation terminée. Dataset 'Normal' généré.")
