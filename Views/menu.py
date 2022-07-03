class MenuViews:

    def __init__(self):
        pass

    @staticmethod
    def application_title():
        print("\n\n----------------------------------")
        print("        TOURNOIS D'ECHECS")
        print("----------------------------------")

    @staticmethod
    def main_menu(menu_lines):
        print("\n\n=== MENU PRINCIPAL ===\n")
        i = 0
        for line in menu_lines:
            i += 1
            print("[" + str(i) + "]" + " " + line)
        print("\n[q] Quitter")

    @staticmethod
    def create_tournament_header():
        print("\n" * 3 + "--- NOUVEAU TOURNOI ---")

    @staticmethod
    def time_control_option():
        print("\nChoisissez un type de contrôle du temps :")
        print("[1] Bullet")
        print("[2] Blitz")
        print("[3] Rapid")

    @staticmethod
    def review_tournament(info, players):
        """
        Affiche les informations rentrées par l'utilisateur avant sauvegarde
        @paramètres "info" : liste des infos input du tournoi
        @paramètres "players" : liste de 8 joueurs sélectionnés
        """
        print("\n\nNouveau tournoi à créer :\n")
        print(f"{info[0].upper()}, {info[1].title()}", end=' | ')
        print(f"Description : {info[2]}", end=' | ')
        print("Rounds : 4", end=' | ')
        print(f"Contrôle du temps : {info[3]}")
        print("\nJoueurs (8 total) :\n")

        for item in players:
            print(f"Player {players.index(item) + 1} : ", end='')
            print(f"{item['id']}", end=' | ')
            print(f"{item['last_name']}, {item['first_name']}", end=' | ')
            print(f"{item['birth_date']}", end=' | ')
            print(f"rank : {item['rank']}")

        print("\nSauvegarder ? [o/n] ", end='')

    @staticmethod
    def tournament_saved():
        print("\nTournoi sauvegardé avec succès !")

    @staticmethod
    def start_tournament():
        print("\nCommencer le tournoi ? [o/n] ", end='')

    @staticmethod
    def select_players(players, player_number):
        """
        Affiche les joueurs pour selection
        @paramètres "players" : liste des joueurs non choisis
        @paramètres "player_number" : numéro du joueur à selectionner sur 8
        """
        print(f"\nChoisissez un joueur {player_number} :\n")
        for i in range(len(players)):
            print(f"[{players[i]['id']}]", end=' ')
            print(f"{players[i]['last_name']}, {players[i]['first_name']}", end=" | ")
            print(f"{players[i]['gender']} | {players[i]['birth_date']}", end=" | ")
            print(f"rang : {players[i]['rank']}")

        print("\n[r] Retour au menu principal")

    @staticmethod
    def select_tournament(tournaments):
        """
        Affiche les tournois pour selection
        @paramètres "tournaments" : liste des tournois
        """
        print("\n" * 3 + "--- CHOISIR UN TOURNOI ---\n")
        for i in range(len(tournaments)):
            print(f"[{tournaments[i]['t_id']}]", end=' ')
            print(tournaments[i]['name'], end=' | ')
            print(tournaments[i]['place'], end=" | ")
            print(tournaments[i]['description'], end=' | ')
            print(f"Date : {tournaments[i]['date']}", end=' | ')
            print(f"Round {tournaments[i]['current_round']-1}/{tournaments[i]['nb_rounds']}")

        print("\n[r] Retour au menu principal")

    @staticmethod
    def create_new_player_header():
        print("\n" * 3 + "- NOUVEAU JOUEUR -\n")

    @staticmethod
    def review_player(info):
        """
        Résume les informations du nouveau joueur saisi avant sauvegarde
        @paramètres "info": liste des informations joueur
        """
        print("\n\nNouveau Joueur :\n")
        print(f"{info[0]}, {info[1]}", end=' | ')
        print(f"Date de naissance: {info[2]}", end=' | ')
        print(f"Genre : {info[3]}", end=' | ')
        print(f"Rang : {info[4]}")
        print("\nVoulez-vous sauvegarder ? [o/n] ", end='')

    @staticmethod
    def update_player(p, options):
        """Infos joueur à modifier
        @paramètres "p" : joueur à modifier
        @paramètres "options" : option de modification
        """
        print("\n\n--- MODIDIER UN JOUEUR ---\n")
        print(f"Joueur {p.last_name}, {p.first_name}\n")
        for i in range(len(options)):
            print(f"[{i+1}] Modifier la valeur {options[i]}")

        print("\n[r] Retour au menu principal")

    @staticmethod
    def player_saved():
        print("\nJoueur sauvegardé avec succès")

    @staticmethod
    def reports_menu():
        print("\n" * 3 + "--- RAPPORTS ---\n")
        print("[1] Joueurs")
        print("[2] Joueurs d'un tournoi")
        print("[3] Tournois")
        print("[4] Rounds d'un tournoi")
        print("[5] Matches d'un tournoi")
        print("\n[r] Retour au menu principal")

    @staticmethod
    def reports_player_sorting():
        print("\n[1] Trier par nom")
        print("[2] Trier par rang")
        print("\n[r] Retour au menu principal")

    @staticmethod
    def input_text(option):
        print(f"\nEntrez {option} ou tapez [r] pour retourner au menu principal : ", end='')

    @staticmethod
    def input_option():
        print("\nChoisissez une [option] puis appuyez sur Entrée : ", end='')

    @staticmethod
    def sure_exit():
        print("\nVoulez-vous vraiment quitter l'application ? [o/n]", end='')

    @staticmethod
    def input_error():
        print("\nErreur de saisie, choisissez une option valide :", end='')

    @staticmethod
    def player_out_of_bounds():
        print("\nNuméro de joueur hors limites. Choisissez un autre joueur :")

    @staticmethod
    def other_report():
        print("\nVoir un autre rapport ? [o/n] ", end='')

    @staticmethod
    def update_rank():
        print("\nModifier les rangs ? [o/n] ", end='')

    @staticmethod
    def rank_update_header(player):
        print(f"\nModification de {player.last_name}, {player.first_name}")

    @staticmethod
    def need_text():
        print("\nSaisie obligatoire", end='')

    @staticmethod
    def date_error():
        print("\nDate incorrecte", end='')
