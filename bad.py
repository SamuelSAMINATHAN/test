import os
import time
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
TARGET_SCRIPT = "aether_supervision.py" 
DUMP_PATH = "/tmp/cybrain_dump"
# Intervalle réduit au minimum pour saturer le dataset d'exemples positifs
ATTACK_INTERVAL = 1 

def run_attack():
    """Exécute l'action malicieuse de manière répétitive"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # Commande optimisée : pgrep trouve le PID, gcore dump, on supprime immédiatement
    # Note : gcore utilise l'appel système ptrace, ce qui est le signal clé pour Tetragon
    cmd = (
        f"pid=$(pgrep -f {TARGET_SCRIPT}) && "
        f"if [ -n \"$pid\" ]; then "
        f"gcore -o {DUMP_PATH} $pid > /dev/null 2>&1 && "
        f"rm -f {DUMP_PATH}.*; "
        f"else echo 'Cible non trouvée'; fi"
    )
    
    try:
        subprocess.run(cmd, shell=True)
        print(f"[{timestamp}] 🚨 Action : Memory Dump effectué sur {TARGET_SCRIPT}")
    except Exception as e:
        print(f"[!] Erreur lors de l'attaque : {e}")

# --- BOUCLE INFINIE POUR LE MVP ---
print(f"🚀 Génération intensive du dataset (Cible: {TARGET_SCRIPT})")
print("Appuyez sur Ctrl+C pour arrêter la capture.")

try:
    while True:
        run_attack()
        time.sleep(ATTACK_INTERVAL)
except KeyboardInterrupt:
    print("\n✅ Simulation interrompue. Dataset prêt pour traitement GNN.")
