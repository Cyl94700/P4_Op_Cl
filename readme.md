![chess_club](Images/chess_club.png)

# Projet 4 DA-Python OC
***Livrable : application de gestion de tournoi d'échecs avec base de données TinyDB.***

_Testé sous Windows 11 - Python version 3.10.5


## Menu

1. [Installation du projet](#id-section1)
    a[Windows](#id-section1-1)
    b[MacOS et Linux](#id-section1-2)
   
2. [Rapport flake8](#section2)
    a[Dernier rapport flake8 généré](#id-section2-1)
    b[Générer un nouveau rapport](#id-section2.2)

3. [Fonctionnement de l'application](#id-section3)
    a[Principe général](#section3-1)
    b[Menu](#section3-2)



<div id='id-section1'></div>

## 1. Installation du projet

<div id='id-section1-1'></div>


#### a. Windows :
   Depuis votre terminal, naviguez vers le dossier racine souhaité.
####### Récupération du projet
         
   $ Tapez :  git clone https://github.com/Cyl94700/P4_Op_Cl.git

####### Accéder au dossier du projet, créer et activer l'environnement virtuel
   Tapez :
   $ cd P4_Op_Cl
   $ python -m venv env 
   $ ~env\scripts\activate
    
####### Installer les paquets requis
   Tapez :
    $ pip install -r requirements.txt

####### Lancer le programme
    $ python main.py


<div id='id-section1-2'></div>

---------

####  b. MacOS et Linux :
   Depuis votre terminal, naviguez vers le dossier souhaité.
###### Récupération du projet

    $ git clone https://github.com/Cyl94700/P4_Op_Cl.git

###### Activer l'environnement virtuel
    $ cd P4_Op_Cl
    $ python -m venv env 
    $ source env/bin/activate
    
###### Installer les paquets requis
    $ pip install -r requirements.txt

###### Lancer le programme
    $ python3 main.py


----------
<div id='id-section2'></div>


## 2. Rapport flake8

<div id='id-section2-1'></div>

#### a. Dernier rapport flake8 généré
![dernier_flake8](Images/dernier_flake8.png)

<div id='id-section2-2'></div>

#### b. Générer un nouveau rapport
Supprimez le dossier "flake8_report" contenant le dernier rapport (fichier "index.html")

Depuis votre terminal tapez :

   $ flake8 --format=html --htmldir=flake8_report

Le dossier "flake8_report" est de nouveau généré avec le rapport   ("index.html") à l'intérieur.



<div id='id-section3'></div>

## 3. Fonctionneùent de l'apllication

<div id='id-section3-1'></div>

#### a. Principe général

<div id='id-section3-2'></div>

#### b. Menu


