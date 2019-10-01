import pygame, sys
import time, random
from typing import TextIO, List

"""Setting the game GUI settings"""
pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
msElapsed = clock.tick(5)
delay = 0.000005

#Constants:
WHITE=(255,255,255)
BLACK = (0,0,0)
BALL_RADIUS = 10
SLIT_SIZE = 80, 10
SLIT1_Y_LOCATION = height - SLIT_SIZE[1]
SLIT2_Y_LOCATION = 0
FONT = pygame.font.SysFont(None, 25)

#BUTTONS
b_button = pygame.font.SysFont(None, 50)
s_button = pygame.font.SysFont(None, 20)


################ Save functions ####################:
def read_scores() -> List:
    """This will read the scores from the saved file and
    import them as a (name, score) tuple into a dictionary"""
    score_lst = []
    with open ('scoreboard.txt') as f:
        try:
            for line in f:
                read_data = line.strip('\n').split()
                score_lst.append((read_data[0],int(read_data[1])))
            return score_lst
        except IndexError:
            return []
        finally:
            f.close()


def insert_index(lst, score) -> int:
    """receive list and insert the new score into the list
    in descending order"""
    if len(lst) < 1:
        return 0
    i = 0
    while i < len(lst) and lst[i][1] > score:
        i += 1
    if i > 9:
        return -1
    return i

def save_score(name: str, score: int) -> None:
    """This will save the score into a textfile, given the
    score is in the top 10 scores"""
    _scores = read_scores()
    index = insert_index(_scores, score)

    if insert_index != -1:
        _scores.insert(index, (name, score))
        if len(_scores) <= 10: #List is not full yet
            with open('scoreboard.txt', 'w') as f:
                for entry in _scores:
                    f.write(entry[0] + ' ' + str(entry[1]) + '\n')
            f.close()
        else:
    ##        Pop lowest score, note at this point, you have already added the
    ##        new score into the list.
            _scores.pop()
            with open('scoreboard.txt', 'w') as f:
                for entry in _scores:
                    f.write(entry[0] + ' ' + str(entry[1]) + '\n')
            f.close()

def ranked(score) -> bool:
    """Return True iff the score should be saved onto the scoreboard"""
    _scores = read_scores()
    if (len(_scores) < 10) or (_scores[len(_scores)-1][1] < score):
        return True
    return False
        

def get_name() -> str:
    """Get an input of the user's name and return it"""
    congratulate = s_button.render("Congratulations! You have ranked in the top 10 scores.", True, WHITE)

    stay = True
    name = ''
    while stay and len(name) < 21:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                new_character = pygame.key.name(event.key)
                if new_character != 'return' and new_character != 'left'\
                   and new_character != 'right':
                    name += new_character
                if new_character == 'backspace':
                    name = name[:-10]
                elif new_character == 'return':
                    stay = False             
        screen.fill(BLACK)
        screen.blit(congratulate, (200, 180))
        question = s_button.render("WHAT IS YOUR NAME?", True, WHITE)
        screen.blit(question, (200, 200))
        name_display = s_button.render(name, True, WHITE)
        screen.blit(name_display,(200, 220))
        pygame.display.update()    
    return name
    
    
def settings() -> None:
    """This will allow players to change the difficulty
    of the game"""
    screen.fill(BLACK)
    difficulty = b_button.render("DIFFICULTY", True, WHITE)
    easy = s_button.render("EASY", True, BLACK)
    med = s_button.render("MEDIUM", True, BLACK)
    hard = s_button.render("HARD", True, BLACK)
    extreme = s_button.render("EXTREME", True, BLACK)
    screen.blit(difficulty, (220,150))
    pygame.draw.rect(screen, WHITE, (100, 200, 100, 50))
    pygame.draw.rect(screen, WHITE, (220, 200, 100, 50))
    pygame.draw.rect(screen, WHITE, (340, 200, 100, 50))
    pygame.draw.rect(screen, WHITE, (460, 200, 100, 50))
    screen.blit(easy, (130, 218))
    screen.blit(med, (245, 218))
    screen.blit(hard, (370, 218))
    screen.blit(extreme, (480, 218))
    pygame.display.update()
    easy = 0.005
    medium = 0.000005
    hard = 0.000000005
    extreme = 0

    leave = False
    while not leave:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN\
             and pygame.mouse.get_pos()[0] >= 100\
             and pygame.mouse.get_pos()[0] <= 200\
             and pygame.mouse.get_pos()[1] >= 200\
             and pygame.mouse.get_pos()[1] <= 250:
                return easy
                leave = True
            elif event.type == pygame.MOUSEBUTTONDOWN\
             and pygame.mouse.get_pos()[0] >= 220\
             and pygame.mouse.get_pos()[0] <= 320\
             and pygame.mouse.get_pos()[1] >= 200\
             and pygame.mouse.get_pos()[1] <= 250:
                return medium
                leave = True
            elif event.type == pygame.MOUSEBUTTONDOWN\
             and pygame.mouse.get_pos()[0] >= 340\
             and pygame.mouse.get_pos()[0] <= 440\
             and pygame.mouse.get_pos()[1] >= 200\
             and pygame.mouse.get_pos()[1] <= 250:
                return hard
                leave = True
            elif event.type == pygame.MOUSEBUTTONDOWN\
             and pygame.mouse.get_pos()[0] >= 460\
             and pygame.mouse.get_pos()[0] <= 560\
             and pygame.mouse.get_pos()[1] >= 200\
             and pygame.mouse.get_pos()[1] <= 250:
                return extreme
                leave = True


def display_scoreboard():
    """print the scoreboard onto the screen"""
    _score = read_scores()
    screen.fill(BLACK)
    position = 20
    for i in range(len(_score)):
        name = _score[i][0]
        score = _score[i][1]
        text = s_button.render(str(i + 1) + "." + name +' '+ str(score), True, WHITE)
        screen.blit(text, (100, position))
        position += 20
    pygame.draw.rect(screen, WHITE, (500, 400, 50, 20))
    back = s_button.render("BACK", True, BLACK)
    screen.blit(back,(507, 404))
    pygame.display.update()
                     
    leave = False
    while leave == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN\
                and pygame.mouse.get_pos()[0] >= 500\
                and pygame.mouse.get_pos()[0] <= 550\
                and pygame.mouse.get_pos()[1] >= 400\
                and pygame.mouse.get_pos()[1] <= 420:
                leave = True

def display_score(score) -> None:
    """Display the score onto the screen"""
    text = FONT.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (0,0))

def mult_play_loop(delay = 0.000005) -> None:
    """Play 1v1"""
    #Default Settings
    crashed = False

    #Initial Locations:
    slit1_x_location = random.randint(0,560)
    slit2_x_location = random.randint(0,560)
    
    ball = [random.randint(BALL_RADIUS, width-BALL_RADIUS), BALL_RADIUS + SLIT_SIZE[1]]

    #Initial movements:
    speed = [1,1]

    def draw_slit(x, y):
        """Draw the slit"""
        pygame.draw.rect(screen, WHITE, (x,y,SLIT_SIZE[0],SLIT_SIZE[1]))

    def draw_ball(x, y):
        """Draw the ball"""
        pygame.draw.circle(screen, WHITE, (x, y), BALL_RADIUS)

    def alive(y) -> bool:
        """return True iff slit and ball haven't crashed"""
        if (y + BALL_RADIUS == height) or (BALL_RADIUS == y):
            return False
        return True

    def bounce() -> bool:
        """Make the ball bounce on the slit
        Return True iff ball bounced off a slit"""
        #Bounce off bottom slit
        if (ball[0] + BALL_RADIUS) >= slit1_x_location and\
           (ball[0] - BALL_RADIUS) <= (slit1_x_location + SLIT_SIZE[0]) and\
           (ball[1] + BALL_RADIUS) == (height - SLIT_SIZE[1]) :
            speed[1] = -speed[1]
            return True
            
        #Bounce off top slit
        if (ball[0] + BALL_RADIUS) >= slit2_x_location and\
           (ball[0] - BALL_RADIUS) <= (slit2_x_location + SLIT_SIZE[0]) and\
           (ball[1]-BALL_RADIUS) == (SLIT2_Y_LOCATION + SLIT_SIZE[1]) :
            speed[1] = -speed[1]
            return True
                    
        #Bounce off left
        elif ball[0] == BALL_RADIUS:
            speed[0] = -speed[0]
            
        #Bounce off right
        elif ball[0] == (width - BALL_RADIUS):
            speed[0] = -speed[0]


    def move_ball(x, y) -> None:
        """Move the ball based on x and y values"""
        ball[0] += speed[0]
        ball[1] += speed[1]

    """update display and put it to sleep for a
    second so the user can get ready to play"""
    screen.fill(BLACK)
    draw_slit(slit1_x_location, SLIT1_Y_LOCATION)
    draw_slit(slit2_x_location, SLIT2_Y_LOCATION)
    draw_ball(ball[0], ball[1])
    pygame.display.update()
    time.sleep(1)

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        #Get move here
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if slit1_x_location > 0:
                        slit1_x_location -= 80
                        draw_slit(slit1_x_location, SLIT1_Y_LOCATION)
                elif event.key == pygame.K_RIGHT:
                    if slit1_x_location < 560:
                        slit1_x_location += 80
                        draw_slit(slit1_x_location, SLIT1_Y_LOCATION)
                if event.key == pygame.K_a:
                    if slit2_x_location > 0:
                        slit2_x_location -= 80
                        draw_slit(slit2_x_location, SLIT2_Y_LOCATION)
                elif event.key == pygame.K_d:
                    if slit2_x_location < 560:
                        slit2_x_location += 80
                        draw_slit(slit2_x_location, SLIT2_Y_LOCATION)
                    
          
        screen.fill(BLACK)
        draw_slit(slit1_x_location, SLIT1_Y_LOCATION)
        draw_slit(slit2_x_location, SLIT2_Y_LOCATION)
        draw_ball(ball[0], ball[1])
        move_ball(speed[0], speed[1])
        time.sleep(delay)
        bounce()
        pygame.display.update()

        if not alive(ball[1]):
            crashed = True
    time.sleep(0.5)
    screen.fill(BLACK)
    lose = b_button.render("GAME OVER", True, WHITE)
    screen.blit(lose, (200, 220))
    pygame.display.update()
    time.sleep(1)
    

def play_loop(delay) -> None:
    """Loop used to play the game with all the functionalities
    included within the function"""

    #Default Settings
    crashed = False
    score = 0

    #Initial Locations:
    slit_x_location = random.randint(0,560)
    ball = [random.randint(BALL_RADIUS, width-BALL_RADIUS), BALL_RADIUS]

    #Initial movements:
    speed = [1,1]

    def draw_slit(x, y = SLIT1_Y_LOCATION):
        """Draw the slit"""
        pygame.draw.rect(screen, WHITE, (x,y,SLIT_SIZE[0],SLIT_SIZE[1]))

    def draw_ball(x, y):
        """Draw the ball"""
        pygame.draw.circle(screen, WHITE, (x, y), BALL_RADIUS)

    def alive(y) -> bool:
        """return True iff slit and ball haven't crashed"""
        if y + BALL_RADIUS == height:
            return False
        return True

    def bounce() -> bool:
        """Make the ball bounce on the slit
        Return True iff ball bounced off a slit"""
        #Bounce off  slit
        if (ball[0] + BALL_RADIUS) >= slit_x_location and\
           (ball[0] - BALL_RADIUS) <= (slit_x_location + SLIT_SIZE[0]) and\
           (ball[1] + BALL_RADIUS) == (height - SLIT_SIZE[1]) :
            speed[1] = -speed[1]
            return True

        #Bounce off left
        elif ball[0] == BALL_RADIUS:
            speed[0] = -speed[0]
            
        #Bounce off right
        elif ball[0] == (width - BALL_RADIUS):
            speed[0] = -speed[0]
            
        #Bounce off top
        elif ball[1] == BALL_RADIUS:
            speed[1] = -speed[1]

    def move_ball(x, y) -> None:
        """Move the ball based on x and y values"""
        ball[0] += speed[0]
        ball[1] += speed[1]

    """update display and put it to sleep for a
    second so the user can get ready to play"""
    screen.fill(BLACK)
    draw_slit(slit_x_location)
    draw_ball(ball[0], ball[1])
    pygame.display.update()
    time.sleep(1)

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        #Get move here
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if slit_x_location > 0:
                        slit_x_location -= 80
                        draw_slit(slit_x_location)
                elif event.key == pygame.K_RIGHT:
                    if slit_x_location < 560:
                        slit_x_location += 80
                        draw_slit(slit_x_location)
          
        screen.fill(BLACK)
        draw_slit(slit_x_location)
        draw_ball(ball[0], ball[1])
        move_ball(speed[0], speed[1])
        time.sleep(delay)
        if bounce():
            score += 1
        display_score(score)
        pygame.display.update()

        if not alive(ball[1]):
            crashed = True
    if ranked(score):
        time.sleep(1)
        name = get_name()
        save_score(name, score)
            

def menu(delay) -> None:
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 90)
    greetings = font.render("WELCOME!", True, WHITE)
    screen.blit(greetings, (160,100))
    pygame.display.update()
    time.sleep(0.5)

    #Play, Settings , Scoreboard, Mult. buttons in order
    pygame.draw.rect(screen, WHITE, (160,180,120,113))
    pygame.draw.rect(screen, WHITE, (305,180,120,33))
    pygame.draw.rect(screen, WHITE, (305,220,120,33))
    pygame.draw.rect(screen, WHITE, (305,260,120,33))
    
    play_button = b_button.render("PLAY", True, BLACK)
    settings_button = s_button.render("SETTINGS", True, BLACK)
    score_button = s_button.render("SCOREBOARD", True, BLACK)
    mult_button = s_button.render("1 V 1", True, BLACK)

    screen.blit(play_button, (175, 220))
    screen.blit(settings_button, (330, 190))
    screen.blit(score_button, (320, 230))
    screen.blit(mult_button, (350, 270))
    pygame.display.update()

    leave = False
    while not leave:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leave = True
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN\
                 and pygame.mouse.get_pos()[0] >= 160\
                 and pygame.mouse.get_pos()[0] <= 280\
                 and pygame.mouse.get_pos()[1] >= 180\
                 and pygame.mouse.get_pos()[1] <= 293:
                play_loop(delay)
                while retry():
                    play_loop(delay)
                menu(delay)
            elif event.type == pygame.MOUSEBUTTONDOWN\
                 and pygame.mouse.get_pos()[0]>= 305\
                 and pygame.mouse.get_pos()[0] <= 425\
                 and pygame.mouse.get_pos()[1] >= 180\
                 and pygame.mouse.get_pos()[1] <= 213:
                delay = settings()
                menu(delay)
            elif event.type == pygame.MOUSEBUTTONDOWN\
                 and pygame.mouse.get_pos()[0]>= 305\
                 and pygame.mouse.get_pos()[0] <= 425\
                 and pygame.mouse.get_pos()[1] >= 220\
                 and pygame.mouse.get_pos()[1] <= 253:
                display_scoreboard()
                menu(delay)
            elif event.type == pygame.MOUSEBUTTONDOWN\
                 and pygame.mouse.get_pos()[0]>= 305\
                 and pygame.mouse.get_pos()[0] <= 425\
                 and pygame.mouse.get_pos()[1] >= 260\
                 and pygame.mouse.get_pos()[1] <= 293:
                mult_play_loop()
                menu(delay)

    #Add options to go into settings, scoreboard and multiplayer later

def retry() -> bool:
    """Return True iff person chooses to retry"""
    #In game Loop options
    retry_message = b_button.render("RETRY?", True, WHITE)
    yes_button = s_button.render("YES", True, BLACK)
    no_button = s_button.render("NO", True, BLACK)
    pygame.display.update()

    screen.fill(BLACK)
    screen.blit(retry_message, (240, 100))
    pygame.draw.rect(screen, WHITE, (240, 180, 50, 30))
    pygame.draw.rect(screen, WHITE, (315, 180, 50, 30))
    screen.blit(yes_button, (250, 190))
    screen.blit(no_button, (330, 190))
    pygame.display.update()
    leave = False
    while not leave:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN\
               and pygame.mouse.get_pos()[0] >= 240\
               and pygame.mouse.get_pos()[0] <= 290\
               and pygame.mouse.get_pos()[1] >= 180\
               and pygame.mouse.get_pos()[1] <= 210:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN\
               and pygame.mouse.get_pos()[0] >= 315\
               and pygame.mouse.get_pos()[0] <= 365\
               and pygame.mouse.get_pos()[1] >= 180\
               and pygame.mouse.get_pos()[1] <= 210:
                return False
                

#Run the game here
menu(delay)
