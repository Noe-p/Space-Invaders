#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Noé PHILIPPE
## Océane PEZENNEC 
## Groupe 5


# In[2]:


try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox


# In[3]:


class Defender:
    defender_image = None
    touched_image = None

    def __init__(self):
        self.width = 52
        self.height = 32
        self.move_delta = 20
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []
        self.life = []
        self.defender_life=3

    def install_in(self, canvas):
        if self.id == None: 
            cx = int(canvas.cget("width"))
            cy = int(canvas.cget("height")) 
            lx = cx / 2
            ly = cy - self.height
            self.id = canvas.create_image(lx,ly, image=self.ship_image(), tags="ship")
        
        #Vies defender
        lx=50
        for i in range(self.defender_life):
            defender = Defender()
            defender.id = canvas.create_image(lx,30, image=self.ship_image(), tags="ship")
            self.life.append(defender.id)
            lx=lx+self.width+30
   
    @classmethod
    def ship_image(cls):
        if cls.defender_image==None:
            cls.defender_image = tk.PhotoImage(file="img/ship.png")
        return cls.defender_image    
    
    @classmethod
    def ship_touched_image(cls):
        if cls.touched_image==None:
            cls.touched_image = tk.PhotoImage(file="img/touched.png")
        return cls.touched_image     

    def coord(self, canvas):
        return canvas.coords(self.id)    

    def move_in(self, canvas, deplacement):
        max_canvas = int(canvas.cget("width")) #On récupere la taille du canvas
        x1 = self.coord(canvas)[0]
        y1 = self.coord(canvas)[1]
        x2 = x1+self.width 
        y2 = y1+self.height
        if deplacement < 0:#Si on va vers la gauche
            if x1 - self.width/2 >0: #Si on ne dépasse pas le canvas 
                canvas.move(self.id, deplacement, 0)#on se déplace 
        else:
            if x2 - self.width/2< max_canvas: 
                canvas.move(self.id, deplacement, 0)
    
    def animation_projectil(self, canvas):#On appel move_in pour chaques bullets
        for bullet in self.fired_bullets:
            bullet.move_in(canvas, "defender")
        
    def fire(self, canvas):
        if len(self.fired_bullets) < self.max_fired_bullets: #si le nb de bullets est < au max de bullets
            Bullet(self).install_in(canvas, "defender", None)#On creer une nouvelle bullet

    def rm_bullet(self, bullet):# Supprime la bullet de la liste
        self.fired_bullets.remove(bullet)
        
    def defender_touche(self, canvas, fleet):
        bullets = fleet.fired_bullets
        for bull in list(bullets):
            x1, y1, x2, y2 = canvas.coords(bull.id)
            touched = canvas.find_overlapping(x1, y1, x2, y2)
            if self.id in touched:
                bullets.remove(bull) #on suprime le projectil de la liste
                canvas.delete(bull.id)
                canvas.delete(self.life[-1])
                del self.life[-1]
                self.kill_defender(canvas)
    
    def kill_defender(self, canvas):
        lx, ly =self.coord(canvas)
        touche = canvas.create_image(lx,ly, image=self.ship_touched_image(), tags="ship_touched")
        canvas.after(300, canvas.delete, touche)


# In[4]:


class Alien(object):
    alien_image = None
    alien_image1= None
    alien_imageAngry = None

    
    def __init__(self):
        self.id = None
    
    @classmethod
    def get_image(cls): #On reçoit le gif d'un alien qui va être stocké dans une variable et retourné
        if cls.alien_image==None:
            cls.alien_image = tk.PhotoImage(file="img/alien.png")#On ajoute l'image
        return cls.alien_image
    
    @classmethod
    def get_deathImage(cls): #On reçoit le gif d'une explosion qui va être stocké dans une variable et retourné
        if cls.alien_image1==None:
            cls.alien_image1 = tk.PhotoImage(file="img/explosion.png")
        return cls.alien_image1 
    
    @classmethod
    def get_imageAngry(cls):
        if cls.alien_imageAngry==None:
            cls.alien_imageAngry = tk.PhotoImage(file="img/alienAngry.png")#On ajoute l'image
        return cls.alien_imageAngry

    def install_in(self,canvas, x, y, image, tag):
        self.id = canvas.create_image(x, y, image=image, tags=tag)# On crée l'image
        
    def img_alien_vivant(self, canvas, x, y): #installe un alien
        self.install_in(canvas, x, y, self.get_image(), "Alien_vivant")
        
    def img_alien_dead(self, canvas, x, y): #installe une explosion et se détruit au bout de 300 ms
        self.install_in(canvas, x, y, self.get_deathImage(), "Alien_dead")
        canvas.after(300, canvas.delete, self.id)
    
    def move_in(self, canvas, dx, dy): #permet à l'alien de changer de position en fonction des pararamètres
        canvas.move(self.id, dx, dy)
        
    def kill_alien(self, canvas):      #cette fonction permettra de tuer l'alien et de déclencher l'animation de mort 
        x, y = canvas.coords(self.id)
        canvas.delete(self.id)
        self.img_alien_dead(canvas, x, y)


# In[5]:


import random

class Fleet(object):
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        fleet_size = self.aliens_lines * self.aliens_columns
        self.aliens_fleet = [None] * fleet_size
        self.max_fired_bullets = 10
        self.fired_bullets = []
        self.alien_angry=False 

    def install_in(self, canvas):
        x=100
        y=100
        h=0
        for i in range(self.aliens_lines):
            for j in range(self.aliens_columns):
                self.alien = Alien() #On crée un alien 
                self.alien.img_alien_vivant(canvas,x, y)
                self.aliens_fleet[h] = self.alien #On l'ajoute dans la liste
                h+=1
                x+=self.aliens_inner_gap + Alien.get_image().width()#On Maj les coordonnés en X
            y+=self.aliens_inner_gap + Alien.get_image().height()#On Maj les coordonnés en Y
            x=100 #On Maj la position en X
            
    def maj_photo_alien(self, canvas):
        self.alien_angry=True
        for alien in self.aliens_fleet:
            canvas.itemconfigure(alien.id, image=alien.get_imageAngry())
    
    def move_in(self, canvas):
        cwidth = int(canvas.cget("width")) #On récupere la taille du canvas
        x1, y1, x2, y2 = canvas.bbox("Alien_vivant") #On récupere la taille de la flotte
        deplacement_y=0

        if(self.alien_x_delta>0): #déplacement vers la droite
            if x2>cwidth: #si sa dépasse le canvas
                self.alien_x_delta = self.alien_x_delta*-1 #on change le signe
                deplacement_y = self.alien_y_delta #on déplace les aliennes vers le bas
        else:
            if x1<0:
                self.alien_x_delta = self.alien_x_delta*-1 
                deplacement_y = self.alien_y_delta 
        
        for alien in self.aliens_fleet: 
            alien.move_in(canvas, self.alien_x_delta, deplacement_y) #Appel de l'animation pour chaque aliens

    def alien_touche(self, canvas, defender, score):
        bullets = defender.fired_bullets
        for bull in list(bullets):
            x1 = canvas.coords(bull.id)[0]
            y1 = canvas.coords(bull.id)[1]
            x2 = x1 + bull.width
            y2 = y1 + bull.width #width car le projectil est trop grand et créer des erreurs
            touched = canvas.find_overlapping(x1, y1, x2, y2)
            
            for alien in self.aliens_fleet:
                if alien.id in touched:
                    alien.kill_alien(canvas) #On tue un alien
                    bullets.remove(bull) #on suprime le projectil de la liste
                    canvas.delete(bull.id) #On supprime le projectil du canvas
                    self.aliens_fleet.remove(alien) #On supprime l'alien de la liste
                    score.pt= score.pt+10 #On met à jour les point ssur le canvas
                    score.toFile("point.json")
    
    def coord(self, canvas): 
        i = random.randint(0, len(self.aliens_fleet)-1)
        alien = self.aliens_fleet[i]
        coord = canvas.coords(alien.id)
        return coord
    
    def animation_projectil(self, canvas):#On appel move_in pour chaques bullets
        for bullet in self.fired_bullets:
            bullet.move_in(canvas, "alien")
        
    def fire(self, canvas):
        if len(self.fired_bullets) < self.max_fired_bullets: #si le nb de bullets est < au max de bullets
            if self.alien_angry==True:
                Bullet(self).install_in(canvas, "alien", "orange")
            else:
                Bullet(self).install_in(canvas, "alien", "blue")#On creer une nouvelle bullet

    def rm_bullet(self, bullet):# Supprime la bullet de la liste
        self.fired_bullets.remove(bullet)
                    
    def get_width(self):
        return ((73 + self.aliens_inner_gap) * self.aliens_columns + 200)


# In[6]:


class Bullet(object):
    image_bullet=None

    def __init__(self, shooter):
        self.radius = 5
        self.speed = 8
        self.id = None
        self.width=9
        self.height=44
        self.shooter = shooter
    
    def install_in(self, canvas, shooterName, color):
        if self.id == None:
            if shooterName == "alien" : 
                cx=self.shooter.coord(canvas)[0] - self.radius
                cy=self.shooter.coord(canvas)[1] - self.radius*2
                self.id = canvas.create_oval(cx, cy,cx + self.radius*2, cy + self.radius*2, fill=color)
            else:
                cx = self.shooter.coord(canvas)[0] 
                cy = self.shooter.coord(canvas)[1] - self.height/2
                self.id = canvas.create_image(cx,cy, image=self.image(), tags="bullet")
            self.shooter.fired_bullets.append(self)#On ajoute une bullet à la liste
    
    @classmethod
    def image(cls):
        if cls.image_bullet==None:
            cls.image_bullet = tk.PhotoImage(file="img/bullet.png")
        return cls.image_bullet
    
    def move_in(self, canvas, shooter):
        coordonnes = canvas.coords(self.id)#On récupere les cooronnés de la bullet
        if coordonnes[1]>=0 and coordonnes[1]<=800:#si elle ne dépasse pas le canvas
            dx = 0
            if shooter == "alien" :
                dy = self.speed
            else:
                dy = - self.speed
            canvas.move(self.id, dx, dy)#elle se déplace 
        else:
            canvas.delete(self.id)#On la supprime du canvas
            self.shooter.rm_bullet(self)#On la supprime de la liste


# In[7]:


class Shelter(object):
    image_newShelter=None
    image_breakShelter=None
    image_breakShelter2=None
    image_touched = None
    image_kill = None
   
    def __init__(self):
        self.id = None
        self.shelterList = []
        self.nbShelters=3
        self.life = 3
        self.width = 96
        self.height = 72
    
    @classmethod
    def image(cls):
        if cls.image_newShelter==None:
            cls.image_newShelter = tk.PhotoImage(file="img/newShelter.png")
        return cls.image_newShelter
    
    @classmethod
    def imagebreak(cls):
        if cls.image_breakShelter==None:
            cls.image_breakShelter = tk.PhotoImage(file="img/shelter_break1.png")
        return cls.image_breakShelter
    
    @classmethod
    def imagebreak2(cls):
        if cls.image_breakShelter2==None:
            cls.image_breakShelter2 = tk.PhotoImage(file="img/shelter_break2.png")
        return cls.image_breakShelter2
    
    @classmethod
    def shelter_touched_image(cls):
        if cls.image_touched==None:
            cls.image_touched = tk.PhotoImage(file="img/touched.png")
        return cls.image_touched
    
    @classmethod
    def shelter_kill_image(cls):
        if cls.image_kill==None:
            cls.image_kill = tk.PhotoImage(file="img/killShelter.png")
        return cls.image_kill


    def install_in(self,canvas):
        cwidth = int(canvas.cget("width")) / self.nbShelters 
        cheight = int(canvas.cget("height")) 
        lx = (cwidth+self.width*2) / self.nbShelters
        
        for i in range(self.nbShelters):
            shelter = Shelter()
            shelter.id = canvas.create_image(lx,cheight-100, image=self.image(), tags="newShelter")
            self.shelterList.append(shelter)
            lx=lx+cwidth
            
    def shelter_touche_defender(self, canvas, shooter):
        bullets = shooter.fired_bullets
        for bull in list(bullets):
            x1 = canvas.coords(bull.id)[0]
            y1 = canvas.coords(bull.id)[1]
            x2 = x1 + bull.width
            y2 = y1 + bull.width #width car le projectil est trop grand et créer des erreurs
            touched = canvas.find_overlapping(x1, y1, x2, y2)
            
            for shelter in self.shelterList:
                if shelter.id in touched:
                    bullets.remove(bull) #on suprime le projectil de la liste
                    canvas.delete(bull.id)
    
    def shelter_touche_alien(self, canvas, shooter):
        bullets = shooter.fired_bullets
        for bull in list(bullets):
            x1, y1, x2, y2 = canvas.coords(bull.id)
            touched = canvas.find_overlapping(x1, y1, x2, y2)
            
            for shelter in self.shelterList:
                if shelter.id in touched:
                    bullets.remove(bull) #on suprime le projectil de la liste
                    canvas.delete(bull.id)
                    shelter.life=shelter.life-1
                    if shelter.life == 0:
                        kill = canvas.create_image(x1,y1, image=self.shelter_kill_image(), tags="shelter_kill")
                        canvas.after(300, canvas.delete, kill)
                        canvas.delete(shelter.id)
                    else:
                        self.break_shelter(canvas, x1, y1, shelter)                   
    
    def break_shelter(self, canvas, lx, ly, shelter):
        touche = canvas.create_image(lx,ly, image=self.shelter_touched_image(), tags="shelter_touched")
        canvas.after(300, canvas.delete, touche)
        if shelter.life==2:
            canvas.itemconfigure(shelter.id, image=self.imagebreak())
        else:
            canvas.itemconfigure(shelter.id, image=self.imagebreak2())


# In[8]:


class Game(object):
    def __init__(self, frame):
        self.frame = frame
        self.fleet = Fleet()
        self.defender = Defender()
        self.shelter= Shelter()
        self.height =800
        self.width = self.fleet.get_width()
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height, background="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.shelter.install_in(self.canvas)
        self.frame.winfo_toplevel().bind("<Key>", self.keypressed)
        
        #Scores
        self.score = Score.fromFile("point.json")
        self.affiScore = self.canvas.create_text(1000,50,text="{}".format(self.score),font=("Helvetica",12), fill="red")
        self.canvas.create_text(1000,30,text="Meilleur score : {}".format(self.meilleur_score()),font=("Helvetica",12), fill="green")

        #Tires fleet
        self.speedFireFleet=1600
    
    def keypressed(self, event):
        if event.keysym == 'Left':
            self.defender.move_in(self.canvas, -self.defender.move_delta)
        elif event.keysym == 'Right':
            self.defender.move_in(self.canvas, self.defender.move_delta)
        elif event.keysym == 'space':
            self.defender.fire(self.canvas)
            
    def start_animation(self):
        self.animation()
        self.animation_fire_fleet()
    
    def animation(self): # Lance les animations 
        #Fleet 
        self.fleet.move_in(self.canvas)
        self.fleet.animation_projectil(self.canvas)
        self.fleet.alien_touche(self.canvas, self.defender, self.score)
        #Defender
        self.defender.animation_projectil(self.canvas)
        self.defender.defender_touche(self.canvas, self.fleet)  
        #Shelter
        self.shelter.shelter_touche_alien(self.canvas, self.fleet)   
        self.shelter.shelter_touche_defender(self.canvas, self.defender)        

        self.canvas.itemconfigure(self.affiScore, text="{}".format(self.score)) #Mise à jour des points sur le canvas

        resultat = self.endGame()
        if resultat == "jeu":
            self.frame.after(30, self.animation) #Si on est en jeu, on appel recurcivement la fonction animation
        else:
            self.restart(resultat)
            
    def meilleur_score(self):
        for i in Resultat.fromFile("resultat.json").listeScore:
            if i.playerName==self.score.playerName:
                return i.pt
    
    def animation_fire_fleet(self):
        resultat = self.endGame()
        if resultat == "jeu": #On verifie que la partie n'est pas terminé
            self.fleet.fire(self.canvas)
            if self.speedFireFleet <=300:
                self.fleet.maj_photo_alien(self.canvas)
                self.speedFireFleet=300
            else:
                self.speedFireFleet=self.speedFireFleet-150
            self.frame.after(self.speedFireFleet, self.animation_fire_fleet)
            
    def newGame(self, nom):
        self.canvas.destroy()
        game = Score(nom.get(),0)
        game.toFile("point.json")
        game = Game(self.frame)
        game.start_animation()
        
    def restart(self, win):
        self.canvas.delete('all')
        if(win=="gagne"):
            self.canvas.create_text(self.width/2,70,text="Bravo ! Vous avez gagné !",font=("Helvetica",30), fill="red")
        elif(win=="perdu"):
            self.canvas.create_text(self.width/2,70,text="Vous avez perdu...",font=("Helvetica",30), fill="red")
        elif(win=="nomVide"):
            self.canvas.create_text(self.width/2,70,text="Entrer un nom :",font=("Helvetica",30), fill="red")
            
        if win != "nomVide":
            # Score 
            self.canvas.create_text(self.width/2,200,text="Votre Score : {}".format(self.score),font=("Helvetica",15), fill="orange")

        ## Meilleurs Score (Affiche les 8 meilleurs score)
        scoreTitre = self.canvas.create_text(1100/2,250,text="Meilleurs scores :",font=("Helvetica",15), fill="green")
        score = Resultat.fromFile("resultat.json").listeScore
        y=300
        for i in range(8):
            if i < len(score):
                scores = self.canvas.create_text(1100/2,y,text="{}".format(score[i]),font=("Helvetica",10), fill="orange")
                y=y+20 
                
        #Création de l'input
        labelNom = self.canvas.create_text(1100/2,570,text="Entrer votre nom :",font=("Helvetica",10), fill="red")
        inputNom = tk.Entry(self.frame)
        
        ## Création du bouton
        buttonRestart = tk.Button(self.frame, text='Restart', bg='green', command=lambda: self.newGame(inputNom))
 
        ## Insertion dans le canva.
        self.canvas.create_window(550, 600, window=inputNom)
        self.canvas.create_window(550, 700, window=buttonRestart)
        
    def endGame(self): 
        l_fleet = len(self.fleet.aliens_fleet) #On recupere la taille de la liste
        defender_life = len(self.defender.life)
        retour = "jeu"
        
        if self.score.playerName=="":
            retour = "nomVide"
        else:
            if (l_fleet) <= 0: #si il n'y a plus d'aliens
                retour = "gagne"
            else:
                if defender_life != 0:
                    x1, y1, x2, y2 = self.canvas.bbox("Alien_vivant") #On récupere la taille de la flotte
                    if y2 > self.height:
                        retour = "perdu"
                else: retour = "perdu" 
        
        ## si la partie est terminée
        
        if retour != "jeu" and (retour != "nomVide"): 
            new=1
            j=0
            for i in Resultat.fromFile("resultat.json").listeScore: #on se déplace dans la liste des joueurs
                if i.playerName==self.score.playerName: #si le nom du joueur existe déjà
                    if i.pt < self.score.pt: #si les point de la partie son meilleurs que celle déja enregistré
                        resultat = Resultat.fromFile("resultat.json") 
                        resultat.remove(j) #on supprime la partie enregistré
                        resultat.toFile("resultat.json") #on insere la nouvelle partie
                    else:
                        new=0
                j=j+1
            if new==1: # si le joueur n'existe pas
                resultat = Resultat.fromFile("resultat.json")
                resultat.ajout(self.score) # On le rajoute 
                resultat.toFile("resultat.json")   

        return retour


# In[9]:


import json

class Score(object):
    def __init__(self, playerName, pt):
        self.playerName = playerName 
        self.pt = pt 
        
    def get_playerName(self): 
        return self.playerName
    
    def get_pt(self):
        return self.pt 
    
    def toFile(self, name):
        f = open(name,"w")
        l=self
        json.dump(l.__dict__,f)
        f.close()
    
    @classmethod
    def fromFile(cls, name):
        f = open(name,"r")
        d = json.load(f)
        lnew=Score(d["playerName"],d["pt"])
        f.close()
        return lnew
    
    def __str__(self):
        return str(self.playerName)+" : "+str(self.pt)

class Resultat(object):
    def __init__(self):
        self.listeScore = []
        
    def ajout(self, score): # Ajout dans l'ordre croissant
        test=0
        for i in range(len(self.listeScore)):
            if (score.pt>self.listeScore[i].pt and test==0):
                self.listeScore.insert(i, score)
                test=1
        if test==0:
            self.listeScore.append(score) 
        
    def remove(self, indice):
        supp = self.listeScore.pop(indice)
        
    def __str__(self):
        chaine=str(self.listeScore[0])
        for e in self.listeScore[1:]:
            chaine=chaine+ "\n" + str(e)
        return chaine
    
    def toFile(self,fich):
        f = open(fich,"w")
        tmp = []
        for l in self.listeScore:
        #créer un dictionnaire
            d = {}
            d["playerName"] = l.playerName
            d["pt"] = l.pt
            tmp.append(d)
        json.dump(tmp,f)
        f.close();
        
    @classmethod
    def fromFile(cls,fich):
        f = open(fich,"r")
        #chargement
        tmp = json.load(f)
        
        liste = []
        for d in tmp:
            #créer un livre
            l=Score(d["playerName"],d["pt"])
            #l'ajouter dans la liste
            liste.append(l)
        res=Resultat()
        res.listeScore=liste
        f.close();
        return res


# In[10]:


class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        self.frame = tk.Frame(self.root)
        self.frame.pack(side="top", fill="both", expand=True)
        self.root.resizable(0, 0)
        
        self.canva2 = tk.Canvas(self.root, width=1100, height=800, bg='black') # 2eme canvas pour le menu
        self.canva2.pack()
    
    def play(self): #le jeu débute contre les aliens
        self.menu()
        self.root.mainloop()
    
    def start(self):   #l'écran start commence (??)
        game = Game(self.frame)
        game.start_animation()
    
    def scoreGame(self, nom): #insere les infos du joueur dans point.json
        self.canva2.destroy()
        game = Score(nom.get(),0)
        game.toFile("point.json")
        self.start()
        
    def menu(self):
        ## Titre 
        titre = self.canva2.create_text(1100/2,70,text="SPACE INVADERS",font=("Helvetica",30), fill="red")
        
        ## Meilleurs Score (Affiche les 8 meilleurs score)
        scoreTitre = self.canva2.create_text(1100/2,200,text="Meilleurs scores :",font=("Helvetica",15), fill="green")
        score = Resultat.fromFile("resultat.json").listeScore
        y=250
        for i in range(8):
            if i < len(score):
                scores = self.canva2.create_text(1100/2,y,text="{}".format(score[i]),font=("Helvetica",10), fill="orange")
                y=y+20
        
        #Création de l'input
        labelNom = self.canva2.create_text(1100/2,570,text="Entrer votre nom :",font=("Helvetica",10), fill="red")
        inputNom = tk.Entry(self.root)
        
        ## Création du bouton
        buttonStart = tk.Button(self.root, text='Start', bg='green', command= lambda: self.scoreGame(inputNom))
 
        ## Insertion dans le canva.
        self.canva2.create_window(550, 700, window=buttonStart)
        self.canva2.create_window(1100/2, 600, window=inputNom)

SpaceInvaders().play()

