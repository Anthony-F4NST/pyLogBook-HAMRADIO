#!/usr/bin/env python3
import csv
import os
from datetime import datetime, timezone

FICHIER_LOG = "radio_logbook.csv"
FICHIER_CONFIG = "logbook_config.txt"
COLONNES = ["Numero", "Date_UTC", "Heure_UTC", "Indicatif", "Bande", "Mode", "RST_Envoye", "RST_Recu", "Commentaires"]
LARGEUR_UTILE = 115

def gerer_configuration():
    if os.path.exists(FICHIER_CONFIG):
        with open(FICHIER_CONFIG, "r", encoding="utf-8") as f:
            return f.read().strip().upper()
    print("\n=== Configuration Initiale du Logbook ===")
    indicatif_station = input("Entrez l'indicatif de votre station (ex: F4NST) : ").strip().upper()
    if not indicatif_station:
        indicatif_station = "RADIOAMATEUR"
    with open(FICHIER_CONFIG, "w", encoding="utf-8") as f:
        f.write(indicatif_station)
    return indicatif_station


def charger_tous_qso_tries():
    if not os.path.exists(FICHIER_LOG):
        return []
    qso_list = []
    with open(FICHIER_LOG, "r", encoding="utf-8") as f:
        lecteur = csv.reader(f)
        next(lecteur)
        for row in lecteur:
            if not row:
                continue
            qso_list.append(row)
    qso_tries = sorted(qso_list, key=lambda x: (x[1], x[2]))
    return qso_tries


def sauvegarder_tout(qso_list):
    with open(FICHIER_LOG, "w", encoding="utf-8", newline="") as f:
        scripteur = csv.writer(f)
        scripteur.writerow(COLONNES)
        scripteur.writerows(qso_list)


def charger_dernier_numero():
    return len(charger_tous_qso_tries())


def initialiser_logbook():
    if not os.path.exists(FICHIER_LOG):
        with open(FICHIER_LOG, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(COLONNES)


def valider_format_date(date_texte):
    try:
        datetime.strptime(date_texte, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valider_format_heure(heure_texte):
    try:
        datetime.strptime(heure_texte, "%H:%M")
        return True
    except ValueError:
        return False


def ajouter_qso():
    print("\n--- Nouvel Enregistrement QSO ---")
    indicatif = input("Indicatif du correspondant : ").strip().upper()
    if not indicatif:
        print("Annule : L'indicatif est obligatoire.")
        return
    bande = input("Bande (ex: 2m, 70cm, 20m) [2m] : ").strip() or "2m"
    mode = input("Mode (ex: DMR, FM, SSB, CW) [DMR] : ").strip().upper() or "DMR"
    rst_s = input("RST Envoye : ").strip() or "59"
    rst_r = input("RST Recu : ").strip() or "59"
    commentaires = input("Commentaires / Prenom / Mobile : ").strip().capitalize()

    maintenant_utc = datetime.now(timezone.utc)
    date_defaut = maintenant_utc.strftime("%Y-%m-%d")
    heure_defaut = maintenant_utc.strftime("%H:%M")

    date_utc = input(f"Date UTC (AAAA-MM-JJ) [{date_defaut}] : ").strip() or date_defaut
    while not valider_format_date(date_utc):
        print("Format invalide. Veuillez utiliser le format AAAA-MM-JJ.")
        date_utc = input(f"Date UTC (AAAA-MM-JJ) [{date_defaut}] : ").strip() or date_defaut

    heure_utc = input(f"Heure UTC (HH:MM) [{heure_defaut}] : ").strip() or heure_defaut
    if len(heure_utc) == 4 and ":" in heure_utc and heure_utc.count(":") == 1:
        heure_utc = "0" + heure_utc
    while not valider_format_heure(heure_utc):
        print("Format invalide. Veuillez utiliser le format HH:MM.")
        heure_utc = input(f"Heure UTC (HH:MM) [{heure_defaut}] : ").strip() or heure_defaut

    numero_provisoire = charger_dernier_numero() + 1
    with open(FICHIER_LOG, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([numero_provisoire, date_utc, heure_utc, indicatif, bande, mode, rst_s, rst_r, commentaires])
    
    qso_tries = charger_tous_qso_tries()
    for index, row in enumerate(qso_tries):
        row[0] = str(index + 1)
    sauvegarder_tout(qso_tries)
    print(f"QSO avec {indicatif} enregistre avec succes !")

def formater_ligne_qso(row):
    num, date, heure, ind, bande, mode, rsts, rstr, comm = row
    rst_brut = f"{rsts}/{rstr}"
    
    # Étape 1 : Construction élastique de la ligne
    ligne_brute = (
        f"QSO n°{num:<3} | {date} {heure} UTC | "
        f"{ind:<8} | Bande: {bande:<5} | Mode: {mode:<6} | "
        f"RST: {rst_brut:<16} | {comm}"
    )
    
    # Étape 2 : Le Slicing magique ! On coupe à 111 caractères max s'il y a débordement, 
    # ou on ajoute des espaces si c'est trop court.
    ligne_tronquee = f"{ligne_brute[:111]:<111}"
    # Étape 3 : On ferme proprement le cadre
    return f"| {ligne_tronquee} |"

def afficher_logbook(indicatif_station):
    qso_tries = charger_tous_qso_tries()
    if not qso_tries:
        print("\nLe carnet de trafic est vide.")
        return
        
    lignes_pretes = [formater_ligne_qso(row) for row in qso_tries]
    
    # On mesure la taille exacte en caracteres de la premiere ligne (ex: 106)
    largeur_reelle = len(lignes_pretes[0])
    
    titre = f" CARNET DE TRAFIC DE LA STATION {indicatif_station} "
    print(f"\n{titre:=^{LARGEUR_UTILE}}")
    for l in lignes_pretes:
        print(l)
    print("=" * LARGEUR_UTILE)


def supprimer_qso(indicatif_station):
    if not os.path.exists(FICHIER_LOG):
        print("\nLe carnet de trafic est vide.")
        return
    afficher_logbook(indicatif_station)
    saisie = input("\nEntrez le numero du QSO a supprimer (ou Entree pour annuler) : ").strip()
    if not saisie.isdigit():
        print("Annule.")
        return
    num_a_supprimer = int(saisie)
    qso_tries = charger_tous_qso_tries()
    trouve = False
    qso_restants = []
    for row in qso_tries:
        if int(row[0]) == num_a_supprimer:
            trouve = True
            continue
        qso_restants.append(row)
    if not trouve:
        print(f"Aucun QSO ne porte le numero {num_a_supprimer}.")
        return
    for index, row in enumerate(qso_restants):
        row[0] = str(index + 1)
    sauvegarder_tout(qso_restants)
    print(f"Le QSO n°{num_a_supprimer} a ete supprime.")


def rechercher_indicatif():
    qso_tries = charger_tous_qso_tries()
    if not qso_tries:
        print("\nLe carnet de trafic est vide.")
        return
    recherche = input("\nEntrez l'indicatif a rechercher : ").strip().upper()
    if not recherche:
        print("Recherche annulee.")
        return
    compteur = 0
    
    lignes_trouvees = []
    for row in qso_tries:
        if recherche in row[3]:
            lignes_trouvees.append(formater_ligne_qso(row))
            compteur += 1
            
    if compteur > 0:
        largeur_reelle = len(lignes_trouvees[0])
        print(f"\n{' RESULTATS DE RECHERCHE POUR ' + recherche + ' ':=^{largeur_reelle}}")
        for l in lignes_trouvees:
            print(l)
        print("=" * largeur_reelle)
    else:
        print(f"Aucun QSO trouve pour la recherche '{recherche}'.")


def afficher_statistiques(indicatif_station):
    qso_tries = charger_tous_qso_tries()
    if not qso_tries:
        print("\nLe carnet de trafic est vide.")
        return
    total_qso = len(qso_tries)
    stats_bandes = {}
    stats_modes = {}
    for row in qso_tries:
        bande = row[4]
        mode = row[5]
        stats_bandes[bande] = stats_bandes.get(bande, 0) + 1
        stats_modes[mode] = stats_modes.get(mode, 0) + 1
    LARGEUR_STATS = 50
    titre = f" STATISTIQUES DE LA STATION {indicatif_station} "
    print(f"\n{titre:=^{LARGEUR_STATS}}")
    print(f" Nombre total de QSO enregistres : {total_qso}")
    print("-" * LARGEUR_STATS)
    print(" Reparpartition par Bande :")
    for b, qte in stats_bandes.items():
        print(f"  - {b:<12} : {qte} QSO")
    print("-" * LARGEUR_STATS)
    print(" Reparpartition par Mode :")
    for m, qte in stats_modes.items():
        print(f"  - {m:<12} : {qte} QSO")
    print("=" * LARGEUR_STATS)


def main():
    indicatif_station = gerer_configuration()
    initialiser_logbook()
    while True:
        print(f"\n=== Carnet de Trafic (Logbook) - {indicatif_station} ===")
        print("1. Enregistrer un QSO")
        print("2. Voir le carnet de trafic")
        print("3. Supprimer un QSO (Delete)")
        print("4. Rechercher un indicatif")
        print("5. Afficher les statistiques")
        print("6. Quitter")
        choix = input("Votre choix (1-6) : ").strip()
        if choix == "1":
            ajouter_qso()
        elif choix == "2":
            afficher_logbook(indicatif_station)
        elif choix == "3":
            supprimer_qso(indicatif_station)
        elif choix == "4":
            rechercher_indicatif()
        elif choix == "5":
            afficher_statistiques(indicatif_station)
        elif choix == "6":
            print(f"73 de Mia ! Bon trafic, {indicatif_station}.")
            break
        else:
            print("Option invalide.")


if __name__ == "__main__":
    main()
