from jeu_de_la_vie import *

def main():

    width = 1000
    height = 600

    nmbre_case_width = 100
    nmbre_case_height = 60

    jeu = Game(width, height, nmbre_case_width, nmbre_case_height)
    jeu.main_loop()

if __name__ == "__main__":
    main()