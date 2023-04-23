import pygame, sys, os
from pygame.locals import *
import random

#background music
from pygame import mixer

# scroll background, file... 
# treba fix, da, bi mogao da draw-uje.... jer nece druge elemente da prikaze..
#from scrollable_background import scroll_bg


# pygame init
pygame.init()



#set up window
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("X-Galactic-Blitz")


# background
BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (WIDTH, HEIGHT))


# LOAD SPACESHIPS
YELLOW_SPACESHIP = pygame.image.load(os.path.join("images", "player.png"))

RED_SPACESHIP = pygame.image.load(os.path.join("images", "pixel_ship_red_small.png"))
BLUE_SPACESHIP = pygame.image.load(os.path.join("images", "pixel_ship_blue_small.png"))
GREEN_SPACESHIP = pygame.image.load(os.path.join("images", "pixel_ship_green_small.png"))






 
# Ship Parent class to inherit player and enemy ship class
class Ship:
    # pozicija ship-a
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
    
    # draw ship na ekranu
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    # funkcija da se dobije širina ship-a, image-a
    def get_width(self):
        return self.ship_img.get_width()
    
    # funkcija da se dobije visina ship-a, image-a
    def get_height(self):
        return self.ship_img.get_height()




"""

Player Ship class which inherits from Ship class


- The line of code self.mask = pygame.mask.from_surface(self.ship_img) creates a collision mask for the enemy ship based on its image.

A collision mask is a Mask object that is used to detect collisions between two objects in a game. The from_surface method of the pygame.mask module creates a Mask object from a given image Surface.

"""
class Player(Ship):

    # pozicija ship-a
    def __init__(self, x, y):
        super().__init__(x, y)

        # vidi ovo gore docs
        self.ship_img = YELLOW_SPACESHIP  # postavljanje slike za ovaj ship
        self.mask = pygame.mask.from_surface(self.ship_img)  
    
    
    # draw ship na ekranu, koristi funkciju od superclass (parent class..)
    def draw(self, window):
        super().draw(window)





"""

Enemy ship class which inherits from ship class


- The line of code self.mask = pygame.mask.from_surface(self.ship_img) creates a collision mask for the enemy ship based on its image.

A collision mask is a Mask object that is used to detect collisions between two objects in a game. The from_surface method of the pygame.mask module creates a Mask object from a given image Surface.

"""
class Enemy(Ship):

    # random ikonica enemy ship-a.. ovo je dictionary
    COLOR_MAP = {
        "red": (RED_SPACESHIP),
        "blue": (BLUE_SPACESHIP),
        "green": (GREEN_SPACESHIP)
    }

    # pozicija ship-a, takodje, u ovaj child, se kreira dodatni argument (override od parent, ovaj dodatni, konstruktor)
    def __init__(self, x, y, color):
        super().__init__(x, y)  # draw position
        
        # vidi ovo gore docs
        self.ship_img = self.COLOR_MAP[color]  # postavljanje slike za ovaj ship
        self.mask = pygame.mask.from_surface(self.ship_img)

    # To move down the enemy ship, ovo je definisano samo u ovaj child class.. 
    def move(self, vel): 
        self.y += vel   # on se pokrece, tako sto se njegova y pozicija povećava. znaci, sto je veci y pozicija, on ustvari ide ka dole. a sto je manja y pozicija ide ka gore.. to je po pygame pravila.. 




"""

funkcija za detekciju collisions

znaci, posto su enemy i player objekti, mi pass-ujemo: collide(enemy, player), sto znaci, da je prvi objekat enemy ship, drugi objekat player ship (ti naravno, gubis lives, ako enemy predje liniju ispod ekrana). 


- Calculate the offset between the positions of the two objects in the x and y directions. The offset is the difference between the x and y coordinates of obj2 and obj1, respectively.

- Call the overlap method of the collision mask of obj1 with the collision mask of obj2 as its argument. The overlap method returns a pygame.Rect object representing the overlapping area of the two masks, or None if the masks don't overlap.


- If the return value is not None, it means that the two objects have collided, so the function returns True. Otherwise, it returns False.

"""
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x   
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def background_music():
    # background music
    mixer.init()                     # Starting the mixer
    mixer.music.load(os.path.join("music", "Sadder_Days_Omelas_Snippet_.ogg"))     # Loading the song 
    mixer.music.set_volume(0.7)      # Setting the volume
    mixer.music.play()               # Start playing the song

# glavni dio funkcionalnosti
def main():


    # background music 
    #               UNCOMMENT THIS, WHEN YOU START WORKING ON IT
    # background_music()

    # game states
    run = True
    lost = False
    lost_count = 0
    level = 0
    lives = 3

    # perfomanse
    FPS = 60

    # brzina enemy-a
    ENEMY_VEL = 3
    
    # enemy list, koji se povecava sa level-ima
    enemies = []

    # ovo je, koliko enemies, ce biti učitano u sledeći level ! svaki sledeci level, ce ovo da se poveca za +5. time, izazivajući, da imamo +5 enemies u odnosu naprethodni put.. 
    wave_length = 0


    # font 
    main_font = pygame.font.SysFont("comicsans", size= 50)

    # postavljanje player ship u centru (ali necemo ga morati pomerati, zato u main event loop, nemamo, nikakve event listeners za player, jer nam ne trebaju u ovoj igri. cilj, je samo iskucati enemies, da se uniste na taj nacin )
    player = Player(240, 480)

    # za redrawing.. 
    clock = pygame.time.Clock()


    def redraw_window():

        # DRAWING THE BACKGROUND
        WIN.blit(BG, (0,0))

        # DRAW TEXT
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))  #level
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))  #lives 
        WIN.blit(lives_label, (10, 10)) # lives se stavlja na ekran, na poziciji, gornji levi ugao
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10)) # level se stavlja na ekran, na poziciji, gornji desni ugao


        # SHIP DRAWING (drawuj, sve enemies koje imas u listi... zato koristimo for loop..)
        for enemy in enemies:
            enemy.draw(WIN)

        # takodje, drawuj, i player (posto se ne pomera, ovo ni ne mora, ali neka stoji u jednoj funkciji)
        player.draw(WIN)
        

        # IF WE LOSE
        if lost:
            lost_label = main_font.render("YOU LOST!", 1, (255,255,255)) # da kreira label
            WIN.blit(lost_label, ((WIDTH-lost_label.get_width())//2, (HEIGHT-lost_label.get_height())//2)) # i da ga prikaze na ekranu
        
        # UPDATING THE DISPLAY
        pygame.display.update()
    

    # main game loop
    while True: 
        

        # scroll background, sa fajla funkciju uzima..  (ovo nesto nece ove druge stvari da prikaze.. nesto tu treba, prilagoditi)
        #scroll_bg(WIN)

        #na osnovu clock, jer clock, ce praviti pauze, da ne bi zbog infinite while loop, PC uzimao resurse previse, tj. da ne bi redraw previse često
        clock.tick(FPS)
        redraw_window() # UPDATING DISPLAY 

        
        """

        # provera, da li imamo dovoljno zivota, da nastavimo igrati. 

        - Check if the number of remaining lives is less than or equal to 0. If it is, set the lost variable to True, which indicates that the game has been lost. Also, increment the lost_count variable by 1.


        - Ako je igra izgubljena jer nema vise zivota, onda u sledeci if case (odmah posle ovog, ne ceka sledeci loop), on ce da proveri da li je 'lost' varijable True. ako jeste, onda, ce da proveri, da li je igra izgubljena duze od 3 sekundi (znaci, 'lost_count' ce da se povecava, dok ne dodje do 3 sekundi.. ). i onda 'run' varijabla ce se stavit na False. sto ce 'halt-ovati' main loop (zato sto u sami while loop stoji: 'while run: ' , sto znaci, da while petlja izvrsava, dokle god, je run True.. sto u ovaj slucaj, pri sledecoj iteraciji za while petlju, nece biti True, i igra ce se zaustaviti

        

        )

        - I takodje, ako smo izgubili, varijabla 'lost' ce biti na True, i time ce se zaustaviti sve sto se kretalo, i nece moci da se krece nista vise. 
        I ovaj 
        # IF WE LOSE
        if lost:
            lost_label = main_font.render("YOU LOST!", 1, (255,255,255)) # da kreira label
            WIN.blit(lost_label, ((WIDTH-lost_label.get_width())//2, (HEIGHT-lost_label.get_height())//2)) # i da ga prikaze na ekranu

        dio, ce da se execute i prikaze, kada se igra izgubi !  i time zavrsavajuci igru.. to je to..



        """
        # provera, da li imamo dovoljno zivota, da nastavimo igrati. 
        if lives <= 0:
            lost = True  
            lost_count += 1
        if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue
            

        # ADDING ENEMIES IN THE LIST AND SPAWNING THEM 
        # kada se svi enemies uniste, onda je lista prazna, i onda, dodamo nove varijable..
        if len(enemies) == 0:
            level += 1   
            wave_length += 5  # +5 enemyes
            ENEMY_VEL += 0.1  #takodje, da se poveca brzina


            # i sada, ce ova funkcija, da kreira, toliko novih, objekata Enemy-a. u zavisnosti od wave_lenght, koji je, koliko enemy-a ce biti sada u ovaj level..
            for _ in range(wave_length):
                # podseti se, konstruktor za Enemy je: def __init__(self, x, y, color):, tako da su ovo samo parametri, da 'x' i 'y' pozicija bude random 
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500 *(1+level//4), -100), random.choice(["red", "green", "blue"]))
                # i to se doda u postojecoj listi... 
                enemies.append(enemy)


        # vazi za svaki enemy objekat, u listi
        for enemy in enemies[:]:
            enemy.move(ENEMY_VEL) #pokrece enemy-a, ka dole.. 

            # ako se sudare enemy, i player, gubis live
            # takodje, i ako enemy, predje ispod ekrana.. nisi ga unistio pre nego je uspeo da pobegne
            # collide funkcija, ce vratiti True, ako su se collide-ovali ! a False ako ne (i time se ovo nece izvrsiti). vidi objasnjenje za collide funkciju kako radi, kod 'return' je to.. 
            if collide(enemy, player):
                lives -= 1
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)




        # checking for events ********** 
        for event in pygame.event.get():





            # quit if X button pressed (in window)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                

        # checking for events ********** 


        # redraw (update) screen
        pygame.display.update()



def main_menu():
    title_font = pygame.font.SysFont("comicsans", 75)
    run = True

    while run:
        
        # title da bude u sredini ekrana, kao launch screen ..
        title_label = title_font.render("Press any key to begin...", 1, (255,255,255))
        WIN.blit(BG, (0,0))
        WIN.blit(title_label, ((WIDTH-title_label.get_width())//2, (HEIGHT-title_label.get_height())//2))
        pygame.display.update()

        # čeka na event, ako pritisne bilo koje dugme, da pocne igra..
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #start, on any key
            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()

# prvo prikaze, da bi poceo igru.. (launch screen, kobajagi... )
main_menu()
