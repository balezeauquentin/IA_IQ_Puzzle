import jeu

def brutforce(table,tab=[k for k in range(12)],b=0):
    """ Fonction qui va tester toutes les combinaisons possibles
        et qui va renvoyer la combinaison gagnante.
    """
    a=jeu.piece(1)

    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] == 0:
                for k in range(1, 12):

                    if tab[k] != 0:
                        for l in range(4):
                            a.piece=jeu.piece(k)
                            a.piece=jeu.tourner_piece_horraire(a.piece)

                            bool=jeu.placer_piece(table, a.piece, (i, j))
                            tab[k]=0
                            table.afficher_tableau_console()
                            brutforce(table,tab,b+1)
                            print(b)
                            if bool:
                                break
                            print("pas de reponse")

        print("pas de reponse")
    print("pas de reponse")




table=jeu.plateau(10,10)
brutforce(table)