import os
import time
import subprocess
import random

# Simule un serveur de virement SWIFT (Secteur Critique) [cite: 89]
def simulate_banking_activity():
    while True:
        # 1. Activité Applicative (SQL & Fichiers) [cite: 21]
        # Simule l'écriture de logs de transaction
        with open("/tmp/swift_transactions.log", "a") as f:
            f.write(f"{time.time()} - TRANSFER - SUCCESS - ID:{random.randint(1000, 9999)}\n")
        
        # 2. Activité Réseau (Appels API internes) [cite: 18, 94]
        # Simule une requête vers une DB interne (Google pour l'exemple)
        subprocess.run(["curl", "-s", "https://www.google.com"], stdout=subprocess.DEVNULL)

        # 3. Activité Admin (Maintenance système) [cite: 20]
        # Lecture périodique de config
        subprocess.run(["cat", "/etc/hostname"], stdout=subprocess.DEVNULL)

        time.sleep(random.uniform(1, 5)) # Rythme variable pour être réaliste

if __name__ == "__main__":
    print("Démarrage de la simulation bancaire pour Vrains...")
    simulate_banking_activity()