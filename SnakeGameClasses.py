import pygame, sys, random, time, os




class Snake():
    def __init__(self):
        self.default_Posn = [100, 50]
        self.def_Body = [[100, 50], [90, 50], [80, 50]]
        self.def_Direction = 'RIGHT'
        self.changeto = 'RIGHT'
        

    def draw_snake(self):
        greenColor = pygame.Color(0, 255, 0)
        for pos in self.def_Body:
            pygame.draw.rect(gameSurface, greenColor, 
            pygame.Rect(pos[0], pos[1], 10, 10))

    def getDefDirection(self):
        return self.def_Direction

    def newsnakeMovement(self, newDirection):
        self.changeto = newDirection
       
    def getSnakeMovement(self):
        return self.changeto

    def snakeMovementForwards(self, direction):
        if direction == 'RIGHT':
            self.default_Posn[0] += 10
        if direction == 'LEFT':
            self.default_Posn[0] -= 10
        if direction == 'UP':
            self.default_Posn[1] -= 10
        if direction == 'DOWN':
            self.default_Posn[1] += 10

    
      

        
    

class Food():
    def __init__(self): 
        self.foodSpawn = True
        self.foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]

    def drawFood(self):
        if self.foodSpawn == False:      
            self.foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
            self.foodSpawn = True
        colorBrown = pygame.Color(165, 42, 42)
        pygame.draw.rect(gameSurface, colorBrown, pygame.Rect(self.foodPos[0], self.foodPos[1], 10, 10))

    def getFoodPos(self):
        return self.foodPos

def importMusic(file):
    class NoSound:
        def play(self):
            pass
    if not pygame.mixer:
        return NoSound()
    fullname = os.path.join('data', file)
    try:
        song = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("cannot load or play")
        raise SystemExit
    return song

def playSong(song):
    try:
        playSong = pygame.mixer.Sound.play(song, -1)
    except pygame.error:
        print("Cannot Play")
        raise SystemExit
    return playSong

def checkErrors():
    check_errors = pygame.init()

    if check_errors[1] > 0:
        print("{0} initiliazation errors. Exiting..".format(check_errors[1]))
        sys.exit()
    else:
        print("Initialized")

def snakeMechanics(snakeClass, foodClass):
        global score
        snakeClass.def_Body.insert(0, list(snakeClass.default_Posn))
        foodX = foodClass.getFoodPos()[0]
        foodY = foodClass.getFoodPos()[1]
        
        if snakeClass.default_Posn[0] == foodX and snakeClass.default_Posn[1] == foodY:
            foodClass.foodSpawn = False   
            score += 1
        else:
            snakeClass.def_Body.pop()

        if snakeClass.default_Posn[0] > 710 or snakeClass.default_Posn[0] < 0:
            gameOver()
        if snakeClass.default_Posn[1] > 450 or snakeClass.default_Posn[1] < 0:
            gameOver()

        for block in snakeClass.def_Body[1:]:
            if snakeClass.default_Posn[0] == block[0] and snakeClass.default_Posn[1] == block[1]:
                gameOver()

def gameOver():
    red = pygame.Color(255, 0, 0)
    myFont = pygame.font.SysFont("monaco", 72)
    GameOverSurface = myFont.render("Game Over", True, red)
    GameOverRect = GameOverSurface.get_rect()
    GameOverRect.midtop = (360, 15)
    gameSurface.blit(GameOverSurface, GameOverRect)
    showScore(0)
    pygame.display.update()
    time.sleep(4) 
    pygame.quit()
    sys.exit()

def showScore(choice=1):
    black = pygame.Color(0, 0, 0)
    scoreFont = pygame.font.SysFont('monaco', 24)
    scoreSurface = scoreFont.render('Score : {0}'.format(score), True, black)
    scoreRect = scoreSurface.get_rect() 
    scoreRect.midtop = (360, 120)
    if choice == 1:
        scoreRect.midtop = (80, 10)
    else:
        scoreRect.midtop = (360, 120)
    gameSurface.blit(scoreSurface, scoreRect)
    
            

checkErrors()
gameSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption("Snake Game")
colorWhite = pygame.Color(255, 255, 255)


fpsController = pygame.time.Clock()
snakeOne = Snake()
food = Food()
score = 0
music = importMusic("house_lo.wav")

playSong(music)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                snakeOne.newsnakeMovement('RIGHT')
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                snakeOne.newsnakeMovement('LEFT')
            if event.key == pygame.K_UP or event.key == ord('w'):
                snakeOne.newsnakeMovement('UP')
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                snakeOne.newsnakeMovement('DOWN')
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if snakeOne.getSnakeMovement() == 'RIGHT' and not snakeOne.def_Direction == 'LEFT':
        snakeOne.def_Direction = 'RIGHT'
    if snakeOne.getSnakeMovement() == 'LEFT' and not snakeOne.def_Direction == 'RIGHT':
        snakeOne.def_Direction = 'LEFT'
    if snakeOne.getSnakeMovement() == 'UP' and not snakeOne.def_Direction == 'DOWN':
        snakeOne.def_Direction = 'UP' 
    if snakeOne.getSnakeMovement() == 'DOWN' and not snakeOne.def_Direction == 'UP':
        snakeOne.def_Direction = 'DOWN'
    gameSurface.fill(colorWhite)
    food.drawFood()
    snakeOne.draw_snake()
    direction = snakeOne.def_Direction
    snakeOne.snakeMovementForwards(direction)
    snakeMechanics(snakeOne, food)
    
    
    
   
  
    
    
    
    showScore()
    pygame.display.update()
    fpsController.tick(15)