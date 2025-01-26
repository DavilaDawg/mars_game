# stack items
# finish health bar/radiation 
# population and teraform info
# fix if eat food disapeer
# make kitchen gadgets 
# make stackable items for storage 
# make fuel leak/ critical oxigen level for hallway 
# make farming 
# assignable tasks for crew 
# skills for crew 
# task list 
# fix comms 
# build farm, start with only space food, build 2 stations, then tell ground to send the next crew??
# make random roocks generate, make finger generration unique/independent per cave 
# fix mining glitch if click a lot
# add pause + leaderboard + main page 
# fix clickng to new object and not placing thee placable one at the same time

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

tileSize = 40
playerSize = 70
cowSize= 70
farmerSize= 70

playerImg = pygame.transform.scale(pygame.image.load('./icon/astronaut.png'), (playerSize, playerSize))
astroImg1 = pygame.transform.scale(pygame.image.load('./icon/astronaut3.png'), (cowSize, cowSize))
astroImg2 = pygame.transform.scale(pygame.image.load('./icon/astronaut2.png'), (farmerSize, farmerSize))
cave1Img = pygame.transform.scale(pygame.image.load('./icon/cave1.png'), (100, 100))
cave2Img = pygame.transform.scale(pygame.image.load('./icon/cave2.png'), (100, 100))

numOfCows = 2
numOfFarmers = 2
numOfCaves = random.randint(1, 4)
numOfFingers = random.randint(7, 11)
xPosFinger = random.randint(0, screen_width)
yPosFinger = random.randint(0, screen_height)

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
incraftFood = False
axObtained = False
rockPresent = False
holding = False
muted = False 
showHint = False 

minHoldTime = 750
holdStartTime = 0
crewMessage= "Hi there captin! Go to your bedroom and find your pickax in the storage bin. Time to go mining!" 
hintMessage= 'You need a pickax to mine. Go to your bedroom storage for it.'

back_rect1= pygame.Rect(495, 620, 300, 80)
back_rect = pygame.Rect(6, 45, 100, 50)

x_offset = 150  # Move to the right
y_offset = 20  # Move down

rect_points = [
    (screen_width // 2 +2 + x_offset, screen_height // 2 -2 + y_offset),  # Top-left
    (screen_width // 2 + 112 + x_offset, screen_height // 2 + 2 + y_offset),  # Top-right
    (screen_width // 2 + 32 + x_offset, screen_height // 2 + 55 + y_offset),  # Bottom-right
    (screen_width // 2 - 130 + x_offset, screen_height // 2 + 38 + y_offset)   # Bottom-left
]

x_coords = [point[0] for point in rect_points]
y_coords = [point[1] for point in rect_points]
min_x, min_y = min(x_coords), min(y_coords)
max_x, max_y = max(x_coords), max(y_coords)

font = pygame.font.Font("MODERNA.ttf", 36)
fontBig = pygame.font.Font("MODERNA.ttf", 70)
fontSmall = pygame.font.Font("MODERNA.ttf", 25)
fontSmall2 = pygame.font.Font("MODERNA.ttf", 23)
fontSmaller = pygame.font.Font("MODERNA.ttf", 25)

font_path = pygame.font.match_font("arial")  # Use Arial or a similar font
font2 = pygame.font.Font(font_path, 27)

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

BAR_WIDTH, BAR_HEIGHT = 150, 20
healthPos = (300, 45)
HUNGER_POS = (500, 45)
THIRST_POS = (700, 45)
# ENERGY_POS= (900, 45)

health = 100
hunger = 100
thirst = 100  
# energy = 100 
DECAY_RATE = 5

increaseHunger = 20 
increaseThirst= 30
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
table =  pygame.transform.scale(pygame.image.load("./icon/table.png"), (100,100))
station = pygame.transform.scale(pygame.image.load("./icon/station.png"), (110,110))
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
volume = pygame.transform.scale(pygame.image.load('./icon/volume.png'), (40,40))
mute = pygame.transform.scale(pygame.image.load('./icon/volumeOff.png'), (40,40))
leftArrow = pygame.transform.scale(pygame.image.load('./icon/leftArrow.png'), (80,80))
rightArrow = pygame.transform.scale(pygame.image.load('./icon/rightArrow.png'), (80,80))
hoe =pygame.transform.scale(pygame.image.load('./icon/hoe.png'), (40,40))
wrench =pygame.transform.scale(pygame.image.load('./icon/wrench.png'), (40,40))
solarPanel = pygame.transform.scale(pygame.image.load('./icon/solarPanel.png'), (80,80))
oven = pygame.transform.scale(pygame.image.load('./icon/oven.png'), (110,110))
ice = pygame.transform.scale(pygame.image.load('./icon/ice.png'), (49,49))
iceMelterUnit = pygame.transform.scale(pygame.image.load('./icon/iceMelterUnit.png'), (49,49))
waterStorage = pygame.transform.scale(pygame.image.load('./icon/waterStorage.png'), (49,49))
upgradedWorkbench = pygame.transform.scale(pygame.image.load('./icon/3d.png'), (49,49))

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
    "upgradedWorkbench": upgradedWorkbench
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
    "materialsNeeded" : [iron, iron],
     },
    {"image": nail,
     "name": "nail",
    "display": "Nail",
    "materialsNeeded" : [iron],
     }, 
    {"image": saw,
     "name": "saw",
    "display": "Saw",
    "materialsNeeded" : [iron, purpleRock],
     }, 
     {"image": hoe,
     "name": "hoe",
    "display": "Hoe",
    "materialsNeeded" : [iron, iron],
    },
      {"image": wrench,
     "name": "wrench",
    "display": "Wrench", 
    "materialsNeeded" : [iron, purpleRock],
     },
      {"image": bolt,
     "name": "bolt",
    "display": "Bolt", 
    "materialsNeeded" : [iron],
     },
     {"image": solarPanel, 
     "name": "solarPanel",
    "display": "Solar Panel",
    "materialsNeeded" : [iron, purpleRock, saw, hammer, nail, nail, nail, nail],
     },
      {"image": iceMelterUnit,
     "name": "iceMelterUnit",
     "display": "Ice Melter Unit",
    "materialsNeeded" : [purpleRock, purpleRock, iron,iron, saw, hammer, nail, nail, nail],
     }, 
      {"image": waterStorage,
     "name": "waterStorage",
     "display": "Water Storage",
    "materialsNeeded" : [purpleRock, wrench, bolt, bolt, bolt],
     }, 
    {"image": upgradedWorkbench,
      "name": "3d",
      "display": "Upgraded Workbench",
     "materialsNeeded" : [purpleRock, iron , iron,wrench, bolt, bolt, saw, hammer, nail, nail],
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

placable_item = ["solarPanel", "iceMelterUnit", "waterStorage", "upgradedWorkbench"] 
placed_items = []
MIN_DISTANCE = 50

last_emission_times = {}
emission_interval = 3
emitted_bolts_count = 0
bolts_emitted = {}

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
    "image": finger
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

inventory_contents = ["solarPanel", "waterStorage", None, None, None, None, None, None]

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
    global current_item_index
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
                    print("first line has two words then the rest on the second but smaller")
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
            itemText = fontSmaller.render(displayName, True, (255, 255, 255))
            text_x = screen_width / 2 - 130
            screen.blit(itemText, (text_x, 201))
    else:
        # fits as is 
        text_x = screen_width / 2 - textWidth / 2
        screen.blit(itemText, (text_x, 201))

    transItem = pygame.transform.scale(pygame.image.load(f'./icon/{itemName}.png'), (40,40)).convert_alpha()
    transItem.set_alpha(90)
    itemRect = pygame.Rect(screen_width/2 - 45 , screen_height/2 + 76, 90, 90)
    leftRect = pygame.Rect(screen_width/2 - 210, 185, 90, 90)
    rightRrect = pygame.Rect(screen_width/2 + 132, 185, 90, 90)
    pygame.draw.rect(screen,(24, 116, 205),itemRect, 3)
    scaledItemImg = pygame.transform.scale(transItem, (80, 80))
    screen.blit(leftArrow, (screen_width/2 - 211, 185)) 
    screen.blit(rightArrow, (screen_width/2 + 132, 185)) 
    screen.blit(scaledItemImg, (screen_width/2 -40,screen_height/2 + 80))

    if leftRect.collidepoint(mouse_pos) and clicked: 
        current_item_index = (current_item_index - 1) % len(bench_items) # index wraps around if it goes below 0
    elif rightRrect.collidepoint(mouse_pos) and clicked:
        current_item_index = (current_item_index + 1) % len(bench_items)
    
    materials = itemData["materialsNeeded"]
    material_box_width, material_box_height = 55, 55
    gap = 15

    total_width = len(materials) * (material_box_width + gap) - gap
    start_x = (screen_width - total_width) // 2
    start_y = 285

    for i, material in enumerate(materials):
        transMat = material.convert_alpha()
        transMat.set_alpha(150)
        box_x = start_x + i * (material_box_width + gap)
        box_rect = pygame.Rect(box_x, start_y, material_box_width, material_box_height)

        pygame.draw.rect(screen, (24, 116, 205),box_rect, 3)
        screen.blit(transMat, (box_x + gap - 8 , start_y + 6))
    

play_music("background", loop=True, volume=2)

mutedRec = pygame.Rect(screen_width-50, 10 , 50, 50)

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
    ufo_rect = pygame.Rect(player_pos.x, player_pos.y, playerSize, playerSize)

    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    current_time = time.time()
    if current_time - last_update_time >= 1: 
        hunger = max(0, hunger - DECAY_RATE) # Compares the result of hunger - DECAY_RATE with 0 and returns the greater of the two
        thirst = max(0, thirst - DECAY_RATE)
        # energy = max(0, energy - DECAY_RATE)
        last_update_time = current_time

    if hunger == 0 or thirst ==0 or health ==0: 
        game_over=True

    # Emit bolts for each solar panel placed
    for item in placed_items:
        last_emission_time = last_emission_times.get(item["position"], 0)

        if item["item"] == "solarPanel":
            if current_time - last_emission_time >= emission_interval:
                emitted_bolts_count += 3  # Increment the total emitted bolts count
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
                            placed_items.append({
                                "background": currentBackground, 
                                "position": centered_pos, 
                                "item": heldItem,
                            })
            if back_rect.collidepoint(mouse_pos):
                current_screen = last_screen
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
                            else: # storage to inventory 
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
                                elif not selected_item_from_inventory and current_storage_contents[selected_slot_index] is not None: # move within storage
                                    current_storage_contents[i] = current_storage_contents[selected_slot_index]
                                    current_storage_contents[selected_slot_index] = None
                            else:
                                if selected_item_from_inventory and selected_slot_index is not None and inventory_contents[selected_slot_index] is not None: # swap from inventory to storage
                                    print("inventory to storage")
                                    inventory_contents[selected_slot_index], current_storage_contents[i] = (
                                        current_storage_contents[i],
                                        inventory_contents[selected_slot_index],
                                    )
                                elif selected_slot_index is not None and current_storage_contents[selected_slot_index] is not None: # swap within storage
                                    print("swap within")
                                    current_storage_contents[selected_slot_index], current_storage_contents[i] = (
                                        current_storage_contents[i],
                                        current_storage_contents[selected_slot_index],
                                    )
                            selected_slot_index = None
                        break  
            if incraftFood: 
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

    if current_screen == "game":       
        if currentBackground == "topRight":
            screen.blit(topRight, (0,0))
            if ufo_rect.left == 0:  
                change_background("topLeft")
                player_pos.x = screen_width - playerSize
            elif ufo_rect.bottom >= screen_height:  
                change_background("bottomRight")
                player_pos.y = 35

        elif currentBackground == "topLeft":
            if ufo_rect.right >= screen_width: 
                change_background("topRight")
                player_pos.x = 0
            elif ufo_rect.bottom >= screen_height:  
                change_background("bottomLeft")
                player_pos.y = 35

        elif currentBackground == "bottomRight":
            if ufo_rect.left == 0:  
                change_background("bottomLeft")
                player_pos.x = screen_width - playerSize
            elif ufo_rect.top == 35: 
                change_background("topRight")
                player_pos.y = screen_height - playerSize

        elif currentBackground == "bottomLeft":
            if ufo_rect.right >= screen_width:  
                change_background("bottomRight")
                player_pos.x = 0
            elif ufo_rect.top == 35: 
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

    check_item_collision(ufo_rect)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 400 * dt
    if keys[pygame.K_RIGHT]:
        player_pos.x += 400 * dt
    if keys[pygame.K_UP]:
        player_pos.y -= 400 * dt
    if keys[pygame.K_DOWN]:
        player_pos.y += 400 * dt

    # player bounds
    player_pos.x = max(0, min(player_pos.x, screen_width - playerSize))
    player_pos.y = max(35, min(player_pos.y, screen_height - playerSize))

    if current_screen == "game":       
        screen.blit(playerImg, (player_pos.x, player_pos.y))
        if currentBackground == "topRight":
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

                screen.blit(station, (screen_width-200, 120))
            
                farmer_rect = pygame.Rect(farmer["pos"].x, farmer["pos"].y, farmerSize, farmerSize)
            
            for cave in caves:
                screen.blit(cave1Img, (cave["pos"].x, cave["pos"].y))
                enter_cave_rect = pygame.Rect(cave["pos"].x - 50, cave["pos"].y - 40, 200, 60)  
                mineText = font.render('Enter cave', True, (100, 100, 50)) 
                cave_rect = pygame.Rect(cave["pos"].x, cave["pos"].y, 100, 100)
            
                if ufo_rect.colliderect(cave_rect):  
                    mining = True 
                    pygame.draw.rect(screen, "black", enter_cave_rect, 50)
                    screen.blit(mineText, (enter_cave_rect.x + 7, enter_cave_rect.y + 10)) 
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        current_screen = "insideCave1"  
                        if not muted:
                            play_music("mine", loop=True, volume=3)

            enter_station_rect = pygame.Rect(screen_width-260, 55, 230, 60)  
            stationRect = pygame.Rect(screen_width-200, 120, 100,100)
            stationText = font.render('Enter station', True, (100, 100, 50)) 
            screen.blit(playerImg, (player_pos.x, player_pos.y)) 

            # cows logic
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

        if ufo_rect.colliderect(stationRect):  
            pygame.draw.rect(screen, "black", enter_station_rect, 50)
            screen.blit(stationText, (enter_station_rect.x + 7, enter_station_rect.y + 10)) 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                current_screen = "hall3"  

        for item in placed_items:
            if item["background"] == currentBackground:
                image = item_images[item["item"]]
                screen.blit(image, item["position"])

    if currentInventoryItem: 
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
        pygame.draw.polygon(screen, (255, 0, 0), rect_points, 4) 
        if clicked and benchRec.collidepoint(mouse_pos):
            current_screen = "bench"

    if current_screen == "bench":
        inBench = True
        last_screen="workshop"
        screen.blit(workbench1, (0, 0)) 
        showCraftableItems()
    
    if currentBackground == "topRight":
        spawn_collectibles(current_screen)

    if current_screen == "insideCave1":
        last_screen="game"
        screen.blit(insideCave1, (0, 0))  
        screen.blit(playerImg, (player_pos.x, player_pos.y))

        if currentInventoryItem: 
            smaller_item = pygame.transform.scale(currentInventoryItem, (30, 30))
            screen.blit(smaller_item,(player_pos.x-7, player_pos.y+30))
        
        for finger in fingers: 
            finger_rect = pygame.Rect(finger["pos"].x, finger["pos"].y, 100, 100)
            if finger_rect.colliderect(ufo_rect): 
                mouse_pos = pygame.mouse.get_pos()  
                if finger_rect.collidepoint(mouse_pos):
                    print("collide")
                    if heldItem == "pickAx":
                        print("waiting for click")
                        if clicked: 
                            print("Mouse clicked")
                            finger["clickCount"] += 1
                            finger["last_click_time"] = pygame.time.get_ticks() 
                        if finger["clickCount"] >= 3:
                            finger["rockPresent"] = True  
                    else: 
                        if clicked: 
                            showHint = True

            if finger["rockPresent"] and not finger["rockCollected"]: 
                screen.blit(purpleRock, (finger["pos"].x, finger["pos"].y))

                current_time = pygame.time.get_ticks()
                
                elapsed_time = current_time - finger.get("last_click_time", 0)
                print(f"Elapsed Time: {elapsed_time} ms")

                if elapsed_time < 1:
                    add_to_inventory(collectible_items["insideCave1"][0])
                if elapsed_time > 500:
                    print("Rock collected after 1 second")
                    finger["rockCollected"] = True 
            elif not finger["rockCollected"]: 
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

    if current_screen is not "game":
        pygame.draw.rect(screen, "black", back_rect, 50)
        backText = font.render('BACK', True, (100, 100, 50))
        screen.blit(backText, (12, 47))

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

    # # energy bar
    # pygame.draw.rect(screen, GREEN, (ENERGY_POS[0], ENERGY_POS[1]+5, energy * (BAR_WIDTH / 100), BAR_HEIGHT))
    # pygame.draw.rect(screen, WHITE, (ENERGY_POS[0], ENERGY_POS[1]+5, BAR_WIDTH, BAR_HEIGHT), 2)
    # screen.blit(energyImg, (ENERGY_POS[0] - 30 , ENERGY_POS[1])) 

    # Stats bar
    pygame.draw.rect(screen, "black", (0,0, screen_width, 40), 50)
    screen.blit(energyImg, (20, 5))
    count_text = font2.render(f"{emitted_bolts_count}", True, (255, 255, 255))
    screen.blit(count_text, (50, 5))

    if mutedRec.collidepoint(mouse_pos) and clicked: 
        muted = not muted
        if muted:
            pygame.mixer.music.pause()  
        else:
            pygame.mixer.music.unpause()

    if not muted: 
        screen.blit(volume, (screen_width-50, 10))
    else:
        screen.blit(mute, (screen_width-50, 10))

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