PEZENNEC Océane
PHILIPPE Noé
_Groupe 5_

# Synthèse du jeu Space Invaders


La classe Bullet a pour objectif de créer les balles et leurs utilités via les fonctions :
la fonction __init__ contient les variables contenues dans la classe.
la fonction install_in() prend en paramètre le canva et le nom du joueur et en fonction de si c'est l'alien ou le joueur qui shoote, la forme du bullet change.
la fonction image() prend en paramètre cls et retourne l'image de la balle.
la fonction move_in() prend en paramètre le canva et le shooter  et produit l'animation qui fera déplacer les balles en fonction de si ça vient du joueur ou de l'alien.


la classe Defender a pour but de créer le personnage qu'on pourra contrôler et ce qu'il peut faire :
la fonction __init__ contient les variables contenues dans la classe.
la fonction install_in() permet de créer le defender et le nombre de vie qu'il peut se permettre.
la fonction ship_image(cls) stocke et retourne l'image "ship.png".
la fonction ship_touched_image() stocke et retourne l'image "touched.png".
la fonction coord() prend en paramètre canvas et retourne les coordonnées du canvas (à la rigueur le defender)
la fonction move_in() permet de limiter l'intervalle ou le defender peut se déplacer.
la fonction animation_projectil() est appelé à chaque fois que le defender tire.
la fonction fire() prend en paramètre un canva et si le nombre de bullets est inférieur au maximum de bullet, on crée un nouveau bullet.
la fonction rm_bullet() permet de supprimer le bullet tiré de la liste
la fonction defender_touche() permet de retirer une vie au joueur lorsqu'il se fait toucher et si il est touché 3, on appelle kill_defender.
la fonction kill_defender() permet de supprimer le defender si il se fait tuer.



la classe Alien permet de créer un alien et les fonctionnalités qui vont avec :
la fonction get_image() reçoit le gif d'un alien qui va être stocké dans une variable et retourné.
la fonction get_deathImage() reçoit le gif d'une explosion qui va être stocké dans une variable et retourné.
la fonction install_in() installe l'image de l'alien vivant.
la fonction img_alien_vivant()  retourne et installe un alien.
la fonction img_alien_dead() installe une explosion et se détruit au bout de 300 ms.
la fonction move_in() permet à l'alien de changer de position en fonction des pararamètres.
la fonction kill_aliens() permet de tuer l'alien et de déclencher l'animation de décès/explosion.


la classe fleet permet de créer une flotte d'alien et les fonctions liés :
la fonction  install_in() permet de créer la flotte d'alien.
la fonction move_in() prend en paramètre un canva(qui corresppond à la flotte) permet à la flotte de se déplacer en descendant de droite à gauche de l'écran sans en sortir.
la fonction alien_touche() prend en paramètre le canva, le defender et le score tel que l'alien touché par le defender augmentera le nombre de points et s'inscrira dans le fichier contenant les scores.
la fonction coord() prend en paramètre le canva et retourne les coordonnées du canva.
la fonction animation_projectil() prend en paramètre canva et permet de faire l'animation des projectiles.
la fonction fire permet que si le nb de bullets est < au max de bulletsalors On crée une nouvelle bullet
la fonction rm_bullet() supprime la bullet de la liste.
la fonction get_width() retourne la longueur du canva.



la classe shelter permet de (???):
la classe Game réunit toutes les classes ci-dessus tel que :
la fonction __init__ contient les variables contenues dans la classe.
la fonction keypressed() prend en paramètre event qui est la touche de clavier et permet l'intéraction entre le joueur et le jeu via le clavier
la fonction start_animation() permet de lancer l'animation (??)
la fonction animation() fait appel à l'animation des différentes classes fleet et defender et l'interaction entre l'alien et le joueur. (?)
la fonction meilleur_score() retourne le nom et le score du joueur qui a le plus de points.
la fonction tire_fleet() permet aux aliens de tirer (??)
la fonction maj_points() fait la mise à jour de tout les points dans le canvas.
la fonction newGame() permet de refaire un nouveau jeu.
la fonction restart() permet d'afficher les messages de fond : "Bravo ! Vous avez gagné !" et "Vous avez perdu..." et l'affichage des 8 meilleurs scores.( ??)
la fonction endGame() permet de terminer la partie si les aliens touchent le sol ou le defender 3 fois.
la classe Score permet d'exploiter le score du joueur :
la fonction __init__ contient les variables contenues dans la classe.
la fonction get_playerName permet de stocker/retourner le nom
la fonction get_pt retourne ??
la fonction toFile permet de modifier le fichier "name"
la fonction fromFile stocke le nom du joueur et le score qui lui ait associé
la fonction __str__ permet d'afficher sur le Kernel [nom] : [score]

la classe Resultat (???)
la fonction __init__ contient la variable self.listeScore qui est une liste qui stockera les scores.
la fonction ajout() prend en paramètre le score et le rajoute à la liste self.listeScore dans l'ordre décroissant.
la fonction remove() prend en paramètre "indice" efface un score de la liste à l'index "indice".
la fonction __str__ permet d'afficher les scores dans le jeu
la fonction toFile ???
la classe fromFile ??


la classe space invaders lance le jeu en appelant la classe Game avec d'autres fonctionnalités :

la fonction __init__ contient les variables contenues dans la classe.
la fonction play() lance le jeu.
la fonction start() permet de commencer le jeu.
la fonction scoreGame() prend en paramètre le nom du joueur et stocke le nom et le score dans un fichier.
la fonction menu() permet d'afficher les scores et de pouvoir mettre au début son nom.
