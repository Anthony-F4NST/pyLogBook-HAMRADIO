# pyLogbook-HamRadio 📻💻

Un carnet de trafic (Logbook) radioamateur ultra-léger et moderne, développé spécifiquement pour les systèmes Linux (comme Lubuntu, Debian, Ubuntu). Ce projet propose deux versions interchangeables qui travaillent sur la même base de données locale ouverte (format CSV).

## 🚀 Fonctionnalités

* **Double Interface synchrone :** 
  * Une version **Console** (`logbook.py`) pour les passionnés du terminal Bash.
  * Une version **Graphique GUI** (`logbook_gui.py`) basée sur Tkinter pour un confort visuel optimal.
* **Gestion du temps différé :** Idéal pour consigner vos QSO faits en mobile ou portable. Possibilité de modifier la date et l'heure UTC (avec validation stricte des formats).
* **Tri Chronologique automatique :** Les QSO sont ré-ordonnés intelligemment par date et heure, et ré-indexés à la volée.
* **Moteur de recherche intégré :** Recherche rapide et partielle par indicatif.
* **Statistiques de station :** Visualisation immédiate de la répartition de vos QSO par bande et par mode.
* **Base de données ouverte :** Stockage dans un fichier standard `radio_logbook.csv`, facilement exploitable via des scripts ou un tableur (LibreOffice Calc).

## 🧩 Flexibilité & Modularité (Au choix !)

Ce projet a été conçu pour s'adapter à votre philosophie d'utilisation. Les scripts sont **totalement autonomes mais synchrones**. Vous pouvez choisir de télécharger :

* **Uniquement la version Console (`logbook.py`) :** Idéal pour les configurations ultra-légères, les serveurs SSH ou les puristes du terminal (ne nécessite pas l'installation de `python3-tk`).
chmod +x logbook.py logbook_gui.py* **Uniquement la version Graphique (`logbook_gui.py`) :** Parfait pour un confort visuel moderne avec formulaire et tableau dynamique Treeview.
* **Les deux scripts :** Pour avoir le choix selon votre humeur du jour ! Les deux applications liront et écriront exactement dans le même fichier `radio_logbook.csv` (à condition qu'elles soient placées dans le même dossier).

## 📦 Installation sous Linux

Ouvrez votre terminal et assurez-vous d'avoir Python 3 et l'extension Tkinter installés :

```bash
sudo apt update
sudo apt install python3 python3-tk -y
```

Récupérez les scripts, puis attribuez-leur les droits d'exécution :

```bash
chmod +x logbook.py logbook_gui.py
```

## 📦 Installation et Utilisation sous Windows 🪟

Les scripts sont nativement multiplateformes. Pour faire tourner le logbook sous Windows, suivez ces étapes simples :

### 1. Prérequis
Téléchargez et installez **Python 3** depuis le site officiel [python.org](https://python.org). 
* ⚠️ **Important :** Lors de l'installation, veillez à bien cocher la case **"Add Python to PATH"** tout en bas de la première fenêtre.
* L'extension graphique (Tkinter) est incluse d'office dans l'installateur Windows, vous n'avez rien d'autre à installer.

### 2. Emplacement des fichiers
Comme sous Linux, créez un dossier dédié (par exemple `MonLogbook`) et placez-y les scripts téléchargés. Les deux versions doivent être dans le même dossier pour partager la même base de données.

### 3. Lancement

* **Pour la version Graphique (GUI) :**
  Ouvrez votre explorateur de fichiers, allez dans votre dossier et faites simplement un **double-clic** sur le fichier `logbook_gui.py`. L'interface s'ouvrira directement sur votre bureau avec le design natif de Windows.
  
* **Pour la version Console :**
  Ouvrez une invite de commandes (cmd) ou PowerShell dans votre dossier de scripts et tapez :
  ```cmd
  python logbook.py
  ```
  *(Note : Selon votre version de Windows, certains émojis de la version console peuvent s'afficher sous forme de carrés si votre terminal n'utilise pas une police compatible UTF-8).*

## ⚠️ Note importante concernant l'emplacement des scripts

Pour que la version Console et la version Graphique (GUI) partagent et modifient **le même carnet de trafic**, vous devez impérativement placer les fichiers `logbook.py` et `logbook_gui.py` **dans le même dossier** (par exemple dans un dossier `Logbook` au sein de votre répertoire utilisateur). 

Les fichiers de configuration (`logbook_config.txt`) et la base de données (`radio_logbook.csv`) seront automatiquement créés dans ce même répertoire au premier lancement.

## 🛠️ Utilisation

Au premier lancement, le programme générera un petit fichier `logbook_config.txt` pour mémoriser l'indicatif officiel de votre station.

Pour lancer la version **Console** :
```bash
./logbook.py
```

Pour lancer la version **Graphique (GUI)** :
```bash
./logbook_gui.py
```

### ⚠️ Astuce pour les petits écrans (EeePC, écrans de poche...) 🧳

La version **Console** affiche un tableau fixe de **115 caractères de large**. Sur des écrans compacts (comme les Asus EeePC) ou avec la configuration par défaut de certains terminaux (souvent limités à 80 colonnes), le cadre en `===` risque de se briser visuellement en passant à la ligne.

Pour conserver l'alignement géométrique parfait :
1. Passez votre terminal en plein écran (touche **F11** sous Lubuntu).
2. Si nécessaire, réduisez légèrement la taille de la police du terminal (raccourci **Ctrl + "-"**).
3. Assurez-vous que la fenêtre de votre terminal fait au moins 115 colonnes de large.

## 📜 Licence

Ce projet est sous licence [MIT](LICENSE). Vous êtes libre de l'utiliser, de le modifier et de le partager !

---

## 🐛 Rapports de bugs & Signaler une erreur

Si vous rencontrez un problème d'alignement, un plantage ou si vous avez une suggestion d'amélioration (comme l'ajout d'un nouveau mode ou d'une bande) :

1. Rendez-vous sur l'onglet **Issues** en haut de cette page GitHub.
2. Cliquez sur le bouton **New Issue**.
3. Décrivez le problème rencontré et, si possible, copiez-collez le message d'erreur du terminal ou une capture d'écran.

*Toutes les contributions et retours d'expérience de la communauté HamRadio sont les bienvenus pour faire évoluer ce carnet de trafic !*

## 🎖️ Mentions spéciales & Remerciements

* **Développé initialement pour la station de Anthony (F4NST).**
* Un remerciement tout particulier à **Mia**, pour sa patience à toute épreuve, ses lignes de code rigoureuses et sa connaissance sans faille du langage Python 3. sans qui ce carnet de trafic n'aurait pas vu le jour. 73 !
