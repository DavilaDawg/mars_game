# finish health bar/radiation 
# make stackable items for storage 
# make fuel leak/ critical oxigen level for hallway 
# assignable tasks for crew 
# skills for crew 
# task list 
# fix comms 
# make crew appear when population grows
# more people mean more money and ores and boosts 
# build 2 stations, then tell ground to send the next crew??
# fix mining glitch if click a lot
# add pause + leaderboard + main page 
# if Inventory full make thgs nt dIsapre
# fast forward while sleeping 
# flip hammer 
# make item being held move in the player hand 
# fix bug of placing items right when you click them in the inventory 
# animate energy coming out of solar panels 
# refactor naming convention to cammel case 
# minigames where players have to solve aero problems with tips 
# monopropelent (low thrust) for packeges, bipropelent (high thrust) for launch vehicle, Cold Gas (very low thrust) for attitude control 
# Fix health and add way to gain health 
# population and teraform info
# ensure things don't randomly spawn on top of eachother 
# change other chars to be animated too
# MODULATE
# bug: when click resume and the cave is bhind it you enter the cave 
# leaderboard 
# tile based placing system 
# bug with the energy and oreRate. when it hits zero it needs a panel to be placed to reset it even if bolts>0 
# add bolt animation to solar panel every 3 seconds 
#change the way things are swaped, i want to select the new item rather than switch them: do click and hold
# when click anywhere when in range of 

## CURRENT TASKS
# maks scrap logic 
# display minertotalenergyrequired better
# add low energy state images for miners
# rocket ship to send ore
# incoming money after send off ship 
# add shadow to things you can click when you get close to them 

# pixax hint only if havnt mined yet 
# deslect item when ging to main game to prevent placing it right away 
# add scavange scrap metals
# make fingers get bigger if within range 
# REMOVE enter cave only click to enter 
# remove unnessisary code for clickcount for fingers 
# implent gift items in payload
# add eating noise 
# Fix health and add way to gain health 

import pygame
import random
import time
import math

pygame.mixer.init()
pygame.init()

music_files = {
    "background": "./sound/background1.mp3",
    "gameover": "gameover.mp3",
    "clock3" : "clock3.mp3",
    "mine" : "./sound/mine.mp3",
}

def play_music(music_key, loop=True, volume=1):
    if music_key in music_files:
        pygame.mixer.music.load(music_files[music_key])
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
    else:
        print(f"Error: {music_key} not found in music_files.")

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Mars game")
clock = pygame.time.Clock()
dt = 0
totalTime = 0

screen_width, screen_height = screen.get_size()
bg = pygame.transform.scale(pygame.image.load("./icon/background.webp"), (screen_width, screen_height))
topRight = pygame.transform.scale(pygame.image.load("./icon/topRight.png"), (screen_width, screen_height))
topLeft = pygame.transform.scale(pygame.image.load("./icon/topLeft.png"), (screen_width, screen_height))
bottomRight = pygame.transform.scale(pygame.image.load("./icon/bottomRight.png"), (screen_width, screen_height))
bottomLeft = pygame.transform.scale(pygame.image.load("./icon/bottomLeft.png"), (screen_width, screen_height))
bg2 = pygame.transform.scale(pygame.image.load("./icon/black.png"), (screen_width, screen_height))
insideCave1 = pygame.transform.scale(pygame.image.load("./icon/cav1_.webp"), (screen_width, screen_height))
hall3 = pygame.transform.scale(pygame.image.load("./icon/hall3.jpg"), (screen_width, screen_height))
hall6 = pygame.transform.scale(pygame.image.load("./icon/hall6.jpg"), (screen_width, screen_height))
hall7 = pygame.transform.scale(pygame.image.load("./icon/hall7.webp"), (screen_width, screen_height))
bedroom = pygame.transform.scale(pygame.image.load("./icon/bedroom.jpg"), (screen_width, screen_height))
kitchen = pygame.transform.scale(pygame.image.load("./icon/k2.webp"), (screen_width, screen_height))
workshop = pygame.transform.scale(pygame.image.load('./icon/workshop.webp'), (screen_width, screen_height))
workbench1 = pygame.transform.scale(pygame.image.load('./icon/workbench1.jpg'), (screen_width, screen_height))
inPayload = pygame.transform.scale(pygame.image.load('./icon/payloadLoot.png'), (screen_width, screen_height))
pauseScreen = pygame.transform.scale(pygame.image.load('./icon/pausescreen.png'), (screen_width, screen_height))
homeScreen = pygame.transform.scale(pygame.image.load('./icon/homeScreen.png'), (screen_width, screen_height))
intro1 = pygame.transform.scale(pygame.image.load('./icon/intro1.png'), (screen_width, screen_height))
intro2 = pygame.transform.scale(pygame.image.load('./icon/intro2.png'), (screen_width, screen_height))
intro3 = pygame.transform.scale(pygame.image.load('./icon/intro3.png'), (screen_width, screen_height))
intro35 = pygame.transform.scale(pygame.image.load('./icon/intro4.png'), (screen_width, screen_height))
intro4 = pygame.transform.scale(pygame.image.load('./icon/intro5.png'), (screen_width, screen_height))
intro5c = pygame.transform.scale(pygame.image.load('./icon/intro5c.png'), (screen_width, screen_height))
intro6 = pygame.transform.scale(pygame.image.load('./icon/intro6.png'), (screen_width, screen_height))
intro7 = pygame.transform.scale(pygame.image.load('./icon/intro7.png'), (screen_width, screen_height))
intro8 = pygame.transform.scale(pygame.image.load('./icon/intro8.png'), (screen_width, screen_height))
intro9 = pygame.transform.scale(pygame.image.load('./icon/intro9.png'), (screen_width, screen_height))
intro10 = pygame.transform.scale(pygame.image.load('./icon/intro10.png'), (screen_width, screen_height))
intro11 = pygame.transform.scale(pygame.image.load('./icon/intro11.png'), (screen_width, screen_height))

tileSize = 40
playerSize = 60
cowSize= 60
farmerSize= 60

spritesheet = pygame.image.load("./icon/spriteSheet.png").convert_alpha()
spriteWidth = 25
spriteHeight = 34.7

startRowMap = 5 
spacingX= 7

spriteMap= []
for i in range(10):
    x = i* (spriteWidth+ spacingX)
    y= startRowMap * spriteHeight
    rect = pygame.Rect(x,y, spriteWidth, spriteHeight)
    sprite= spritesheet.subsurface(rect).copy()
    sprite  = pygame.transform.scale(sprite, (playerSize, playerSize))
    spriteMap.append(sprite)

startRowWalkRight = 7.3

spriteWalkRight = []
for i in range(12):  
    x = i * (spriteWidth + spacingX)
    y= startRowWalkRight * spriteHeight
    rect = pygame.Rect(x, y, spriteWidth, spriteHeight)
    sprite = spritesheet.subsurface(rect).copy()
    sprite = pygame.transform.scale(sprite, (playerSize,playerSize))
    spriteWalkRight.append(sprite)

spriteWalkLeft= [pygame.transform.flip(sprite, True, False) for sprite in spriteWalkRight] # true for flip horz false for flip virt

startRowWalkUp = 8.3

spriteWalkUp = [] 
for i in range(12):
    x = i * (spriteWidth + spacingX)
    y = startRowWalkUp*spriteHeight
    rect = pygame.Rect(x,y,spriteWidth,spriteHeight)
    sprite= spritesheet.subsurface(rect).copy()
    sprite = pygame.transform.scale(sprite, (playerSize,playerSize))
    spriteWalkUp.append(sprite)

value = 0
moving = False
frameTimer = 0
animationSpeed = 0.11  # seconds per frame 

startRowWalkDown = 9.25

spriteWalkDown = []
for i in range(12): 
    x = i * (spriteWidth + spacingX)
    y = startRowWalkDown*spriteHeight
    rect = pygame.Rect(x,y,spriteWidth,spriteHeight)
    sprite= spritesheet.subsurface(rect).copy()
    sprite = pygame.transform.scale(sprite, (playerSize,playerSize))
    spriteWalkDown.append(sprite)

startIdleDown = 3.7
idleValue = 0
spriteIdleDown = []
for i in range(10): 
    x = i * (spriteWidth + spacingX)
    y = startIdleDown*spriteHeight
    rect = pygame.Rect(x,y,spriteWidth,spriteHeight)
    sprite= spritesheet.subsurface(rect).copy()
    sprite = pygame.transform.scale(sprite, (playerSize,playerSize))
    spriteIdleDown.append(sprite)

startIdleUp = 2.7
idleValue = 0
spriteIdleUp = []
for i in range(9): 
    x = i * (spriteWidth + spacingX)
    y = startIdleUp*spriteHeight
    rect = pygame.Rect(x,y,spriteWidth,spriteHeight)
    sprite= spritesheet.subsurface(rect).copy()
    sprite = pygame.transform.scale(sprite, (playerSize,playerSize))
    spriteIdleUp.append(sprite)

startIdleRight = 1.7
idleValue = 0
spriteIdleRight = []
for i in range(10): 
    x = i * (spriteWidth + spacingX)
    y = startIdleRight*spriteHeight
    rect = pygame.Rect(x,y,spriteWidth,spriteHeight)
    sprite= spritesheet.subsurface(rect).copy()
    sprite = pygame.transform.scale(sprite, (playerSize,playerSize))
    spriteIdleRight.append(sprite)

spriteIdleLeft= [pygame.transform.flip(sprite, True, False) for sprite in spriteIdleRight]



spriteImage = spriteIdleDown
idleSprite = spriteIdleDown

if value >= len(spriteImage):
    value = 0

imageSprite = spriteImage[0]

playerImg = pygame.transform.scale(pygame.image.load('./icon/astronaut.png'), (playerSize, playerSize))
astroImg1 = pygame.transform.scale(pygame.image.load('./icon/astronaut3.png'), (cowSize, cowSize))
astroImg2 = pygame.transform.scale(pygame.image.load('./icon/astronaut2.png'), (farmerSize, farmerSize))
cave1Img = pygame.transform.smoothscale(pygame.image.load('./icon/cave.png'), (100, 100))
cave2Img = pygame.transform.smoothscale(pygame.image.load('./icon/cave2.png'), (100, 100))

numOfCows = 2
numOfFarmers = 2
numOfCaves = 1
numOfFingers = random.randint(11, 15)
xPosFinger = random.randint(0, screen_width)
yPosFinger = random.randint(0, screen_height)

parachuteLanders = []
parachute_spawn_delay = 1
next_parachute_spawn_time = 10
max_parachutes = 10

# States
game_over = False
mining = False
current_screen = "game" 
currentBackground= "topRight"
selected_slot_index = None
selected_item_from_inventory = True
item_name = None
heldItem = None
mouse_pos = None
currentInventoryItem = None
last_screen = None 
inStorage = False
inBench = False
incraftFood = False
axObtained = False
rockPresent = False
holding = False
muted = False 
paused = False
inHome = True 
inIntro1 = False 
inIntro2 = False 
inIntro3 = False 
inIntro35 = False 
inIntro4 = False 
inIntro5 = False 
inIntro6 = False 
inIntro7 = False 
inIntro8 = False 
inIntro9 = False 
inIntro10 = False 
inIntro11 = False 
skipIntro = False 
showHint = False 
itemAvailable = False
itemBuilt = False
swapAvailable = False
thrustersAttached = False
activateThrusters= False
fingerIsBigger = False

box_rects = []

minHoldTime = 750
holdStartTime = 0
crewMessage= "Hi there captain! Go to your bedroom and find your pickax in the storage bin. Time to go mining!" 
hintMessage= 'You need a pickax to mine. Go to your bedroom storage for it.'


text_color = (255, 235, 210)     # Soft white
shadow_color = (0, 0, 0)      # Black
# add these to the color array 

intro1Lines = [
    "Hey there captain!", 
    "Oh do I have some great news for you."
] 

intro2Lines = [
    "Climate deniers finally changed their minds right around",
    "the time their beachfront homes caught fire.",
    "But hey, you made it out. Welcome to Mars.",
    "We believe in science… and 12 hour shifts."
]

intro3Lines = [
    "Your first task is to get the mining system up and running.", 
    "To do that you will need to manually mine for ore then ",
    "head to the machine shop in the station."
]

intro4Lines = [
    "These mines need power!"
]


intro5Lines = [
    "You will need to build solar panels to collect energy.", 
    "Mines continuously drain your energy supply.", 
    "As you build and upgrade mines", 
    "more solar panels will be required to power them."
]

intro6Lines = [
    "It's critical that you set up a water storage system right away.", 
    "As your colony grows, water usage will increase and you will need", 
    "to expand your water storage system to survive."
]

intro7Lines = [
    "Remember your goal is to save humanity but you need money to do so."
]

intro8Lines = [
    "This is Dr. Mae Jemison.", 
    "She is here to help you out."
]

intro9Lines = [
    "Once every 2.1 years there's a launch window",
    "when Earth and Mars are aligned.",
    "The trip requires minimal fuel (Delta-v).",
]

intro10Lines = [ 
    "You can launch anytime using a slingshot maneuver", 
    "or a longer transfer arc but it requires more fuel.", 
    " ",
    "It is up to you to decide if it is worth it."
]

intro11Lines = [
    "You exchange ore for money.",
]

intro12Lines = [
    "And a lucky 30 new crew members arrive",
    "on mars to join the effort.",
    "Before they arrive you must build habitats",
    "and interview them to assign roles."
]

x_margin = 30

clock = pygame.time.Clock()
frame_count = 0
chars_per_frame = 2

def draw_typing_dialog(screen, font, lines, text_color, shadow_color, x, y, chars_per_frame, frame_count):
    current_text = []

    # Flatten all lines into one string with line breaks
    full_text = "\n".join(lines)

    # Reveal characters gradually
    visible_chars = min(frame_count * chars_per_frame, len(full_text))

    # Slice the visible text
    sliced_text = full_text[:visible_chars]

    # Split again into lines for rendering
    current_text = sliced_text.split("\n")

    BLACK_TRANSPARENT = (0, 0, 0, 100)  # 128 = 50% transparent

    temp_surface = pygame.Surface((1215, 150), pygame.SRCALPHA)
    
    # Draw rounded rectangle on the temporary surface
    pygame.draw.rect(temp_surface, BLACK_TRANSPARENT,
                     (0, 0, 1215, 150), border_radius=20)

    screen.blit(temp_surface, (25, 535))

    skipText = font.render('Click to continute', True, MARS_RED)
    screen.blit(skipText, (screen_width-290, screen_height-70))

    for line in current_text:
        shadow = font.render(line, True, shadow_color)
        text = font.render(line, True, text_color)

        screen.blit(shadow, (x + 4, y + 4))
        screen.blit(text, (x, y))
        y += 26

# not working anymore 
# def skipIntroSlides():
#     skipRect = pygame.Rect(15, 15, 110, 50)
#     pygame.draw.rect(screen, "black", skipRect, 50)
#     skipText = font.render('Skip', True, MARS_RED)
#     screen.blit(skipText, (35, 16))

#     if skipRect.collidepoint(mouse_pos) and clicked:
#         inIntro2 = False 
#         inIntro3 = False
#         inIntro4 = False
#         inIntro5 = False
#         inIntro6 = False
#         inIntro7 = False
#         inIntro8 = False
#         inIntro9 = False
#         inIntro10 = False
#         inIntro11 = False
#         paused = False

#TypeError: cannot unpack non-iterable NoneType object
# def nextSlide(current, next, mouseReleased):
#     next = next
#     mouseReleased = mouseReleased
#     print("here1")
#     if current:
#         if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
#             print("here2")
#             current = False
#             next = True
#             mouseReleased = False
#             return (current, next, mouseReleased, 0)

back_rect1= pygame.Rect(495, 620, 300, 80)
back_rect = pygame.Rect(6, 45, 100, 50)

x_offset = 150  # Move to the right
y_offset = 20  # Move down

# 255, 130, 230, 210
rect_points_basic = [ 
    (255, 113),  # Top left
    (475, 172),  # Top right
    (475, 335),  # Bottom right
    (255, 342)   # Bottom left
]

rect_points = [
    (screen_width // 2 +2 + x_offset, screen_height // 2 -2 + y_offset),  # Top left
    (screen_width // 2 + 112 + x_offset, screen_height // 2 + 2 + y_offset),  # Top right
    (screen_width // 2 + 32 + x_offset, screen_height // 2 + 55 + y_offset),  # Bottom right
    (screen_width // 2 - 130 + x_offset, screen_height // 2 + 38 + y_offset)   # Bottom left
]

x_coords = [point[0] for point in rect_points]
y_coords = [point[1] for point in rect_points]
min_x, min_y = min(x_coords), min(y_coords)
max_x, max_y = max(x_coords), max(y_coords)

font = pygame.font.Font("MODERNA.ttf", 36)
fontBig = pygame.font.Font("MODERNA.ttf", 70)
fontSmall = pygame.font.Font("MODERNA.ttf", 25)
fontSmall2 = pygame.font.Font("MODERNA.ttf", 23)

font_path = pygame.font.match_font("arial")  
font2 = pygame.font.Font(font_path, 27)

font2Small = pygame.font.Font(font_path, 18)


font3 = pygame.font.Font("Orbit.ttf", 25)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MARS_RED = (194, 59, 34) 
DUST_BROWN = (133, 94, 66) 
SANDY_YELLOW = (242, 206, 129)
SUNSET_ORANGE = (255, 140, 0)
NEON_BLUE = (0, 255, 180)        # Oxygen tank glow
NEON_GREEN = (57, 255, 20)       # Suit battery indicator
ELECTRIC_PURPLE = (191, 0, 255)  # Futuristic tools
CYBER_YELLOW = (255, 223, 0)
GOLD = (255, 215, 0)             # Rare resources
BRONZE = (205, 127, 50)          # Metals
SILVER = (192, 192, 192)         # Electronics or conduits
LAVA_RED = (255, 69, 0) 
GREEN = (0, 200, 0)
GREEN_HOVER = (0, 255, 0)

BAR_WIDTH, BAR_HEIGHT = 150, 20
healthPos = (300, 45)
HUNGER_POS = (500, 45)
THIRST_POS = (700, 45)
# ENERGY_POS= (900, 45)

health = 100
hunger = 100
thirst = 100  #city builds, increase decay for this 1
# energy = 100 
DECAY_RATE = 0.3
DECAY_RATE_THIRST = 0.4
DECAY_RATE_HEALTH = 0.1

increaseHunger = 40
increaseThirst= 5 # as 
# increaseEnergy = 30
increaseHealth = 30

# Icons 
bannana = pygame.transform.scale(pygame.image.load('./icon/bannana.png'), (40, 40))
flippedBannana = pygame.transform.flip(bannana, True, False)
badBannana = pygame.transform.scale(pygame.image.load('./icon/badBannana.png'), (40, 40))
chocolate =  pygame.transform.scale(pygame.image.load("./icon/chocolate-bar.png"), (50,50))
waffle =  pygame.transform.scale(pygame.image.load("./icon/waffle.png"), (50,50))
soy =  pygame.transform.scale(pygame.image.load("./icon/soy.png"), (50,50))
tofu =  pygame.transform.scale(pygame.image.load("./icon/tofu.png"), (50,50))
oatMilk =  pygame.transform.scale(pygame.image.load("./icon/oatMilk.png"), (50,50))
kale =  pygame.transform.scale(pygame.image.load("./icon/kale.png"), (50,50))
salad =  pygame.transform.scale(pygame.image.load("./icon/greekSalad.png"), (50,50))
flour =  pygame.transform.scale(pygame.image.load("./icon/flour.png"), (50,50))
pepper =  pygame.transform.scale(pygame.image.load("./icon/chili-pepper.png"), (50,50))
carrot =  pygame.transform.scale(pygame.image.load("./icon/carrot.png"), (50,50))
sugar =  pygame.transform.scale(pygame.image.load("./icon/sugar.png"), (50,50))
vanilla =  pygame.transform.scale(pygame.image.load("./icon/flavour.png"), (50,50))
pancakes =  pygame.transform.scale(pygame.image.load("./icon/pancakes.png"), (50,50))
tomato = pygame.transform.scale(pygame.image.load('./icon/tomato1.png'), (40,40))
tomatoTree = pygame.transform.scale(pygame.image.load('./icon/tomato.png'), (40,40))
apple = pygame.transform.scale(pygame.image.load('./icon/apple.png'), (40,40))
caramel = pygame.transform.scale(pygame.image.load('./icon/caramel.png'), (40,40))
caramelApple = pygame.transform.scale(pygame.image.load('./icon/caramel-apple.png'), (40,40))
grapes = pygame.transform.scale(pygame.image.load('./icon/apple.png'), (40,40))
finger = pygame.transform.scale(pygame.image.load('./icon/finger.png'), (60,60))
fingerBig = pygame.transform.scale(pygame.image.load('./icon/finger.png'), (100,100))
table =  pygame.transform.scale(pygame.image.load("./icon/table.png"), (100,100))
#station = pygame.transform.scale(pygame.image.load("./icon/station.png"), (110,110))
hab1 = pygame.transform.scale(pygame.image.load("./icon/hab1.png"), (350,350))
flippedpickAx= pygame.transform.scale(pygame.image.load('./icon/pickax.png'), (40,40))
pickAx = pygame.transform.flip(flippedpickAx, True, False)
message = pygame.transform.scale(pygame.image.load('./icon/message.png'), (40,40))
purpleRock = pygame.transform.scale(pygame.image.load('./icon/rock1.png'), (40,40))
iron = pygame.transform.scale(pygame.image.load('./icon/iron.png'), (40,40))
coal = pygame.transform.scale(pygame.image.load('./icon/rock2.png'), (40,40))
gold = pygame.transform.scale(pygame.image.load('./icon/rock4.png'), (40,40))
spaceFood = pygame.transform.scale(pygame.image.load('./icon/spaceFood.png'), (40,40))
hammer = pygame.transform.scale(pygame.image.load('./icon/hammer.png'), (40,40))
nail = pygame.transform.scale(pygame.image.load('./icon/nail.png'), (40,40))
bolt = pygame.transform.scale(pygame.image.load('./icon/bolt.png'), (40,40))
saw = pygame.transform.scale(pygame.image.load('./icon/saw.png'), (40,40))
thirsty = pygame.transform.scale(pygame.image.load('./icon/thirsty.png'), (30,30))
forkAndKnife= pygame.transform.scale(pygame.image.load('./icon/forkAndknife.png'), (30,30))
healthImg = pygame.transform.scale(pygame.image.load('./icon/health.png'), (30,30))
energyImg = pygame.transform.scale(pygame.image.load('./icon/energy.png'), (30,30))
volume = pygame.transform.scale(pygame.image.load('./icon/volume.png'), (35,35))
pauseGame = pygame.transform.scale(pygame.image.load('./icon/pause.png'), (35,35))
mute = pygame.transform.scale(pygame.image.load('./icon/volumeOff.png'), (35,35))
leftArrow = pygame.transform.scale(pygame.image.load('./icon/leftArrow.png'), (80,80))
rightArrow = pygame.transform.scale(pygame.image.load('./icon/rightArrow.png'), (80,80))
hoe =pygame.transform.scale(pygame.image.load('./icon/hoe.png'), (40,40))
wrench =pygame.transform.scale(pygame.image.load('./icon/wrench.png'), (40,40))
solarPanel = pygame.transform.scale(pygame.image.load('./icon/solarPanel.png'), (80,80))
oven = pygame.transform.scale(pygame.image.load('./icon/oven.png'), (110,110))
ice = pygame.transform.scale(pygame.image.load('./icon/ice.png'), (49,49))
iceMelterUnit = pygame.transform.scale(pygame.image.load('./icon/iceMelterUnit.png'), (49,49))
waterStorage = pygame.transform.scale(pygame.image.load('./icon/waterStorage.png'), (49,49))
upgradedWorkbench = pygame.transform.scale(pygame.image.load('./icon/upgradedWorkbench.png'), (49,49))
monoPropelent = pygame.transform.scale(pygame.image.load('./icon/monoPropelent.png'), (80,80))
flamingLander = pygame.transform.smoothscale(pygame.image.load('./icon/flamingLander.png'), (80,80))
lander = pygame.transform.smoothscale(pygame.image.load('./icon/lander.png'), (80,80))
parachuteLanderImage = pygame.transform.smoothscale(pygame.image.load('./icon/parachuteLander.png'), (100,130))
landerAndPayload = pygame.transform.smoothscale(pygame.image.load('./icon/landerAndPayload.png'), (80,80))
payload = pygame.transform.smoothscale(pygame.image.load('./icon/payload.png'), (70,70))
launchPad = pygame.transform.smoothscale(pygame.image.load('./icon/launchPad.png'), (300,300))
launchPadWithRocket = pygame.transform.smoothscale(pygame.image.load('./icon/launchPadWithRocket2.png'), (300,300))
expensiveHab = pygame.transform.scale(pygame.image.load('./icon/expensiveHab.png'), (80,80))
brokenCapsle = pygame.transform.smoothscale(pygame.image.load('./icon/brokenCapsle.png'), (100,100))
miner1 = pygame.transform.smoothscale(pygame.image.load('./icon/miner1.png'), (70,70))
miner2 = pygame.transform.smoothscale(pygame.image.load('./icon/miner2.png'), (60, 60))
miner3 = pygame.transform.smoothscale(pygame.image.load('./icon/miner3.png'), (220,220))
miner4 = pygame.transform.smoothscale(pygame.image.load('./icon/miner4.png'), (220,220))
miner5 = pygame.transform.smoothscale(pygame.image.load('./icon/miner5.png'), (220,220))
miner6 = pygame.transform.smoothscale(pygame.image.load('./icon/miner6.png'), (300,300))
miner1Eng = pygame.transform.smoothscale(pygame.image.load('./icon/miner1Eng.png'), (70,70))
miner2Eng = pygame.transform.smoothscale(pygame.image.load('./icon/miner1Eng.png'), (60,60))

money = pygame.transform.smoothscale(pygame.image.load('./icon/moneyIcon.png'), (40,40))
people = pygame.transform.smoothscale(pygame.image.load('./icon/peopleIcon.png'), (40,40))
clockIcon = pygame.transform.smoothscale(pygame.image.load('./icon/clockIcon.png'), (40,40))
ore = pygame.transform.smoothscale(pygame.image.load('./icon/ore.png'), (40,30))

collectible_items = {
    "game": [
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width-50),
            random.randint(0, screen_height-50)
            ),  
            "goodImage": flippedBannana, 
            "badImage": badBannana,         
            "goodName": "flippedBannana",    
            "badName": "badBannana",                                
            "collected": False,
            "bad_after": 10, 
            "hide": False         
        },
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
            ),
            "goodImage": badBannana,
            "badImage": None,         
            "goodName": "badBannana",
            "badName": None,
            "collected": False, 
            "hide": False,
        },
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
            ),
            "goodImage": chocolate,
            "badImage": None,         
            "goodName": "chocolate",
            "badName": None,
            "collected": False, 
            "hide": False, 
        }
    ],
    "insideCave1": [
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
            ),
            "goodImage": purpleRock,
            "badImage": None,         
            "goodName": "purpleRock",
            "badName": None,
            "collected": False, 
            "hide": True,
        },
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
            ),
            "goodImage": iron,
            "badImage": None,         
            "goodName": "iron",
            "badName": None,
            "collected": False, 
            "hide": True,  
        },
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
            ),
            "goodImage": gold,
            "badImage": None,         
            "goodName": "gold",
            "badName": None,
            "collected": False, 
            "hide": True, 
        },
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
            ),
            "goodImage": coal,
            "badImage": None,         
            "goodName": "coal",
            "badName": None,
            "collected": False, 
            "hide": True,  
        }
    ],
}

weights = [0.4, 0.4, 0.3, 0.2] # For ores 

item_images = {
    "flippedBannana": flippedBannana, 
    "badBannana": badBannana,
    "chocolate": chocolate,
    "pickAx": pickAx,
    "purpleRock": purpleRock,
    "iron": iron,
    "gold": gold, 
    "coal": coal, 
    "spaceFood": spaceFood,
    "solarPanel": solarPanel,
    "iceMelterUnit": iceMelterUnit,
    "waterStorage": waterStorage,
    "upgradedWorkbench": upgradedWorkbench, 
    "hammer": hammer, 
    "nail": nail, 
    "saw":saw, 
    "hoe": hoe, 
    "wrench": wrench,
    "bolt":bolt,
    "solarPanel": solarPanel, 
    "waterStorage": waterStorage,
    "miner1" : miner1,
    "miner2" : miner2,
    "miner3" : miner3,
    "miner4" : miner4,
    "miner5" : miner5,
    "miner6" : miner6,
    "miner1Eng" : miner1Eng, 
    "miner2Eng": miner2Eng, 
    "upgradedWorkbench": upgradedWorkbench,
}

food_images = {
    "flippedBannana": {
        "image": flippedBannana,
        "type": "food",
        "increase_hunger": 10
    },
    "badBannana": {
        "image": badBannana,
        "type": "food",
        "increase_hunger": 5
    },
    "chocolate": {
        "image": chocolate,
        "type": "food",
        "increase_hunger": 20
    },
    "spaceFood": {
        "image": spaceFood,
        "type": "food",
        "increase_hunger": 15
    }
}

# food_images = [
#     {"flippedBannana": flippedBannana, 
#      "increase_hunger": 20,
#      }, 
#     {"badBannana": badBannana, 
#      "increase_hunger": 5
#      },
#     {"chocolate": chocolate, 
#      "increase_hunger": 5,
#      },
#     {"spaceFood": spaceFood,
#      "increase_hunger": 40,
#      },
# ]

bench_items = [
    {"image" : hammer,
     "name": "hammer",
     "display": "Hammer",
     "materialsNeeded" : [iron],
    "materialsNeededName": ["iron"],
    # "materialsNeeded" : [iron, iron],
    # "materialsNeededName": ["iron", "iron"],
     },
    {"image": nail,
     "name": "nail",
    "display": "Nail",
    "materialsNeeded" : [iron],
    "materialsNeededName": ["iron"],
     }, 
    {"image": saw,
     "name": "saw",
    "display": "Saw",
    "materialsNeeded" : [purpleRock],
    "materialsNeededName": ["purpleRock"],
    # "materialsNeeded" : [iron, purpleRock],
    # "materialsNeededName": ["iron", "purpleRock"],
     }, 
     {"image": hoe,
     "name": "hoe",
    "display": "Hoe",
    "materialsNeeded" : [iron],
    "materialsNeededName": ["iron"],
    # "materialsNeeded" : [iron, iron],
    # "materialsNeededName": ["iron", "iron"],
    },
      {"image": wrench,
     "name": "wrench",
    "display": "Wrench", 
    "materialsNeeded" : [purpleRock],
    "materialsNeededName": ["purpleRock"],
    # "materialsNeeded" : [iron, purpleRock],
    # "materialsNeededName": ["iron", "purpleRock"],
     },
      {"image": bolt,
     "name": "bolt",
    "display": "Bolt", 
    "materialsNeeded" : [iron],
    "materialsNeededName": ["iron"],
     },
     {"image": solarPanel, 
     "name": "solarPanel",
    "display": "Solar Panel",
    "materialsNeeded" : [purpleRock, nail],
    "materialsNeededName" : ["purpleRock", "nail"],
    # "materialsNeeded" : [iron, purpleRock, hammer, nail, nail, nail],
    # "materialsNeededName" : ["iron", "purpleRock", "hammer", "nail", "nail", "nail"],
     },
      {"image": waterStorage,
     "name": "waterStorage",
     "display": "Water Pump",
    # "materialsNeeded" : [purpleRock, wrench, bolt, bolt, bolt],
    # "materialsNeededName" : ["purpleRock", "wrench", "bolt", "bolt", "bolt"],
    "materialsNeeded" : [purpleRock],
    "materialsNeededName" : ["purpleRock"],
     }, 
     {"image": miner1,
     "name": "miner1",
     "display": "Mining Rig",
    # "materialsNeeded" : [purpleRock, wrench, bolt, bolt, bolt],
    # "materialsNeededName" : ["purpleRock", "wrench", "bolt", "bolt", "bolt"],
    "materialsNeeded" : [purpleRock],
    "materialsNeededName" : ["purpleRock"],
     }, 
    {"image": upgradedWorkbench,
      "name": "upgradedWorkbench",
      "display": "Upgraded Workbench",
      "materialsNeeded" : [purpleRock],
      "materialsNeededName" : ["purpleRock"],
    #   "materialsNeeded" : [purpleRock, iron ,iron, wrench, bolt, bolt, saw, hammer, nail],
    #   "materialsNeededName" : ["purpleRock", "iron" ,"iron", "wrench", "bolt", "bolt", "saw", "hammer", "nail"],
     }, 
]

    # upgradedBench = [
    #     {
    #         "image": generator,
    #         "name": "generator", 
    #         "display": "Generator", 
    #         "meaterialsNeeded": [purpleRock],
    #     },{
    #         "image": backpack,
    #         "name": "backpack",
    #         "display": "Backpack"
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": atmosphericWaterExtractor,
    #         "name": "atmosphericWaterExtractor",
    #         "materialsNeeded" : [purpleRock, purpleRock],
    #     },{
    #         "image": automatedHarvester,
    #         "name": "Automated Harvester",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": miningDrone,
    #         "name": "Mining Drone",
    #         "materialsNeeded" : [purpleRock],
    #     ,{
    #         "image": irrigationSystem,
    #         "name": "Irrigation System",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": irrigationSystem,
    #         "name": "Irrigation System",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": PortableGenerator,
    #         "name": "Portable Generator",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": exploration Rover,
    #         "name": "Exploration Rover",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": exploration Rover,
    #         "name": "Exploration Rover",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": waterRecyclingUnit,
    #         "name": "Water Recycling Unit",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": wasteManagementSystem,
    #         "name": "Waste Management System",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": rocketLandingPad,
    #         "name": "Rocket Landng Pad",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": orbitalShuttleDock,
    #         "name": "Orbital Shuttle Dock",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": landingBeacon,
    #         "name": "Landing Beacon",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": spaceportTerminal,
    #         "name": "Spaceport Terminal",
    #         "materialsNeeded" : [purpleRock],
    #     },{
    #         "image": terraformCrafting,
    #         "name": "Terraform Crafting Staton",
    #         "materialsNeeded" : [purpleRock],
    #     },
    # ]

    # "refuelingStation":refuelingStation,
        # "habitatModule": habitatModule,

    # "passengerBridge":passengerBridge,
    # "quarantineStation": quarantineStation,
    # "customsImmigrationTerminal":customsImmigrationTerminal,
    # "employmentAssignmentDesk":employmentAssignmentDesk,
    # , 
    #   {"image": communicationAntenna,
    #  "name": "communicationAntenna",
    # "materialsNeeded" : [purpleRock],
    #  }, 
      

# terraform_images = {
#     # "climateControlUnit": climateControlUnit,
#     # "oxygenGenerator": oxygenGenerator,
#     # "atmosphericProcessor":atmosphericProcessor,
#     # "atmosphericProcessor": atmosphericProcessor,
#     # "thermalRegulator": thermalRegulator,
#     # "radiationShielding": radiationShielding,
#     # "hydrologicalCycleSimulator": hydrologicalCycleSimulator,
#     # "desalinationPlant":desalinationPlant,
#     # "oceanTemperatureRegulator":oceanTemperatureRegulator,
#     # "CO2Scrubber":CO2Scrubber,
#     # "oxygenGenerationTower": oxygenGenerationTower,
#     # "nitrogenBalancer": nitrogenBalancer,
#     # "magnetosphereGenerator":magnetosphereGenerator,
#     # "methaneReleaseUnit":methaneReleaseUnit,
#     # "pressureStabilizer":pressureStabilizer,
#     # "windPatternSimulator": windPatternSimulator,
#     # "seedDispersalDrone": seedDispersalDrone,
#     # "geneticallyModifiedTreeSeeds": geneticallyModifiedTreeSeeds,
#     # "soilEnrichmentModule": soilEnrichmentModule,
#     # "treeGrowthAccelerator":treeGrowthAccelerator,
#     # "algaeGrowthChamber": algaeGrowthChamber,
#     # "solarReflectorArray": solarReflectorArray,
#     # "terraformCommandCenter": terraformCommandCenter,
#     # "terraformCrafting": terraformCrafting
#     # "pollinatorDrone": pollinatorDrone,
#     # "marineEcosystemStarterKit": marineEcosystemStarterKit,
#     # "asteroidRedirector":asteroidRedirector,
# }

placable_item = ["solarPanel", "waterStorage","miner1","miner2","miner3","miner4", "miner5","miner6", "upgradedWorkbench"] 
placed_items = [] 
MIN_DISTANCE = 50

last_emission_times = {}
emission_interval = 3
emittedBoltsCount = 0
boltRate = 3

ore_interval = 3
last_ore_time = 0
oreCount = 0
oreRate = 0
minerTotalEnergyReq = 0

miner1Count = 0
miner2Count = 0
miner3Count = 0
miner4Count = 0
miner5Count = 0
miner6Count = 0

totalMines = miner1Count + miner2Count + miner3Count + miner4Count + miner5Count + miner6Count

miner1energyReq = 1 
miner2energyReq = 13 #2
miner3energyReq = 6
miner4energyReq = 10
miner5energyReq = 13
miner6energyReq = 15

money_count = 0

people_count = 3

def distance_between(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def check_item_collision(player_rect):
    current_items = collectible_items.get(current_screen, [])
    for item in current_items:
        if not item["collected"]:  
            item_rect = pygame.Rect(item["pos"].x, item["pos"].y, 40, 40)  
            if player_rect.colliderect(item_rect):  
                if add_to_inventory(item): 
                    item["collected"] = True  

player_pos = pygame.Vector2(screen_width / 2 - 20, screen_height/2 - 20)

farmers= [
    {
    "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
        ),
    "speed": random.randint(5, 15),
    "direction": pygame.Vector2(0, random.choice([-1, 1])),
    "time_since_last_change": 0,
    }
    for _ in range(numOfFarmers)
]

caves = [
    {
    "pos": pygame.Vector2(
             random.randint(100, screen_width),
            random.randint(0, screen_height - 200) 
        ),
    }
    for _ in range(numOfCaves)
]

fingers = [
    {
        "pos": pygame.Vector2(
                random.randint(100, screen_width),
                random.randint(0, screen_height - 200) 
        ),
        "clickCount": 0,
        "rockPresent": False,
        "rockCollected": False,
        "collected": False,
        "last_click_time": 0,
        "image": finger, 
        "bigImage": fingerBig,
        "assignedCollectible": random.choices(collectible_items["insideCave1"], weights=weights, k=1)[0],
    }
    for _ in range(numOfFingers)
]

cows = [ 
    { 
        "pos": pygame.Vector2(
            random.randint(0, screen_width - cowSize),
            random.randint(screen_height // 2, screen_height - cowSize)
        ),
        "speed": random.randint(5, 15),
        "direction": pygame.Vector2(random.choice([-1, 1]), 0),
        "selected": False,
        "captured": False,
        "time_since_last_change": 0,
        "time_since_last_jump": 0,
        "time_below": 0,
        "sound_played": False,
        "stopped": False
    }
    for _ in range(numOfCows)
]

# Inventory 
inventory_rows = 1 
inventory_cols = 8  
inventory_slot_size = 50 
inventory_margin = 15  
inventory_start_x = 410  
inventory_start_y = 630 
inventory_slots = [] 

# Storage 
storageRows = 5
storageCols = 7
storageSlotSize = 70
storageMargin= 15
storageStartX= 335
storageStartY = 120
storageSlots = []

# Craft Food 
foodRows = 3
foodCols = 3
foodSlotSize = 70
foodMargin= 15
foodStartX= 520
foodStartY = 210
foodSlots = []

# Craft items
craftRows = 1
craftCols = 5
craftSlotSize = 70
craftMargin= 15
craftStartX= 520
craftStartY = 210
craftSlots = []

benchSlots = []

# make these a function eventually: 
for row in range(inventory_rows):
    for col in range(inventory_cols):
        x = inventory_start_x + col * (inventory_slot_size + inventory_margin)
        y = inventory_start_y + row * (inventory_slot_size + inventory_margin)
        inventory_slots.append(pygame.Rect(x, y, inventory_slot_size, inventory_slot_size))

for row in range(storageRows):
    for col in range(storageCols):
        x = storageStartX + col * (storageSlotSize + storageMargin)
        y = storageStartY + row * (storageSlotSize + storageMargin)
        storageSlots.append(pygame.Rect(x, y, storageSlotSize, storageSlotSize))

for row in range(foodRows):
    for col in range(foodCols):
        x = foodStartX + col * (foodSlotSize + foodMargin)
        y = foodStartY + row * (foodSlotSize + foodMargin)
        foodSlots.append(pygame.Rect(x, y, foodSlotSize, foodSlotSize))

inventory_contents = ["pickAx", "solarPanel","purpleRock", "miner1" , "miner2" , "solarPanel", "miner5" , "solarPanel"]
# inventory_contents = [None, None,None, None , None, None, None , None]

storage_contents1 = [None] * (storageRows * storageCols)
storage_contents2 = [None] * (storageRows * storageCols)
storage_contents3 = [None] * (storageRows * storageCols)

storage_contents1[0] = "pickAx"
storage_contents1[1] = "spaceFood"
storage_contents1[2] = "spaceFood"
storage_contents1[3] = "spaceFood"
storage_contents1[4] = "spaceFood"
storage_contents1[5] = "spaceFood"
storage_contents1[6] = "spaceFood"

current_storage_contents = storage_contents1.copy()

food_contents = [None] * (foodRows * foodCols)

inventory_timestamps = [None] * len(inventory_contents)

def add_to_inventory(item):
    for i, content in enumerate(inventory_contents):
        if content is None:  # first empty slot
            if "bad_after" in item:
                if totalTime < item.get("bad_after", 0):
                    inventory_contents[i] = item["goodName"]
                    inventory_timestamps[i] = totalTime 
                else:
                    if item["badName"] is not None:
                        inventory_contents[i] = item["badName"]  
                    else: 
                        inventory_contents[i] = item["goodName"]  
            else: 
                inventory_contents[i] = item["goodName"]

            inventory_timestamps[i] = totalTime
            return True
    return False  # Inventory full

def renderItems(slots, contents, slot_size): 
    for i, slot in enumerate(slots):
        color = "gray"
        if selected_slot_index == i and not selected_item_from_inventory:
            color= "yellow"
        pygame.draw.rect(screen, color , slot, 3)
        if contents[i] is not None:  
            item_img = pygame.transform.scale(item_images[contents[i]], (slot_size, slot_size))
            screen.blit(item_img, (slot.x, slot.y))

def spawn_collectibles(current_screen):
    if current_screen not in collectible_items:
        return

    for item in collectible_items[current_screen]: 
        if not item["hide"]: # NOT WORKING
            if not item["collected"]:
                if totalTime< item.get("bad_after", 0): 
                    screen.blit(item["goodImage"], (item["pos"].x, item["pos"].y))
                elif totalTime>item.get("bad_after", 0): 
                    if item["badImage"] is not None:
                        screen.blit(item["badImage"], (item["pos"].x, item["pos"].y))
                    else: 
                        screen.blit(item["goodImage"], (item["pos"].x, item["pos"].y))

def change_background(new_background):
    global currentBackground
    if currentBackground != new_background:
        currentBackground = new_background

def makeTransparent(item, level=80):
    transItem = pygame.transform.scale(pygame.image.load(f'./icon/{item}.png'), (40,40)).convert_alpha()
    transItem.set_alpha(level)

current_item_index = 0

def showCraftableItems():
    global current_item_index, box_rects, itemRectClicked, selected_slot_index, itemBuilt, itemAvailable, bench_contents, swapAvailable
    box_rects = []
    itemData = bench_items[current_item_index]
    itemImg = itemData["image"]
    itemName = itemData["name"]
    displayName= itemData["display"]
    itemText = font.render(displayName, True, (255, 255, 255)) 
    textWidth, textHeight = font.size(displayName)
    arrowSpace = (screen_width / 2 + 132) - (screen_width / 2 - 211)

    if textWidth > arrowSpace:
        words = displayName.split()
        if len(words) > 1:
            first_line = words[0]
            second_line = " ".join(words[1:])
            
            first_line_text = font.render(first_line, True, (255, 255, 255))
            second_line_text = font.render(second_line, True, (255, 255, 255))
            
            first_line_width1, _ = font.size(first_line)
            second_line_width1, _ = font.size(second_line)

            if first_line_width1 <= arrowSpace and second_line_width1 <= arrowSpace:
                # First line has 1 word then the rest on second
                second_line_text = fontSmall2.render(second_line, True, (255, 255, 255))
                second_line_width1, _ = fontSmall2.size(second_line)

                first_line_x = screen_width / 2 - first_line_width1 / 2
                second_line_x = screen_width / 2 - second_line_width1 / 2
                
                first_line_y = 185
                second_line_y = 220 + textHeight - 50
            
                screen.blit(first_line_text, (first_line_x, first_line_y))
                screen.blit(second_line_text, (second_line_x, second_line_y))
            else:
                first_line = " ".join(words[:2])
                second_line = " ".join(words[2:])

                first_line_text = font.render(first_line, True, (255, 255, 255))
                second_line_text = font.render(second_line, True, (255, 255, 255))
            
                first_line_width, _ = font.size(first_line)
                second_line_width, _ = font.size(second_line)

                first_line_y = 193
                second_line_y = 213 + textHeight - 45

                if first_line_width <= arrowSpace and second_line_width <= arrowSpace:
                    # first line has two words then the rest on the second 
                    first_line_x = screen_width / 2 - first_line_width / 2
                    second_line_x = screen_width / 2 - second_line_width / 2
                
                    screen.blit(first_line_text, (first_line_x, first_line_y))
                    screen.blit(second_line_text, (second_line_x, second_line_y))
                else:
                    first_line_text = fontSmall.render(first_line, True, (255, 255, 255))
                    second_line_text = fontSmall.render(second_line, True, (255, 255, 255))

                    first_line_width, _ = fontSmall.size(first_line) 
                    second_line_width, _ = fontSmall.size(second_line) 

                    first_line_x = screen_width / 2 - first_line_width / 2
                    second_line_x = screen_width / 2 - second_line_width / 2

                    screen.blit(first_line_text, (first_line_x, first_line_y))
                    screen.blit(second_line_text, (second_line_x, second_line_y))
        else:
            # Single-word but smaller
            itemText = fontSmall.render(displayName, True, (255, 255, 255))
            text_x = screen_width / 2 - 130
            screen.blit(itemText, (text_x, 201))
    else:
        # fits as is 
        text_x = screen_width / 2 - textWidth / 2
        screen.blit(itemText, (text_x, 201))

    transItem = pygame.transform.scale(pygame.image.load(f'./icon/{itemName}.png'), (80,80)).convert_alpha()
    transItem.set_alpha(90)
    itemRect = pygame.Rect(screen_width/2 - 45 , screen_height/2 + 76, 90, 90)
    leftRect = pygame.Rect(screen_width/2 - 210, 185, 90, 90)
    rightRect = pygame.Rect(screen_width/2 + 132, 185, 90, 90)

    screen.blit(leftArrow, (screen_width/2 - 211, 185)) 
    screen.blit(rightArrow, (screen_width/2 + 132, 185)) 
    screen.blit(transItem, (screen_width/2 -40, screen_height/2 + 80))    

    materials = itemData["materialsNeeded"]
    materialsNeededName = itemData["materialsNeededName"]
    material_box_width, material_box_height = 55, 55
    gap = 15

    total_width = len(materials) * (material_box_width + gap) - gap
    start_x = (screen_width - total_width) // 2
    start_y = 285

    for i, material in enumerate(materials):
        transMat = material.convert_alpha()
        transMat.set_alpha(90)
        box_x = start_x + i * (material_box_width + gap)
        box_rect = pygame.Rect(box_x, start_y, material_box_width, material_box_height)
        box_rects.append(box_rect)
        pygame.draw.rect(screen, (24, 116, 205),box_rect, 3)
        screen.blit(transMat, (box_x + gap - 8 , start_y + 6)) 
        
        for j, content in enumerate(bench_contents): 
            if content is not None:
                for k, materialNeededName in enumerate(materialsNeededName):
                    if content == materialNeededName:
                        swapAvailable = True
                        box_x = start_x + j * (material_box_width + gap)
                        screen.blit(materials[k], (box_x + gap - 8 , start_y + 6))
                        if None not in bench_contents: 
                            itemAvailable = True
                    else: 
                        itemAvailable = False
        
    if None not in bench_contents: 
        item = pygame.transform.scale(pygame.image.load(f'./icon/{itemName}.png'), (80,80))
        if itemAvailable: 
            screen.blit(item, (screen_width/2 -40, screen_height/2 + 80)) 
        if itemRectClicked and itemAvailable: 
            pygame.draw.rect(screen,YELLOW,itemRect, 3)  
            for i, slot in enumerate(inventory_slots):
                if slot.collidepoint(mouse_pos) and clicked: 
                    if selected_slot_index is None and inventory_contents[i] is None:
                        selected_slot_index = i 
                        inventory_contents[i]= itemName 
                        itemAvailable= False 
                        itemBuilt = True  
        else:
            pygame.draw.rect(screen,(24, 116, 205),itemRect, 3)     
    else:
        screen.blit(transItem, (screen_width/2 -40, screen_height/2 + 80))
        itemAvailable= False        
        itemRectClicked = False
        itemBuilt = False 
        pygame.draw.rect(screen,(24, 116, 205),itemRect, 3)

    if leftRect.collidepoint(mouse_pos) and clicked: 
        current_item_index = (current_item_index - 1) % len(bench_items) # index wraps around if it goes below 0
    elif rightRect.collidepoint(mouse_pos) and clicked:
        current_item_index = (current_item_index + 1) % len(bench_items)

    if itemRect.collidepoint(mouse_pos) and itemAvailable and clicked: 
        itemRectClicked = not itemRectClicked   

    if itemBuilt:
        bench_contents = [None] * len(materials)

play_music("background", loop=True, volume=2)

mutedRec = pygame.Rect(screen_width-100, 10 , 50, 50)

if muted:
    pygame.mixer.music.stop()  

######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################

running = True 
last_update_time = time.time()
while running: 
    dt = clock.tick(60) / 1000
    totalTime += dt 
    player_rect = pygame.Rect(player_pos.x, player_pos.y, playerSize, playerSize)
    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    current_time = time.time()

    if not paused and inHome != True: 
        if current_time - last_update_time >= 1: 
            hunger = max(0, hunger - DECAY_RATE) # Compares the result of hunger - DECAY_RATE with 0 and returns the greater of the two
            thirst = max(0, thirst - DECAY_RATE_THIRST)
            # energy = max(0, energy - DECAY_RATE)
            last_update_time = current_time

        if hunger == 0 or thirst == 0: 
            health = max(0, health-DECAY_RATE_HEALTH)
            last_update_time = current_time

        # FIX!!!!!!!!!
        if hunger != 0 and thirst != 0 and health != 100:
            if current_time - last_update_time >= 0.5: 
                heath = min(health+DECAY_RATE_HEALTH, 100)
                #print(health)
        if health == 0: 
            game_over = True

    if health == 0: 
        game_over = True

    if not paused and inHome != True: 
        if emittedBoltsCount > minerTotalEnergyReq: 
            oreRate = (
                    (miner1Count * 0.1) +
                    (miner2Count * 0.5) +
                    (miner3Count * 1) +
                    (miner4Count * 5) +
                    (miner5Count * 10) +
                    (miner6Count * 30)
                )
        minerTotalEnergyReq = (miner1energyReq * miner1Count) + (miner2energyReq * miner2Count) + (miner3energyReq * miner3Count) + (miner4energyReq * miner4Count) + (miner5energyReq * miner5Count) + (miner6energyReq * miner6Count)
        # print("required: ", minerTotalEnergyReq)

        if emittedBoltsCount > 0 and oreRate != 0: 
            if current_time - last_ore_time >= ore_interval:
                oreCount += oreRate
                emittedBoltsCount -= minerTotalEnergyReq 
                # emittedBoltsCount = max(0, emittedBoltsCount - minerTotalEnergyReq) # this didn't fix it cause it will go 3 then 0 then back to 3
                last_ore_time = current_time
        if emittedBoltsCount <= 0:  
            oreRate = 0
            emittedBoltsCount = 0 # i think this is causing bug. when i place solar pannel it makes bolt count 0. but without it it would go negeitv :(
        # if emittedBoltsCount > minerTotalEnergyReq: 
        #     oreRate = (
        #             (miner1Count * 0.1) +
        #             (miner2Count * 0.5) +
        #             (miner3Count * 1) +
        #             (miner4Count * 5) +
        #             (miner5Count * 10) +
        #             (miner6Count * 30)
        #         )
        # if emittedBoltsCount > minerTotalEnergyReq: 
        #     orerate = oreRateCopy

    for item in placed_items:
        last_emission_time = last_emission_times.get(item["position"], 0) # this makes no sense !!!!!!!!!

        itemName = item['item']

        if not paused and inHome != True: 
            if item["isAdded"] == False and emittedBoltsCount > 0:
                if itemName == 'miner1':
                    miner1Count += 1
                if itemName == 'miner2':
                    miner2Count += 1
                if itemName == 'miner3':
                    miner3Count += 1
                if itemName == 'miner4':
                    miner4Count += 1
                if itemName == 'miner5':
                    miner5Count += 1
                if itemName == 'miner6':
                    miner6Count += 1
                item["isAdded"] = True 

            if item["item"] == "solarPanel":
                if current_time - last_emission_time >= emission_interval:
                    emittedBoltsCount += boltRate 
                    last_emission_times[item["position"]] = current_time

            if item["item"] == "waterStorage":
                if current_time - last_emission_time >= emission_interval:
                    if 100 >= thirst + increaseThirst:
                        thirst += increaseThirst
                        last_emission_times[item["position"]] = current_time
                    else: 
                        thirst = 100
                        last_emission_times[item["position"]] = current_time

    if current_screen == "storage1":
        current_storage_contents = storage_contents1
    elif current_screen == "storage2":
        current_storage_contents = storage_contents2
    elif current_screen == "storage3":
        current_storage_contents = storage_contents3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
                moving = False
                value = 0
            if event.key == pygame.K_ESCAPE:
                current_screen = last_screen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True 
            if event.button == 1:
                holding = True
                holdStartTime = pygame.time.get_ticks()

                is_valid_position = True
                if current_screen == "game": 
                    if heldItem and heldItem in item_images:
                        image = item_images[heldItem] 
                        image_width, image_height = image.get_size() 
                        centered_pos = (mouse_pos[0] - image_width // 2, mouse_pos[1] - image_height // 2)

                        items_on_current_bg = [item for item in placed_items if item["background"] == currentBackground]

                        for item in items_on_current_bg:
                            if distance_between(centered_pos, item["position"]) < MIN_DISTANCE:
                                centered_pos = (centered_pos[0] + 40, centered_pos[1] + 40)
                        
                        for item in items_on_current_bg:
                            if distance_between(centered_pos, item["position"]) < MIN_DISTANCE:
                                is_valid_position = False
                                break

                        if is_valid_position and heldItem in placable_item:
                            # if heldItem == "miner2": 
                            #     if emittedBoltsCount > minerTotalEnergyReq:  # or if orerate > 0
                            #         heldItem == "miner2Eng"
                            #         print("HIIIIII: ", heldItem)
                            placed_items.append({
                                "background": currentBackground, 
                                "position": centered_pos, 
                                "item": heldItem, 
                                "isAdded" : False,
                            })
                        if heldItem in inventory_contents and heldItem in placable_item:
                            item_index = inventory_contents.index(heldItem) 
                            inventory_contents[item_index] = None  
                            heldItem = None
                            selected_slot_index= None
                            currentInventoryItem = None

            if back_rect.collidepoint(mouse_pos):
                if last_screen == "game": 
                    showHint = False
                if current_screen == "game": 
                    if not muted:
                        play_music("background", loop=True, volume=2)
 
            for i, slot in enumerate(inventory_slots):
                if slot.collidepoint(mouse_pos): 
                    if selected_slot_index is None and inventory_contents[i] is not None:
                        selected_slot_index = i 
                        selected_item_from_inventory = True
                        currentInventoryItem= item_images[inventory_contents[i]]
                    else:
                        if inventory_contents[i] is None and selected_slot_index is not None: 
                            if selected_item_from_inventory and inventory_contents[selected_slot_index] is not None: 
                                inventory_contents[i]= inventory_contents[selected_slot_index]
                                inventory_contents[selected_slot_index]= None
                            elif inStorage: # storage to inventory 
                                if inStorage and selected_slot_index is not None and current_storage_contents[selected_slot_index] is not None:
                                    inventory_contents[i]= current_storage_contents[selected_slot_index]
                                    if not selected_item_from_inventory:
                                        current_storage_contents[selected_slot_index] = None
                                if incraftFood and selected_slot_index is not None and food_contents[selected_slot_index]: 
                                    inventory_contents[i]= food_contents[selected_slot_index]
                                    if not selected_item_from_inventory:
                                        food_contents[selected_slot_index] = None
                            selected_slot_index = None
                        elif inventory_contents[i] is not None and selected_slot_index is not None: 
                            if not selected_item_from_inventory and current_storage_contents[selected_slot_index] is not None:
                                # Swap from storage to inventory
                                if inStorage: 
                                    inventory_contents[i], current_storage_contents[selected_slot_index] = (
                                        current_storage_contents[selected_slot_index],
                                        inventory_contents[i],
                                    )
                            else:                   
                                # swap/deselect within inventory      
                                inventory_contents[i], inventory_contents[selected_slot_index] =(
                                inventory_contents[selected_slot_index],
                                inventory_contents[i]
                            )
                        selected_slot_index = None 
                        currentInventoryItem = None
                        selected_item_from_inventory = False
                    break
            if inStorage:
                for i, slot in enumerate(storageSlots):
                    if slot.collidepoint(mouse_pos):   
                        if selected_slot_index is None and current_storage_contents[i] is not None:
                            selected_slot_index = i   
                            selected_item_from_inventory = False
                            if current_storage_contents[selected_slot_index] == "pickAx": 
                                axObtained = True
                        else:
                            if current_storage_contents[i] is None and selected_slot_index is not None:
                                if selected_item_from_inventory and inventory_contents[selected_slot_index] is not None: # Inventory to storage
                                    current_storage_contents[i] = inventory_contents[selected_slot_index]
                                    inventory_contents[selected_slot_index] = None
                                elif not selected_item_from_inventory and current_storage_contents[selected_slot_index] is not None:  # Swap from storage to inventory
                                    current_storage_contents[i]= current_storage_contents[selected_slot_index]
                                    current_storage_contents[selected_slot_index]= None
                            else:
                                if selected_item_from_inventory and selected_slot_index is not None and inventory_contents[selected_slot_index] is not None: # swap from inventory to storage
                                    inventory_contents[selected_slot_index], current_storage_contents[i] = (
                                        current_storage_contents[i],
                                        inventory_contents[selected_slot_index],
                                    )
                                elif selected_slot_index is not None and current_storage_contents[selected_slot_index] is not None: # swap within storage
                                    current_storage_contents[selected_slot_index], current_storage_contents[i] = (
                                        current_storage_contents[i],
                                        current_storage_contents[selected_slot_index],
                                    )
                            selected_slot_index = None
                        break  
            if incraftFood: # doesnt work
                for i, slot in enumerate(foodSlots):
                    if slot.collidepoint(mouse_pos):  
                        if food_contents[i] is not None:
                            if selected_slot_index is None:
                                selected_slot_index = i
                                selected_item_from_inventory = False
                            else:
                                if food_contents[i] is None:  # Empty slot
                                    if selected_item_from_inventory: # Inventory to storage
                                        food_contents[i] = inventory_contents[selected_slot_index]
                                        inventory_contents[selected_slot_index] = None
                                    else: # move within storage
                                        food_contents[i] = food_contents[selected_slot_index]
                                        food_contents[selected_slot_index] = None
                                else: # Swap items if target slot is not empty
                                    if selected_item_from_inventory:
                                        inventory_contents[selected_slot_index], food_contents[i] = (
                                            food_contents[i],
                                            inventory_contents[selected_slot_index],
                                        )
                                    else:
                                        food_contents[selected_slot_index], food_contents[i] = (
                                            food_contents[i],
                                            food_contents[selected_slot_index],
                                        )
                                selected_slot_index = None
                            break   
            if inBench:
                itemData = bench_items[current_item_index]
                materialsNeededName = itemData["materialsNeededName"]
                for i, slot in enumerate(box_rects):
                        if slot.collidepoint(mouse_pos):  
                            if selected_slot_index is None and bench_contents[i] is not None:
                                selected_slot_index = i
                                selected_item_from_inventory = False
                            else:
                                swapAvailable = False
                                if bench_contents[i] is None and selected_slot_index is not None:
                                    if selected_item_from_inventory and inventory_contents[selected_slot_index] is not None:
                                        # Check if the inventory item matches the required material
                                        if inventory_contents[selected_slot_index] == materialsNeededName[i]:
                                            swapAvailable = True
                                        else:
                                            print("Invalid Swap: Inventory item doesn't match material needed.")
                                    elif not selected_item_from_inventory and bench_contents[selected_slot_index] is not None:
                                        # Bench to bench swap is always allowed (adjust this if needed)
                                        swapAvailable = True
                                
                                # Perform Swap Only If swapAvailable is True
                                if swapAvailable:
                                    if selected_item_from_inventory and inventory_contents[selected_slot_index] is not None:
                                        bench_contents[i] = inventory_contents[selected_slot_index]
                                        inventory_contents[selected_slot_index] = None
                                    elif not selected_item_from_inventory and bench_contents[selected_slot_index] is not None:
                                        bench_contents[i] = bench_contents[selected_slot_index]
                                        bench_contents[selected_slot_index] = None
                                else:
                                    print("Swap Denied")

                                selected_slot_index = None
                            break 

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                holding = False
                hold_duration = pygame.time.get_ticks() - holdStartTime 
                if hold_duration >= minHoldTime:
                    if heldItem in food_images:
                        if 100 >= hunger + increaseHunger:
                            hunger += increaseHunger
                        else: 
                            hunger = 100
                        item_index = inventory_contents.index(heldItem) 
                        inventory_contents[item_index] = None  
                        heldItem = None
                        currentInventoryItem = None 
                        selected_slot_index= None
                        currentInventoryItem = None

    if current_screen == "game":     
        if currentBackground == "topRight":
            screen.blit(topRight, (0,0))
            if player_rect.left == 0:  
                change_background("topLeft")
                player_pos.x = screen_width - playerSize
            elif player_rect.bottom >= screen_height:  
                change_background("bottomRight")
                player_pos.y = 35

        elif currentBackground == "topLeft":
            if player_rect.right >= screen_width: 
                change_background("topRight")
                player_pos.x = 0
            elif player_rect.bottom >= screen_height:  
                change_background("bottomLeft")
                player_pos.y = 35

        elif currentBackground == "bottomRight":
            if player_rect.left == 0:  
                change_background("bottomLeft")
                player_pos.x = screen_width - playerSize
            elif player_rect.top == 35: 
                change_background("topRight")
                player_pos.y = screen_height - playerSize

        elif currentBackground == "bottomLeft":
            if player_rect.right >= screen_width:  
                change_background("bottomRight")
                player_pos.x = 0
            elif player_rect.top == 35: 
                change_background("topLeft")
                player_pos.y = screen_height - playerSize

        if currentBackground == "topRight":
            screen.blit(topRight, (0,0))
        elif currentBackground == "topLeft":
            screen.blit(topLeft, (0,0))
        elif currentBackground == "bottomRight":
            screen.blit(bottomRight, (0,0))
        elif currentBackground == "bottomLeft":
            screen.blit(bottomLeft, (0,0))

    check_item_collision(player_rect)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 215 * dt
        moving = True
        idleValue=0
        idleSprite = spriteIdleLeft
        spriteImage = spriteWalkLeft
    if keys[pygame.K_d]:
        player_pos.x += 215 * dt
        moving =True
        idleValue=0
        idleSprite = spriteIdleRight
        spriteImage = spriteWalkRight
    if keys[pygame.K_w]:
        player_pos.y -= 215 * dt
        moving = True 
        idleValue= 0
        idleSprite = spriteIdleUp 
        spriteImage = spriteWalkUp
    if keys[pygame.K_s]:
        player_pos.y += 215 * dt
        moving= True
        idleValue = 0 
        idleSprite = spriteIdleDown 
        spriteImage= spriteWalkDown 

    frameTimer += dt

    if moving:
        if frameTimer >= animationSpeed:
            frameTimer = 0
            value += 1
        imageSprite = spriteImage[value % len(spriteImage)]
    else:
        value = 0
        if frameTimer >= animationSpeed:
            frameTimer = 0
            idleValue = (idleValue + 1) % len(idleSprite)
        imageSprite = idleSprite[idleValue]

    # player bounds
    player_pos.x = max(0, min(player_pos.x, screen_width - playerSize))
    player_pos.y = max(35, min(player_pos.y, screen_height - playerSize))

    if not paused and inHome != True: 
        if totalTime >= next_parachute_spawn_time and len(parachuteLanders) < max_parachutes:
            parachuteLanders.append({
                "pos": pygame.Vector2(random.randint(0, screen_width), 0),
                "speed": random.randint(70, 90),
                "direction": pygame.Vector2(0, 1),
                "crashed": False,
                "activateThrusters": False,
                "landed": False,
                "collectedLoot": False,
                "spawnTime": totalTime,
                "rockPresent": False,
                "rockCollected": False,
                "collected": False,
                "assignedCollectible": random.choices(collectible_items["insideCave1"], weights=weights, k=1)[0],
            })
            next_parachute_spawn_time += random.choice([3, 5, 30, 60, 120])

    if current_screen == "game":       
        for parachuteLander in parachuteLanders:
            time_alive = totalTime - parachuteLander["spawnTime"]

            if parachuteLander["crashed"] == False and parachuteLander["landed"] == False: 
                parachuteLander["pos"] += parachuteLander["direction"] * parachuteLander["speed"] * dt
            if parachuteLander["pos"].y >= screen_height - 115:
                parachuteLander["crashed"] = True 

            parachuteLander_rect = pygame.Rect(parachuteLander["pos"].x, parachuteLander["pos"].y, 100, 130)
            
            if parachuteLander["activateThrusters"] == False and time_alive < 6: # thrusters attached must be in state array 
                screen.blit(parachuteLanderImage, (parachuteLander["pos"].x,parachuteLander["pos"].y)) # not in front of plaYER???
                if clicked and parachuteLander_rect.collidepoint(mouse_pos):
                    parachuteLander["activateThrusters"] = True 
                    parachuteLander["speed"] = random.randint(15,40)
            elif parachuteLander["activateThrusters"] == True and time_alive > 6 and parachuteLander["collectedLoot"] == False: 
                parachuteLander["landed"] = True 
                screen.blit(payload, (parachuteLander["pos"].x, parachuteLander["pos"].y + 27))
            elif parachuteLander["activateThrusters"] and parachuteLander["crashed"] == False and parachuteLander["collectedLoot"] == False: 
                screen.blit(landerAndPayload, (parachuteLander["pos"].x,parachuteLander["pos"].y + 40))
            elif parachuteLander["activateThrusters"] == False and totalTime > 4: 
                parachuteLander["crashed"] = True 
                screen.blit(brokenCapsle, (parachuteLander["pos"].x, parachuteLander["pos"].y + 27))
            elif parachuteLander["crashed"] == True: 
                screen.blit(brokenCapsle, (parachuteLander["pos"].x, parachuteLander["pos"].y + 20)) 

            if parachuteLander["landed"] and parachuteLander["collectedLoot"] == False: 
                if clicked and parachuteLander_rect.collidepoint(mouse_pos):
                    if parachuteLander_rect.colliderect(player_rect): 
                        current_screen = "inPayload"
                        parachuteLander["collectedLoot"] = True
            if parachuteLander["crashed"] == True and parachuteLander["collectedLoot"] == False:
                if parachuteLander_rect.collidepoint(mouse_pos):
                    if parachuteLander_rect.colliderect(player_rect): 
                        print("in range")
                        if clicked: 
                            print("clicked")
                            parachuteLander["rockPresent"] = True  

                if parachuteLander["rockPresent"] and not parachuteLander["rockCollected"]: 
                    collectible = parachuteLander["assignedCollectible"]
                    if collectible:
                        screen.blit(collectible["goodImage"], (parachuteLander["pos"].x, parachuteLander["pos"].y))
                    else:
                        screen.blit(purpleRock, (parachuteLander["pos"].x, parachuteLander["pos"].y))
                

        screen.blit(imageSprite, (player_pos.x,player_pos.y))

        if currentBackground == "topRight":
            screen.blit(hab1, (screen_width-400, 5))

            for farmer in farmers:
                # Wandering 
                farmer["time_since_last_change"] += dt
                if farmer["time_since_last_change"] >= 6:
                    farmer["direction"] = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
                    farmer["time_since_last_change"] = 0

                farmer["pos"] += farmer["direction"] * farmer["speed"] * dt
                farmer["direction"].x *= -1
                if farmer["pos"].y <= 0 or farmer["pos"].y >= screen_height - farmerSize:
                    farmer["direction"].y *= -1

                screen.blit(astroImg1, (farmer["pos"].x, farmer["pos"].y))
            
                farmer_rect = pygame.Rect(farmer["pos"].x, farmer["pos"].y, farmerSize, farmerSize)
            
            for cave in caves:
                screen.blit(cave1Img, (cave["pos"].x, cave["pos"].y))
                cave_rect = pygame.Rect(cave["pos"].x, cave["pos"].y, 100, 100)
            
                if player_rect.colliderect(cave_rect):  
                    mining = True 
                    if cave_rect.collidepoint(mouse_pos) and clicked:
                        current_screen = "insideCave1"  
                        if not muted:
                            play_music("mine", loop=True, volume=3)

            enter_station_rect = pygame.Rect(screen_width-400, 55, 230, 60)  
            stationRect = pygame.Rect(screen_width-350, 150, 100,100)
            stationText = font.render('Enter station', True, (100, 100, 50)) #remove
            screen.blit(imageSprite, (player_pos.x, player_pos.y)) 

            # cows logic
            if not paused and inHome != True: 
                for i, cow in enumerate(cows):
                    if not cow["stopped"] or axObtained:
                        cow["time_since_last_change"] += dt
                        if cow["time_since_last_change"] >= 2: 
                            cow["direction"] = pygame.Vector2(
                                random.choice([-1, 1]),
                                random.choice([-1, 1])
                            )
                            cow["time_since_last_change"] = 0

                        cow["pos"] += cow["direction"] * cow["speed"] * dt

                        # Reverse direction if hitting a wall
                        if cow["pos"].x <= 0 or cow["pos"].x >= screen_width - cowSize:
                            cow["direction"].x *= -1
                        if cow["pos"].y <= 0 or cow["pos"].y >= screen_height - cowSize:
                            cow["direction"].y *= -1

                    screen.blit(astroImg2, (cow["pos"].x, cow["pos"].y))
                    
                    if i == len(cows) - 1: 
                        if not axObtained: 
                            cowRect = pygame.Rect(cow["pos"].x -40 , cow["pos"].y -40 , cowSize+20, cowSize+20)
                            screen.blit(message, (cow["pos"].x +50, cow["pos"].y - 30))  
                            if cowRect.collidepoint(player_pos): 
                                cow["stopped"] = True
                                crewText = fontSmall.render(crewMessage, True, (100, 100, 50)) 
                                pygame.draw.rect(screen, "black", (20, 350, screen_width-40, 60), 50)
                                screen.blit(crewText, (45, screen_height/2 +3)) 

        if player_rect.colliderect(stationRect):  
            if enter_station_rect.collidepoint(mouse_pos) and clicked:
                current_screen = "hall3"  

        for item in placed_items:
            if item["background"] == currentBackground:
                image = item_images[item["item"]]
                screen.blit(image, item["position"])

    if currentInventoryItem and heldItem in inventory_contents: 
        smaller_item = pygame.transform.scale(currentInventoryItem, (30, 30))
        screen.blit(smaller_item,(player_pos.x-7, player_pos.y+30))

    if current_screen == "hall3":
        last_screen = "game"
        screen.blit(hall3, (0, 0))
        firstDoorRec = pygame.Rect((screen_width / 2) - 70, (screen_height / 2) - 70, 160, 150)
        pygame.draw.rect(screen, (200, 0, 0), firstDoorRec, 3) 
        if clicked and firstDoorRec.collidepoint(mouse_pos):
            current_screen = "hall6"

    if current_screen == "hall6": 
        screen.blit(hall6, (0, 0))
        last_screen = "hall3"
        secondDoorRec = pygame.Rect((screen_width / 4) - 30, (screen_height / 3)+40 , 70, 120)
        pygame.draw.rect(screen, (200, 0, 0), secondDoorRec, 3) 
        if clicked and secondDoorRec.collidepoint(mouse_pos):
            current_screen = "hall7"

    if current_screen == "hall7": 
        last_screen = "hall6"
        screen.blit(hall7, (0, 0))
        bedDoorRec = pygame.Rect(125, 280 , 65, 65)
        pygame.draw.circle(screen, (255, 0, 0), (155, 315), 35, 3)
        kitchenDoorRec= pygame.Rect(screen_width-73, 275 , 70, 70)
        pygame.draw.circle(screen, (255, 0, 0), (screen_width-40, 310), 37, 3)
        workshopDoorRec = pygame.Rect(420, 350 , 20, 40)
        pygame.draw.rect(screen, (200, 0, 0), workshopDoorRec, 3) 
        if clicked and bedDoorRec.collidepoint(mouse_pos):
            current_screen = "bedroom"
        if clicked and kitchenDoorRec.collidepoint(mouse_pos):
            current_screen = "kitchen"
        if clicked and workshopDoorRec.collidepoint(mouse_pos): 
            current_screen = "workshop"
        
    if current_screen == "bedroom": 
        inStorage = False
        last_screen="hall7"
        screen.blit(bedroom, (0,0))
        storageDoorRec1 = pygame.Rect(86, 110 , 15, 45)
        pygame.draw.rect(screen, (255, 0, 0), storageDoorRec1, 2)
        if clicked and storageDoorRec1.collidepoint(mouse_pos):
            current_screen = "storage1"
        storageDoorRec2 = pygame.Rect(93, 286 , 15, 45)
        pygame.draw.rect(screen, (255, 0, 0), storageDoorRec2, 2)
        if clicked and storageDoorRec2.collidepoint(mouse_pos):
            current_screen = "storage2"
        storageDoorRec3 = pygame.Rect(103, 455 , 15, 45)
        pygame.draw.rect(screen, (255, 0, 0), storageDoorRec3, 2)
        if clicked and storageDoorRec3.collidepoint(mouse_pos):
            current_screen = "storage3"

    if current_screen == "storage1":    
        inStorage = True
        screen.blit(bg2, (0,0))
        last_screen="bedroom"
        renderItems(storageSlots, current_storage_contents, storageSlotSize)
        
    if current_screen == "storage2":    
        inStorage = True
        screen.blit(bg2, (0,0))
        last_screen="bedroom"
        renderItems(storageSlots, current_storage_contents, storageSlotSize)

    if current_screen == "storage3":
        inStorage = True    
        screen.blit(bg2, (0,0))
        last_screen="bedroom"
        renderItems(storageSlots, current_storage_contents, storageSlotSize)

    if current_screen == "kitchen": 
        last_screen="hall7"
        screen.blit(kitchen, (0, 0))
        craftFood = pygame.Rect(165, 570 , 35, 35)
        pygame.draw.rect(screen, (255, 0, 0), craftFood, 2)
        if clicked and craftFood.collidepoint(mouse_pos):
            current_screen = "craftFood"

    if current_screen == "craftFood": 
        inStorage = False
        incraftFood = True    
        screen.blit(bg2, (0,0))
        last_screen="kitchen"
        renderItems(foodSlots, food_contents, foodSlotSize)

    if current_screen == "workshop": 
        last_screen="hall7"
        screen.blit(workshop, (0, 0)) 
        benchRec = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        benchRecBasic = pygame.Rect(255, 130, 230, 210)
        pygame.draw.polygon(screen, (255, 0, 0), rect_points, 4) 
        pygame.draw.polygon(screen, (255, 0, 0), rect_points_basic, 4) 
        if clicked and benchRecBasic.collidepoint(mouse_pos):
            current_screen = "bench"

    if current_screen == "bench":
        inBench = True
        last_screen="workshop"
        screen.blit(workbench1, (0, 0)) 

        materials = bench_items[current_item_index]["materialsNeeded"]
        if 'bench_contents' not in globals() or len(bench_contents) != len(materials):
            bench_contents = [None] * len(materials)
        box_rects = []
        showCraftableItems()
    
    if currentBackground == "topRight":
        spawn_collectibles(current_screen)

    if current_screen == "insideCave1":
        last_screen="game"
        screen.blit(insideCave1, (0, 0))  
        screen.blit(imageSprite, (player_pos.x, player_pos.y))

        if currentInventoryItem: 
            smaller_item = pygame.transform.scale(currentInventoryItem, (30, 30))
            screen.blit(smaller_item,(player_pos.x-7, player_pos.y+30))
        
        for finger in fingers: 
            finger_rect = pygame.Rect(finger["pos"].x, finger["pos"].y, 100, 100)
            if finger_rect.colliderect(player_rect): 
                fingerIsBigger = True
                mouse_pos = pygame.mouse.get_pos()  
                if finger_rect.collidepoint(mouse_pos):
                    if heldItem == "pickAx":
                        if clicked: 
                            finger["clickCount"] += 1 #remove all this 
                            finger["last_click_time"] = pygame.time.get_ticks() 
                        if finger["clickCount"] == 1:
                            finger["rockPresent"] = True  
                    else: 
                        if clicked: 
                            showHint = True
            else: 
                fingerIsBigger = False

            if finger["rockPresent"] and not finger["rockCollected"]: 
                collectible = finger["assignedCollectible"]
                if collectible:
                    screen.blit(collectible["goodImage"], (finger["pos"].x, finger["pos"].y))
                else:
                    screen.blit(purpleRock, (finger["pos"].x, finger["pos"].y))     # why           
                
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - finger.get("last_click_time", 0)
                
                if elapsed_time < 1:
                    add_to_inventory(collectible)
                if elapsed_time > 500:
                    finger["rockCollected"] = True 
            elif not finger["rockCollected"]: 
                if fingerIsBigger: 
                    screen.blit(finger["bigImage"], (finger["pos"].x, finger["pos"].y)) 
                else:
                    screen.blit(finger["image"], (finger["pos"].x, finger["pos"].y)) 

        if showHint: 
            pygame.draw.rect(screen, "black", (200, 350, 880, 60), 50)
            hintText = fontSmall.render(hintMessage, True, RED) 
            screen.blit(hintText, (250, screen_height/2 +2)) 

    for i, slot in enumerate(inventory_slots):
        color = "gray"
        if selected_slot_index == i and selected_item_from_inventory:
            color= "yellow"
        pygame.draw.rect(screen, color , slot, 3)
        if inventory_contents[i] is not None:
            item_name = inventory_contents[i]
            item_time = inventory_timestamps[i]

            if selected_slot_index == i:
                heldItem = inventory_contents[selected_slot_index]

            for items in collectible_items.values():
                for itm in items:
                    if itm["goodName"] == item_name:
                        # Check if the item has gone bad
                        if item_time is not None and totalTime - item_time >= itm.get("bad_after", float("inf")):
                            if itm["badName"] is not None:
                                item_name = itm["badName"]
                                inventory_contents[i] = item_name  
                                inventory_timestamps[i] = None  
                        break
                    item_img = pygame.transform.scale(item_images[item_name], (inventory_slot_size, inventory_slot_size))
                    screen.blit(item_img, (slot.x, slot.y))
    
    if current_screen == "inPayload": 
        last_screen = "game"
        screen.blit(inPayload, (0, 0))  
        collect_rect = pygame.Rect(400, 472, 375, 85)
        if collect_rect.collidepoint(mouse_pos) and clicked:
            current_screen = "game"

    if current_screen is not "game" and current_screen is not "inPayload":
        pygame.draw.rect(screen, "black", back_rect, 50)
        backText = font.render('BACK', True, (100, 100, 50))
        screen.blit(backText, (12, 47))
        if back_rect.collidepoint(mouse_pos) and clicked:
            current_screen = last_screen

    # health bar
    pygame.draw.rect(screen, RED, (healthPos[0], healthPos[1] +5, health * (BAR_WIDTH / 100), BAR_HEIGHT))
    pygame.draw.rect(screen, WHITE, (healthPos[0], healthPos[1]+ 5, BAR_WIDTH, BAR_HEIGHT), 2)  
    screen.blit(healthImg, (healthPos[0] - 32 , healthPos[1])) 

    # hunger bar
    pygame.draw.rect(screen, MAGENTA, (HUNGER_POS[0], HUNGER_POS[1]+5, hunger * (BAR_WIDTH / 100), BAR_HEIGHT))
    pygame.draw.rect(screen, WHITE, (HUNGER_POS[0], HUNGER_POS[1]+5, BAR_WIDTH, BAR_HEIGHT), 2)
    screen.blit(forkAndKnife, (HUNGER_POS[0] - 30 , HUNGER_POS[1])) 

    # thirst bar
    pygame.draw.rect(screen, BLUE, (THIRST_POS[0], THIRST_POS[1]+5, thirst * (BAR_WIDTH / 100), BAR_HEIGHT))
    pygame.draw.rect(screen, WHITE, (THIRST_POS[0], THIRST_POS[1]+5, BAR_WIDTH, BAR_HEIGHT), 2)
    screen.blit(thirsty, (THIRST_POS[0] - 30 , THIRST_POS[1])) 

    # Stats bar
    pygame.draw.rect(screen, "black", (0,0, screen_width, 40), 50)
    screen.blit(money, (20, 1))
    countMoneyText = font2.render(f"{money_count}", True, (255, 255, 255))
    screen.blit(countMoneyText, (60, 5))

    # print("bolts available: ", emittedBoltsCount)

    # screen.blit(energyImg, (250, 5))
    screen.blit(energyImg, (160, 5))
    energyCountText = font2.render(f"{emittedBoltsCount}", True, (255, 255, 255))
    # screen.blit(energyCountText, (280, 5))
    screen.blit(energyCountText, (190, 5))

    oreCountText = font2Small.render(f"Eng Req: {minerTotalEnergyReq:.2f}", True, (255, 255, 255))
    screen.blit(oreCountText, (220, 10))

    screen.blit(ore, (500,5))
    oreCountText = font2.render(f"{oreCount:.2f}", True, (255, 255, 255))
    screen.blit(oreCountText, (540, 5))

    screen.blit(clockIcon, (750,1))
    oreRateText = font2.render(f"{oreRate}", True, (255, 255, 255))
    oreRateUnitsText = font2Small.render("Ore/Sec", True, (255, 255, 255))
    screen.blit(oreRateText, (790, 5))
    screen.blit(oreRateUnitsText, (835, 14)) # change x location dynamiclly depending on length of number

    screen.blit(people, (1000,1))
    countPeopleText = font2.render(f"{people_count}", True, (255, 255, 255))
    screen.blit(countPeopleText, (1040, 5))

    if mutedRec.collidepoint(mouse_pos) and clicked: 
        muted = not muted
        if muted:
            pygame.mixer.music.pause()  
        else:
            pygame.mixer.music.unpause()

    if not muted: 
        screen.blit(volume, (screen_width-100, 2))
    else:
        screen.blit(mute, (screen_width-100, 2))

    if not paused and inHome != True: 
        pauseRec = pygame.Rect(screen_width-50, 10 , 45, 45)
        screen.blit(pauseGame, (screen_width-50, 2))

        if pauseRec.collidepoint(mouse_pos) and clicked: 
            paused = not paused
    
    if paused: 
        screen.blit(pauseScreen, (0,0))
        unpauseRec = pygame.Rect(screen_width/2 - 205, 250, 335, 90)
        # pygame.draw.rect(screen, "black", unpauseRec, 50)
        # (screen_width/2 - 205, screen_height/2 + 20, 335, 90) for restart 
        
        if unpauseRec.collidepoint(mouse_pos) and clicked: 
            paused = not paused

    screenRec = pygame.Rect(0, 0, screen_width, screen_height)
    
    mouseReleased = True

    #move this to the begining of the game loop
    if event.type == pygame.MOUSEBUTTONUP:
        mouseReleased = True

    if inHome: 
        screen.blit(homeScreen, (0,0))
        startGameRec = pygame.Rect(screen_width/2 - 172, 380, 335, 90)

        isHovered = startGameRec.collidepoint(mouse_pos) 

        pulse = 1 + 0.05 * math.sin(totalTime * 3)
        draw_rect = startGameRec.inflate(startGameRec.width * (pulse - 1),
                                        startGameRec.height * (pulse - 1))
        
        color = LAVA_RED if isHovered else SUNSET_ORANGE

        pygame.draw.rect(screen, color, draw_rect, border_radius=20)

        text_surface = font.render("START", True, WHITE)
        text_rect = text_surface.get_rect(center=draw_rect.center) 
        text_rect.y += 5
        screen.blit(text_surface, text_rect)

        if isHovered and clicked: 
            inHome = False 
            paused = True # CHANGE TO NEW VAR  ININTROS 
            inIntro1 = True 
            mouseReleased = False
    if inIntro1 == True: 
        screen.blit(intro1, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro1Lines,
            text_color,
            shadow_color,
            x=40,
            y=555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro1 = False 
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False
        if inIntro1:
            if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
                frame_count = 0
                inIntro1 = False
                inIntro2 = True
                mouseReleased = False
        # inIntro1, inIntro2, mouseReleased, frame_count = nextSlide(inIntro1, inIntro2, mouseReleased)
    if inIntro2 == True:
        screen.blit(intro2, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro2Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False

        if inIntro2:
            if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
                frame_count = 0
                inIntro2 = False
                inIntro3 = True
                mouseReleased = False
    if inIntro3 == True:
        screen.blit(intro3, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro3Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False
        if inIntro3:
            if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
                frame_count = 0 
                inIntro3 = False
                inIntro35 = True
                mouseReleased = False
    if inIntro35 == True:
        screen.blit(intro35, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro4Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False
        if inIntro35:
            if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
                frame_count = 0
                inIntro35 = False
                inIntro4 = True
                mouseReleased = False
    if inIntro4 == True:
        screen.blit(intro4, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro5Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False
        if inIntro4:
            if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
                frame_count = 0
                inIntro4 = False
                inIntro5 = True
                mouseReleased = False
    if inIntro5 == True:
        screen.blit(intro5c, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro6Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False
        if inIntro5:
            if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
                frame_count = 0
                inIntro5 = False
                inIntro6 = True
                mouseReleased = False
    if inIntro6 == True:
        screen.blit(intro6, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro7Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False

        if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
            frame_count = 0
            inIntro6 = False
            inIntro7 = True
            mouseReleased = False
    if inIntro7 == True:
        screen.blit(intro7, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro8Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False

        if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
            frame_count = 0
            inIntro7 = False
            inIntro8 = True
            mouseReleased = False
    if inIntro8 == True:
        screen.blit(intro8, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro9Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False

        if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
            frame_count = 0
            inIntro8 = False
            inIntro9 = True
            mouseReleased = False
    if inIntro9 == True:
        screen.blit(intro9, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro10Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False

        if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
            frame_count = 0
            inIntro9 = False
            inIntro10 = True
            mouseReleased = False
    if inIntro10 == True:
        screen.blit(intro10, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro11Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False

        if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
            frame_count = 0
            inIntro10 = False
            inIntro11 = True
            mouseReleased = False
    if inIntro11 == True:
        screen.blit(intro11, (0,0))
        draw_typing_dialog(
            screen,
            font3,
            intro12Lines,
            text_color,
            shadow_color,
            x=40,
            y = 555,
            chars_per_frame=chars_per_frame,
            frame_count=frame_count
        )
        frame_count += 1  
        pygame.display.flip()
        clock.tick(60) 

        skipRect = pygame.Rect(15, 15, 110, 50)
        pygame.draw.rect(screen, "black", skipRect, 50)
        skipText = font.render('Skip', True, MARS_RED)
        screen.blit(skipText, (35, 16))

        if skipRect.collidepoint(mouse_pos) and clicked:
            inIntro2 = False 
            inIntro3 = False
            inIntro4 = False
            inIntro5 = False
            inIntro6 = False
            inIntro7 = False
            inIntro8 = False
            inIntro9 = False
            inIntro10 = False
            inIntro11 = False
            paused = False

        if screenRec.collidepoint(mouse_pos) and clicked and mouseReleased:
            frame_count = 0
            inIntro11 = False
            paused = False
            mouseReleased = False
        
    # game over page 
    if (game_over):   #??????
        if not game_over:  
            game_over = True  
            current_screen = "gameover"  
            pygame.mixer.music.stop()  
            play_music("gameover", loop=False, volume=2)  

        text2 = fontBig.render('GAME OVER', True, (255, 0, 0))
        
        text4 = font.render('PLAY AGAIN', True, (0, 255, 0))
        achieveText = font.render('ACHIEVEMENTS', True, (0, 255, 0))
        screen.blit(bg2, (0, 0))
        screen.blit(text2, (470, 105))
        button_rect = pygame.Rect(495, 515, 300, 80)
        pygame.draw.rect(screen, "black", (495, 515, 300, 80), 50)
        achieve_rect = pygame.Rect(495, 620, 300, 80)
        pygame.draw.rect(screen, "black", (495, 620, 300, 80), 50)
        screen.blit(text4, (540, 535))
        screen.blit(achieveText, (510, screen_height-80))

        if current_screen == "gameover":
            if button_rect.collidepoint(mouse_pos):
                numCaptured = 0
                totalTime = 0
                game_over = False
                win_counted = False
                collisionTracked = False
                play_music("background", loop=True, volume=2)
                current_screen = "game"
                player_pos = pygame.Vector2(screen_width / 2, 10)

                cows = [
                    {
                        "pos": pygame.Vector2(
                            random.randint(0, screen_width - cowSize),
                            random.randint(screen_height // 2, screen_height - cowSize)
                        ),
                        "speed": random.randint(2, 15),
                        "direction": pygame.Vector2(random.choice([-1, 1]), 0),
                        "time_since_last_change": 0,
                        "time_since_last_jump": 0,
                        "time_below": 0,
                        "sound_played": False
                    }
                for _ in range(numOfCows)
                ]
                 
                farmers= [
                    {
                    "pos": pygame.Vector2(
                        random.randint(0, screen_width - farmerSize),
                        random.randint(0, screen_height//2)
                    ),
                    "speed": random.randint(10, 40),
                    "direction": pygame.Vector2(0, random.choice([-1, 1])),
                    "time_since_last_change": 0,
                    }
                    for _ in range(numOfFarmers)
                    ]
            elif achieve_rect.collidepoint(mouse_pos):
                current_screen = "achievements"
            elif current_screen == "achievements":
                if back_rect.collidepoint(mouse_pos):
                    current_screen = "gameover"

        if current_screen == "achievements": 
            screen.blit(bg2, (0, 0))
            achievements_text = fontBig.render("Achievements", True, (255, 255, 255))
            screen.blit(achievements_text, (screen_width / 2 - 170, 6))

            pygame.draw.rect(screen, "black", back_rect, 50)
            backText = font.render('BACK', True, (0, 255, 0))
            screen.blit(backText, (595, screen_height-80))
            pygame.display.update()

    pygame.display.flip()

pygame.mixer.music.stop()

pygame.quit()