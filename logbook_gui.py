#!/usr/bin/env python3
import csv
import os
from datetime import datetime, timezone
import tkinter as tk
from tkinter import messagebox, ttk

FICHIER_LOG = "radio_logbook.csv"
FICHIER_CONFIG = "logbook_config.txt"
COLONNES = [
    "Numero", "Date_UTC", "Heure_UTC", "Indicatif",
    "Bande", "Mode", "RST_Envoye", "RST_Recu",
    "Commentaires"
]

def gerer_configuration_gui():
    if os.path.exists(FICHIER_CONFIG):
        with open(FICHIER_CONFIG, "r", encoding="utf-8") as f:
            return f.read().strip().upper()
    return ""

def charger_tous_qso_tries():
    if not os.path.exists(FICHIER_LOG):
        return []
    qso_list = []
    with open(FICHIER_LOG, "r", encoding="utf-8") as f:
        lecteur = csv.reader(f)
        next(lecteur)
        for ligne in lecteur:
            if not ligne:
                continue
            qso_list.append(ligne)
    qso_tries = sorted(qso_list, key=lambda x: (x[1], x[2]))
    for index, ligne in enumerate(qso_tries):
        ligne[0] = str(index + 1)
    return qso_tries

def sauvegarder_tout(qso_list):
    with open(FICHIER_LOG, "w", encoding="utf-8", newline="") as f:
        scripteur = csv.writer(f)
        scripteur.writerow(COLONNES)
        scripteur.writerows(qso_list)

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

class LogbookApp:
    def __init__(self, root):
        self.root = root
        self.indicatif_station = gerer_configuration_gui()
        titre_init = (
            f"Logbook - Station "
            f"{self.indicatif_station if self.indicatif_station else 'Config'}"
        )
        self.root.title(titre_init)
        self.root.geometry("950x550")
        maintenant = datetime.now(timezone.utc)
        self.date_initiale = maintenant.strftime("%Y-%m-%d")
        self.heure_initiale = maintenant.strftime("%H:%M")
        if not self.indicatif_station:
            self.fenetre_configuration()
            return
        self.creer_interface()

    def fenetre_configuration(self):
        self.cadre_config = ttk.LabelFrame(
            self.root, text=" Configuration ", padding=20
        )
        self.cadre_config.pack(expand=True, padx=20, pady=20)
        ttk.Label(
            self.cadre_config,
            text="Entrez l'indicatif (ex: F4NST) :"
        ).pack(pady=5)
        self.entry_config_ind = ttk.Entry(self.cadre_config, width=15)
        self.entry_config_ind.pack(pady=5)
        ttk.Button(
            self.cadre_config, text="Enregistrer",
            command=self.valider_config
        ).pack(pady=10)

    def valider_config(self):
        ind = self.entry_config_ind.get().strip().upper()
        if not ind:
            messagebox.showerror("Erreur", "Indicatif requis.")
            return
        with open(FICHIER_CONFIG, "w", encoding="utf-8") as f:
            f.write(ind)
        self.indicatif_station = ind
        self.cadre_config.pack_forget()
        self.root.title(f"Logbook - Station {self.indicatif_station}")
        self.creer_interface()

    def creer_interface(self):
        titre_cadre = f" Enregistrer un QSO - {self.indicatif_station} "
        cadre_form = ttk.LabelFrame(
            self.root, text=titre_cadre, padding=10
        ) 
        cadre_form.pack(fill="x", padx=10, pady=5)
        self.var_date = tk.StringVar(value=self.date_initiale)
        self.var_heure = tk.StringVar(value=self.heure_initiale)
        self.var_indicatif = tk.StringVar()
        self.var_bande = tk.StringVar(value="2m")
        self.var_mode = tk.StringVar(value="DMR")
        self.var_rsts = tk.StringVar(value="59")
        self.var_rstr = tk.StringVar(value="59")
        self.var_commentaires = tk.StringVar()
        self.var_recherche = tk.StringVar()
        
        ttk.Label(cadre_form, text="Date :").grid(
            row=0, column=0, padx=5, pady=2, sticky="e"
        )
        ttk.Entry(
            cadre_form, textvariable=self.var_date, width=12
        ).grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(cadre_form, text="Heure :").grid(
            row=0, column=2, padx=5, pady=2, sticky="e"
        )
        ttk.Entry(
            cadre_form, textvariable=self.var_heure, width=8
        ).grid(row=0, column=3, padx=5, pady=2)
        ttk.Label(cadre_form, text="Indicatif :").grid(
            row=0, column=4, padx=5, pady=2, sticky="e"
        )
        ttk.Entry(
            cadre_form, textvariable=self.var_indicatif, width=12
        ).grid(row=0, column=5, padx=5, pady=2)
        ttk.Label(cadre_form, text="Bande :").grid(
            row=0, column=6, padx=5, pady=2, sticky="e"
        )
        ttk.Entry(
            cadre_form, textvariable=self.var_bande, width=8
        ).grid(row=0, column=7, padx=5, pady=2)
        ttk.Label(cadre_form, text="Mode :").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        ttk.Entry(
            cadre_form, textvariable=self.var_mode, width=12
        ).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(cadre_form, text="RST S/R :").grid(
            row=1, column=2, padx=5, pady=5, sticky="e"
        )
        cadre_rst = ttk.Frame(cadre_form)
        cadre_rst.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(
            cadre_rst, textvariable=self.var_rsts, width=3
        ).pack(side="left")
        ttk.Label(cadre_rst, text="/").pack(side="left")
        ttk.Entry(
            cadre_rst, textvariable=self.var_rstr, width=3
        ).pack(side="left")
        ttk.Label(cadre_form, text="Infos :").grid(
            row=1, column=4, padx=5, pady=5, sticky="e"
        )
        ttk.Entry(
            cadre_form, textvariable=self.var_commentaires, width=35
        ).grid(
            row=1, column=5, columnspan=3, padx=5, pady=5, sticky="we"
        )
        cadre_boutons_form = ttk.Frame(cadre_form)
        cadre_boutons_form.grid(
            row=2, column=0, columnspan=8, pady=5, sticky="we"
        )
        ttk.Button(
            cadre_boutons_form, text="Actualiser Heure",
            command=self.actualiser_horloge
        ).pack(side="left", padx=5)
        ttk.Button(
            cadre_boutons_form, text="Enregistrer QSO",
            command=self.ajouter_qso_gui
        ).pack(side="right", padx=5)

        cadre_rech = ttk.LabelFrame(
            self.root, text=" Rechercher un indicatif ", padding=5
        )
        cadre_rech.pack(fill="x", padx=10, pady=2)
        ttk.Label(cadre_rech, text="Indicatif :").pack(side="left", padx=5)
        ttk.Entry(
            cadre_rech, textvariable=self.var_recherche, width=15
        ).pack(side="left", padx=5)
        ttk.Button(
            cadre_rech, text="Filtrer", command=self.rechercher_qso_gui
        ).pack(side="left", padx=5)
        ttk.Button(
            cadre_rech, text="Tous les QSO", command=self.effacer_filtre_gui
        ).pack(side="left", padx=5)

        cadre_table = ttk.Frame(self.root, padding=10)
        cadre_table.pack(fill="both", expand=True)
        self.tableau = ttk.Treeview(
            cadre_table, columns=COLONNES, show="headings"
        )
        tailles = {
            "Numero": 50, "Date_UTC": 100, "Heure_UTC": 80,
            "Indicatif": 100, "Bande": 80, "Mode": 80,
            "RST_Envoye": 60, "RST_Recu": 60, "Commentaires": 250
        }
        for col in COLONNES:
            self.tableau.heading(col, text=col.replace("_", " "))
            self.tableau.column(
                col, width=tailles[col],
                anchor="center" if col != "Commentaires" else "w"
            )
        defilement = ttk.Scrollbar(
            cadre_table, orient="vertical", command=self.tableau.yview
        )
        self.tableau.configure(yscrollcommand=defilement.set)
        self.tableau.pack(side="left", fill="both", expand=True)
        defilement.pack(side="right", fill="y")
        
        cadre_actions = ttk.Frame(self.root, padding=10)
        cadre_actions.pack(fill="x")
        ttk.Button(
            cadre_actions, text="Supprimer QSO",
            command=self.supprimer_qso_gui
        ).pack(side="left", padx=5)
        ttk.Button(
            cadre_actions, text="Statistiques",
            command=self.afficher_stats_gui
        ).pack(side="left", padx=5)
        ttk.Button(
            cadre_actions, text="Quitter", command=self.root.quit
        ).pack(side="right", padx=5)
        self.rafraichir_tableau()

    def actualiser_horloge(self):
        maintenant = datetime.now(timezone.utc)
        self.var_date.set(maintenant.strftime("%Y-%m-%d"))
        self.var_heure.set(maintenant.strftime("%H:%M"))

    def rafraichir_tableau(self):
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        for qso in charger_tous_qso_tries():
            self.tableau.insert("", "end", values=qso)

    def ajouter_qso_gui(self):
        indicatif = self.var_indicatif.get().strip().upper()
        if not indicatif:
            messagebox.showerror("Erreur", "Indicatif obligatoire !")
            return
        date_utc = self.var_date.get().strip()
        heure_utc = self.var_heure.get().strip()
        if not valider_format_date(date_utc):
            messagebox.showerror("Erreur", "Format date incorrect.")
            return
        if (len(heure_utc) == 4 and ":" in heure_utc and 
                heure_utc.count(":") == 1):
            heure_utc = "0" + heure_utc
            self.var_heure.set(heure_utc)
        if not valider_format_heure(heure_utc):
            messagebox.showerror("Erreur", "Format heure incorrect.")
            return
        bande = self.var_bande.get().strip() or "2m"
        mode = self.var_mode.get().strip().upper() or "DMR"
        rsts = self.var_rsts.get().strip() or "59"
        rstr = self.var_rstr.get().strip() or "59"
        comm = self.var_commentaires.get().strip().capitalize()
        if not os.path.exists(FICHIER_LOG):
            with open(FICHIER_LOG, "w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow(COLONNES)
        with open(FICHIER_LOG, "a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(
                ["0", date_utc, heure_utc, indicatif,
                 bande, mode, rsts, rstr, comm]
            )
        sauvegarder_tout(charger_tous_qso_tries())
        self.var_recherche.set("")
        self.rafraichir_tableau()
        self.var_indicatif.set("")
        self.var_commentaires.set("")
        self.actualiser_horloge()
        
    def supprimer_qso_gui(self):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un QSO.")
            return
        item_selectionne = selection[0]
        valeurs = self.tableau.item(item_selectionne, "values")
        if not valeurs:
            return
        num_del = valeurs[0]
        msg = f"Supprimer le QSO n°{num_del} ?"
        if messagebox.askyesno("Confirmation", msg):
            qso_tries = charger_tous_qso_tries()
            qso_restants = [l for l in qso_tries if l[0] != str(num_del)]
            sauvegarder_tout(qso_restants)
            self.var_recherche.set("")
            self.rafraichir_tableau()

    def rechercher_qso_gui(self):
        term = self.var_recherche.get().strip().upper()
        if not term:
            self.rafraichir_tableau()
            return
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        compteur = 0
        for qso in charger_tous_qso_tries():
            if term in qso[3]:
                self.tableau.insert("", "end", values=qso)
                compteur += 1
        if compteur == 0:
            messagebox.showinfo("Recherche", f"Aucun QSO pour {term}.")
            self.rafraichir_tableau()

    def effacer_filtre_gui(self):
        self.var_recherche.set("")
        self.rafraichir_tableau()

    def afficher_stats_gui(self):
        qso_tries = charger_tous_qso_tries()
        if not qso_tries:
            messagebox.showinfo("Stats", "Carnet vide.")
            return
        total = len(qso_tries)
        bandes = {}
        modes = {}
        for l in qso_tries:
            b_cle = l[4]  # Correction Python 3.14 strict : index de colonne Bande
            m_cle = l[5]  # Correction Python 3.14 strict : index de colonne Mode
            bandes[b_cle] = bandes.get(b_cle, 0) + 1
            modes[m_cle] = modes.get(m_cle, 0) + 1
        texte_stats = f"Total QSO : {total}\n\n--- PAR BANDE ---\n"
        for b, q in bandes.items():
            texte_stats += f"• {b} : {q} QSO\n"
        texte_stats += "\n--- PAR MODE ---\n"
        for m, q in modes.items():
            texte_stats += f"• {m} : {q} QSO\n"
        titre_box = f"Statistiques Station {self.indicatif_station}"
        messagebox.showinfo(titre_box, texte_stats)

if __name__ == "__main__":
    if not os.path.exists(FICHIER_LOG):
        with open(FICHIER_LOG, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(COLONNES)
    fenetre = tk.Tk()
    app = LogbookApp(fenetre)
    fenetre.mainloop()
