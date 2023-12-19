import random
import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Configuration de la fenêtre
largeur, hauteur = 1000, 800  # Modification de la taille de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Pendu")

# Police d'écriture
font = pygame.font.Font(None, 36)

def afficher_menu():
    fenetre.fill(BLANC)
    titre = font.render("Menu du pendu", True, NOIR)
    fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 50))

    options = ["Commencer une nouvelle partie", "Insérer un nouveau mot", "Quitter le programme"]
    y = 150
    regions_rectangulaires = {}  # Dictionnaire pour stocker les régions rectangulaires associées à chaque option
    for option in options:
        texte = font.render(option, True, NOIR)
        largeur_texte, hauteur_texte = texte.get_size()

        # Dessine la boîte autour de l'option
        region_rectangulaire = pygame.Rect((largeur // 2 - 250, y, 500, 50))
        pygame.draw.rect(fenetre, (192, 192, 192), region_rectangulaire, 2)

        # Centrer le texte à l'intérieur de la boîte
        fenetre.blit(texte, (largeur // 2 - largeur_texte // 2, y + (50 - hauteur_texte) // 2))

        regions_rectangulaires[option] = region_rectangulaire
        y += 50 + 20  # Ajoute un espacement entre les options

    pygame.display.flip()

    return regions_rectangulaires

def choisir_mot_aleatoire(difficulte):
    with open("mots.txt", "r", encoding="utf-8") as fichier:
        mots = [mot.strip().lower() for mot in fichier.readlines() if difficulte[0] <= len(mot.strip()) <= difficulte[1]]
        
    mot_choisi = random.choice(mots)
    return mot_choisi

def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])
    return mot_cache

def choisir_difficulte():
    fenetre.fill(BLANC)
    titre = font.render("Choisissez la difficulté", True, NOIR)
    fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 50))

    options_difficulte = ["Facile", "Moyen", "Difficile"]
    y = 150
    regions_difficulte = {}

    difficultes = {"Facile": (1, 4), "Moyen": (5, 6), "Difficile": (7, 27)}

    for option_difficulte in options_difficulte:
        texte_difficulte = font.render(option_difficulte, True, NOIR)
        largeur_texte_difficulte, hauteur_texte_difficulte = texte_difficulte.get_size()

        region_rectangulaire_difficulte = pygame.Rect((largeur // 2 - 250, y, 500, 50))
        pygame.draw.rect(fenetre, (192, 192, 192), region_rectangulaire_difficulte, 2)

        fenetre.blit(texte_difficulte, (largeur // 2 - largeur_texte_difficulte // 2, y + (50 - hauteur_texte_difficulte) // 2))

        regions_difficulte[option_difficulte] = region_rectangulaire_difficulte
        y += 50 + 20

    pygame.display.flip()

    choix_difficulte = None
    while choix_difficulte not in options_difficulte:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for option_difficulte, region_rectangulaire_difficulte in regions_difficulte.items():
                    if region_rectangulaire_difficulte.collidepoint(pos):
                        choix_difficulte = option_difficulte

    return difficultes[choix_difficulte]


def inserer_mot():
    nouveau_mot = ""
    en_train_d_ecrire = True

    clock = pygame.time.Clock()

    while en_train_d_ecrire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    en_train_d_ecrire = False
                    # Ajouter le nouveau mot au fichier mots.txt
                    with open("mots.txt", "a", encoding="utf-8") as fichier:
                        fichier.write(f"{nouveau_mot} \n")
                elif event.key == pygame.K_BACKSPACE:
                    nouveau_mot = nouveau_mot[:-1]
                elif event.key in range(pygame.K_a, pygame.K_z + 1):
                    lettre = chr(event.key).lower()
                    nouveau_mot += lettre
                elif event.key == pygame.K_ESCAPE:
                    return  # Retourner au menu si la touche Échap est enfoncée

        fenetre.fill(BLANC)

        titre = font.render("Insérer un nouveau mot", True, NOIR)
        fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 50))

        prompt = font.render("Entrez un nouveau mot : {}".format(nouveau_mot), True, NOIR)
        fenetre.blit(prompt, (largeur // 2 - prompt.get_width() // 2, 150))

        pygame.display.flip()
        clock.tick(60)



def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        regions_rectangulaires = afficher_menu()

        choix = None
        while choix not in ["1", "2", "3"]:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Vérifie si les coordonnées du clic sont à l'intérieur de l'une des régions rectangulaires
                    for option, region_rectangulaire in regions_rectangulaires.items():
                        if region_rectangulaire.collidepoint(pos):
                            if option == "Commencer une nouvelle partie":
                                choix = "1"
                            elif option == "Insérer un nouveau mot":
                                choix = "2"
                            elif option == "Quitter le programme":
                                choix = "3"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    choix = "3"  # Revenir au menu si la touche Échap est enfoncée

        if choix == "1":
            difficulte = choisir_difficulte()
            pendu(difficulte)
        elif choix == "2":
            inserer_mot()
        elif choix == "3":
            print("Au revoir !")
            pygame.quit()
            sys.exit()

def pendu(difficulte):
    mot_a_trouver = choisir_mot_aleatoire(difficulte)
    lettres_trouvees = set()
    erreurs_max = len(mot_a_trouver)
    erreurs = 0
    
    pygame.display.set_caption("Jeu du Pendu - Devinez le mot!")

    # Initialisez la liste des lettres essayées à l'extérieur de la boucle principale
    lettres_essayed_liste = []

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Retourner au menu si la touche Échap est enfoncée
                elif event.key in range(pygame.K_a, pygame.K_z + 1):
                    lettre = chr(event.key).lower()
                    if lettre not in lettres_trouvees:
                        lettres_trouvees.add(lettre)
                        lettres_essayed_liste.append(lettre)
                        if lettre not in mot_a_trouver:
                            erreurs += 1

        fenetre.fill(BLANC)

        afficher_mot = afficher_mot_cache(mot_a_trouver, lettres_trouvees)
        mot_texte = font.render(afficher_mot, True, NOIR)
        fenetre.blit(mot_texte, (largeur // 2 - mot_texte.get_width() // 2, 50))

        # Affiche les lettres essayées au-dessus des underscores
        lettres_essayed_texte = font.render(f"Tentatives: {' '.join(lettres_essayed_liste)}", True, NOIR)
        fenetre.blit(lettres_essayed_texte, (largeur // 2 - lettres_essayed_texte.get_width() // 2, 20))

        erreurs_texte = font.render("Erreurs {}/{}".format(erreurs, erreurs_max), True, NOIR)
        fenetre.blit(erreurs_texte, (largeur // 2 - erreurs_texte.get_width() // 2, 200))

        pygame.display.flip()
        clock.tick(60)

        if all(lettre in lettres_trouvees for lettre in mot_a_trouver):
            gagne_texte = font.render("Félicitations! Vous avez deviné le mot '{}'.".format(mot_a_trouver), True, NOIR)
            fenetre.blit(gagne_texte, (largeur // 2 - gagne_texte.get_width() // 2, 250))
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        if erreurs == erreurs_max:
            perdu_texte = font.render("Perdu, vous avez atteint le nombre maximum d'erreurs. Le mot était '{}'.".format(mot_a_trouver), True, NOIR)
            fenetre.blit(perdu_texte, (largeur // 2 - perdu_texte.get_width() // 2, 250))
            pygame.display.flip()
            pygame.time.wait(3000)
            return

# Appeler la fonction menu à la fin du script
if __name__ == "__main__":
    menu()
