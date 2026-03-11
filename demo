import os
import time
import sys
import random
import subprocess

def get_target_pid(process_name):
    """Trouve le PID de l'application cible."""
    try:
        pid = subprocess.check_output(["pgrep", "-f", process_name]).decode().strip().split('\n')[0]
        return int(pid)
    except subprocess.CalledProcessError:
        return None

def simulate_memory_scan(pid):
    """
    Simule un scan mémoire. 
    L'ouverture de /proc/[PID]/mem est le VRAI déclencheur 
    qui va réveiller ta sonde eBPF/Tetragon.
    """
    mem_path = f"/proc/{pid}/mem"
    try:
        # C'est CET appel système (openat sur /proc/pid/mem) que CyBrain doit détecter !
        with open(mem_path, 'rb') as mem_file:
            # On lit juste quelques octets pour générer l'appel 'read'
            mem_file.read(16) 
            return True
    except PermissionError:
        print("[-] Erreur : Droits root (sudo) requis pour lire la RAM d'un autre processus.")
        sys.exit(1)
    except Exception as e:
        return False

def print_hacker_output(pid):
    """Génère l'effet visuel pour la vidéo."""
    print(f"[*] Attachement au processus cible (PID: {pid})... OK")
    print(f"[*] Analyse des segments mémoire (Heap/Stack)...")
    
    scan_count = 0
    while True:
        # 1. On effectue la vraie action système pour les logs eBPF
        success = simulate_memory_scan(pid)
        
        # 2. On affiche le faux log de scan pour la vidéo
        addresses = [hex(random.randint(0x7f0000000000, 0x7fffffffffff)) for _ in range(3)]
        sys.stdout.write(f"\r[~] Scanning memory regions: {addresses[0]} ... ")
        sys.stdout.flush()
        
        time.sleep(0.8) # Vitesse du scan à l'écran
        scan_count += 1

        # Pour la démo : Au bout de quelques scans, on "trouve" le mot de passe
        if scan_count == 8:
            print("\n\n[+] MATCH TROUVÉ DANS LE SEGMENT HEAP !")
            print("-" * 50)
            print("[!] DUMP DES IDENTIFIANTS EN CLAIR :")
            print("    -> Utilisateur intercepté : consultant")
            print("    -> Mot de passe intercepté : maintenance2026")
            print("-" * 50)
            print("[*] En attente de la prochaine connexion...\n")
            scan_count = 0 # On réinitialise pour boucler

if __name__ == "__main__":
    print(r"""
     ___      _   _               _    
    |   \ ___| |_| |__  ___  ___ | |__ 
    | |) / -_)  _| '_ \/ _ \/ _ \| / / 
    |___/\___|\__|_.__/\___/\___/|_\_\  v2.1
    -- Advanced Memory Scraper --
    """)
    
    target_name = "aether_supervision.py"
    print(f"[*] Recherche du processus '{target_name}'...")
    
    pid = get_target_pid(target_name)
    if not pid:
        print(f"[-] Impossible de trouver le processus. Le serveur Aether est-il lancé ?")
        sys.exit(1)
        
    # Lance la boucle d'attaque (nécessite sudo pour lire la RAM)
    print_hacker_output(pid)
