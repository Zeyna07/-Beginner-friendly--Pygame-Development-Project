'''
-screen area: (670, 670)
-game area: (600, 600)
-24x24 sprites // 25x25 grid
-Block coordinates: 
    -top left: -288, 288
    -top right: 288, 288
    -bottom left: -288, -288
    -bottom right: 288, -288

'''
import pygame
import turtle 
import math
import random
import sys 
from button import Button

pygame.init()
pygame.mixer.init()

running = True
game_over = False

#setup the window
window = turtle.Screen()
window.title("Wizard Dash: The Maze Quest")
window.setup(670, 670)
window.bgcolor("black")
window.tracer(0)


screen = pygame.display.set_mode((670, 670))
Time_limit = 120
start_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 24)

pygame.display.set_caption("Menu")

BG = pygame.image.load("background.jpeg")


#sound effects
treasure_sound = pygame.mixer.Sound("sound/treasure.mp3")
enemy_hit_sound = pygame.mixer.Sound("sound/enemy_hit.mp3")
pygame.mixer.music.load("sound/game_background.mp3")

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
treasure_sound.set_volume(0.8)
enemy_hit_sound.set_volume(0.6)

#pause function
is_paused = False
pause_duration = 0
pause_start_time = 0



def get_font(size):
    return pygame.font.Font(None, size)

#main menu 
def main_menu():
    """Displays the main menu. When PLAY is clicked this function returns
    and the game loop starts. EXIT quits the program.
    """
    pygame.display.set_caption("Menu")
    while True:
        # Clear the screen (use BG if available)
        try:
            screen.blit(BG, (0, 0))
        except Exception:
            screen.fill((0, 0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(75).render("MAIN MENU", True, "White")
        menu_rect = menu_text.get_rect(center=(335, 100))
        screen.blit(menu_text, menu_rect)

        play_button = Button(image=None, pos=(335, 250), 
                             text_input="PLAY", font=get_font(75),
                             base_color="Brown", hovering_color="Red")
        exit_button = Button(image=None, pos=(335, 400), 
                             text_input="EXIT", font=get_font(75),
                             base_color="Brown", hovering_color="Red")

        for button in [play_button, exit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    # Start the main game by returning to the caller
                    return
                if exit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

#play screen
def play_screen():
    pygame.display.set_caption("Play")

    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        #screen.fill("black")

        play_text = get_font(45).render("Play Screen", True, "White")
        play_rect = play_text.get_rect(center=(335, 100))
        screen.blit(play_text, play_rect)

        play_back_button = Button(image=None, pos=(335, 550), 
                                                                    text_input="BACK", font=get_font(75),
                                                                    base_color="White", hovering_color="Pink")
        
        play_back_button.change_color(play_mouse_pos)
        play_back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back_button.check_for_input(play_mouse_pos):
                    return

        pygame.display.update()

#options screen
def options_screen():
    pygame.display.set_caption("Options")

    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        options_text = get_font(45).render("Options Screen", True, "White")
        options_rect = options_text.get_rect(center=(335, 100))
        screen.blit(options_text, options_rect)

        options_back_button = Button(image=None, pos=(335, 550), 
                                                                         text_input="BACK", font=get_font(75),
                                                                         base_color="White", hovering_color="Pink")
        
        options_back_button.change_color(options_mouse_pos)
        options_back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back_button.check_for_input(options_mouse_pos):
                    return

        pygame.display.update()


#register the shapes 
turtle.register_shape("wall.gif")
turtle.register_shape("wizard_right.gif")
turtle.register_shape("wizard_left.gif")
turtle.register_shape("treasure.gif")
turtle.register_shape("enemy.gif")


#create grids
class Grid(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

#create players
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wizard_right.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0
        # flag to prevent continuous damage while colliding
        self.hit = False

    def go_up(self):
        new_x = self.xcor()
        new_y = self.ycor() + 24        
        #check for wall collision
        if (new_x, new_y ) not in walls:
            self.goto(new_x, new_y) 
                      

    def go_down(self):
        new_x = self.xcor()
        new_y = self.ycor() - 24

        if (new_x, new_y) not in walls: 
            self.goto(new_x, new_y)

    def go_left(self):
        new_x = self.xcor() - 24
        new_y = self.ycor()
        self.shape("wizard_left.gif")
        
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)


    def go_right(self):
        new_x = self.xcor() + 24
        new_y = self.ycor()
        self.shape("wizard_right.gif")

        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False
        

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.gold = 100

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("enemy.gif")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])
        # schedule the first move for this enemy
        try:
            turtle.ontimer(self.move, random.randint(50, 150))
        except turtle.Terminator:
            pass

    def move(self):
        # don't move while the game is paused; reschedule to keep polling
        if 'is_paused' in globals() and is_paused:
            try:
                turtle.ontimer(self.move, 200)
            except turtle.Terminator:
                return
            return
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0
        
        #if the player is close, move toward the player
        if self.is_close(player):
            if player.xcor() > self.xcor():
                self.direction = "right"
            elif player.xcor() < self.xcor():
                self.direction = "left"
            elif player.ycor() > self.ycor():
                self.direction = "up"    
            elif player.ycor() < self.ycor(): 
                self.direction = "down"   

        #where the enemy is moving to
        new_x = self.xcor() + dx
        new_y = self.ycor() + dy

        # check for wall collision and move or change direction
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)
        else:
            # choose a different direction and don't move this turn
            self.direction = random.choice(["up", "down", "left", "right"])

        # schedule the next move regardless of whether this move succeeded
        try:
            turtle.ontimer(self.move, random.randint(100, 300))
        except turtle.Terminator:
            return

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))    
        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()    

    

#create levels 
levels = [""]

#level 1
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX", 
    "XP  XXXXXXX         EXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X       XX       X     TX",
    "XXXXXX  EX       X  XXXXX",
    "XXXXXX       XXXX   XXXXX",
    "XXXXXX  XXXXXXXXXX  XXXXX",
    "XT       X              X",
    "X XX X  X  XXXXXX  XXXXXX",
    "X XX E     X    X       X",
    "X    XXXXX X    X  XXXXXX",
    "XXXXXX     XX  XX  TXXXXX",
    "XXXXXX  XXXXX  XX   XXXXX",
    "X       X      TX       X",
    "X  XXXXXE  XXXXXX  XXXXXX",
    "X  XXXXXX          XXXXXX",
    "X  XXXXXXXXXXXX   XXXXXXX", 
    "X              X        X",
    "XX    XXXXXXXXXXXX   XXXX", 
    "XX    TXXXXXXXX      XXXX",
    "XX  XXXXXXX  XXXXX     XX",
    "XX           EXXXXX     X",
    "XXXXXXXXXXX      XXX  XXX",
    "XXXXXXXXXXE            XX",
    "XXXXXXXXXXXXXXXX      XXX", 
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

#lists
treasures = []
enemies = []

#add maze to maze list
levels.append(level_1)

#create function to set up level
def setup_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            #get the charcter at each x and y coordinate
            #note the y coordinate is reversed in the next line
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                #check if it's an X to add a wall
                grid.goto(screen_x, screen_y)
                grid.shape("wall.gif")
                grid.stamp()
                walls.append((screen_x, screen_y))

                #check if it's a P that represents the player
            if character == "P":
                player.goto(screen_x, screen_y)

            if character == "T":
                #add a treasure
                treasures.append(Treasure(screen_x, screen_y))

            if character == "E":
                #add an enemy
                enemies.append(Enemy(screen_x, screen_y))

#class instances
grid = Grid()
player = Player()

# turtle writer for pause message (shown on the game window)
pause_writer = turtle.Turtle()
pause_writer.hideturtle()
pause_writer.penup()
pause_writer.color("yellow")

walls = []

#setup first level
setup_level(levels[1])

# Show the main menu and wait until the user presses PLAY (or Exit)
main_menu()

#keyboard bindings
turtle.listen()
turtle.onkey(player.go_down, "Down")
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")

#screen updates
turtle.tracer(0)

clock = pygame.time.Clock()
# enemies schedule their own moves in their constructor; no need to schedule here


#main loop
while True: 
    #pause game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Toggle pause with Space
            if event.key == pygame.K_SPACE:
                if not is_paused:
                    is_paused = True
                    pause_start_time = pygame.time.get_ticks()
                    # show pause text on turtle window
                    pause_writer.goto(0, 0)
                    pause_writer.write("PAUSED", align="center", font=("Arial", 24, "bold"))
                else:
                    is_paused = False
                    # accumulate total paused time so the timer doesn't advance while paused
                    pause_duration += pygame.time.get_ticks() - pause_start_time
                    pause_writer.clear()
    
    if is_paused:
        # show pause overlay in pygame window as well
        try:
            screen.blit(BG, (0, 0))
        except Exception:
            screen.fill((0, 0, 0))
        pause_text = font.render("PAUSED - Press SPACE to resume", True, (255, 255, 0))
        screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height() // 2))
        pygame.display.update()
        # don't advance game logic or collisions while paused
        continue
            
    #check for collision with treasures
    for treasure in treasures:
        if player.is_collision(treasure):
            treasure_sound.play()
            player.gold += treasure.gold
            print("Gold: {}".format(player.gold))
            treasure.destroy()
            treasures.remove(treasure)

    # If all treasures are collected, end the game
    if not treasures:
        game_over = True
        print("You collected all treasures! You win!")
        try:
            screen.blit(BG, (0, 0))
        except Exception:
            screen.fill((0, 0, 0))
        win_text = font.render("You collected all treasures! You win!", True, (0, 255, 0))
        screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2,
                               screen.get_height() // 2 - win_text.get_height() // 2))
        pygame.display.update()
        # short pause so player sees the message, then exit cleanly
        pygame.time.delay(3000)
        pygame.quit()
        try:
            turtle.bye()
        except Exception:
            pass
        sys.exit()



    # Check for collision with enemies
    collided = False
    for enemy in enemies:
        if player.is_collision(enemy):
            enemy_hit_sound.play()
            collided = True
            if not player.hit:
                gold_lost = min(player.gold, 10)
                player.gold -= gold_lost
                print("Lost gold:", gold_lost)
                player.hit = True

    if not collided:
        player.hit = False

    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time - pause_duration) / 1000
        remaining_time = max(0, Time_limit - int(elapsed_time))
        time_text = font.render("Time Left: {}".format(remaining_time), True, (255, 255, 255))
        window.title("Wizard Dash: The Maze Quest - Time Left: {}".format(remaining_time))

 
        if remaining_time <= 0:
            game_over = True
            print("Time's up! Game Over!")

     
    turtle.update()
