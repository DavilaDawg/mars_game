# fix music 
# fix clicking pickax and it goes inside the storage 
# fix pickax moving slot randomly
# deselect items and swap inside inventory 
# make messanger move after not being collided with 
# make text background for message 
# make mining abilities 
# make hunger bar/ health bar/ thirst bar/ oxigen bar / Sleep bar / oxigen level bar 
# make kitchen gadgets 
# make stackable items for storage 
# make fuel leak/ critical oxigen level for hallway 
# make farming 
# assignable tasks for crew 
# skills for crew 
# task list 
# fix comms 
# build farm, start with only space food, build 2 stations, then tell ground to send the next crew??
# make farm 

# make mining abilities 
# make farm 
# make kitchen gadgets 


import pygame
import random

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
bg2 = pygame.transform.scale(pygame.image.load("./icon/black.png"), (screen_width, screen_height))
insideCave1 = pygame.transform.scale(pygame.image.load("./icon/cav1_.webp"), (screen_width, screen_height))
hall3 = pygame.transform.scale(pygame.image.load("./icon/hall3.jpg"), (screen_width, screen_height))
hall6 = pygame.transform.scale(pygame.image.load("./icon/hall6.jpg"), (screen_width, screen_height))
hall7 = pygame.transform.scale(pygame.image.load("./icon/hall7.webp"), (screen_width, screen_height))
bedroom = pygame.transform.scale(pygame.image.load("./icon/bedroom.jpg"), (screen_width, screen_height))
kitchen = pygame.transform.scale(pygame.image.load("./icon/k2.webp"), (screen_width, screen_height))
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
numOfFingers = random.randint(3, 6)
xPosFinger = random.randint(0, screen_width)
yPosFinger = random.randint(0, screen_height)

# States
game_over = False
mining = False
current_screen = "game" 
selectedItem = "pickAx"
selected_slot_index = None
selected_item_from_inventory = True
mouse_pos = None
last_screen = None 
inStorage = False
incraftFood = False
axObtained = False
crewMessage= "Hi there captin! Go to your bedroom and find your pickax in the storage bin. Time to go mining!" 

back_rect1= pygame.Rect(495, 620, 300, 80)
back_rect = pygame.Rect(18, 23, 100, 50)

font = pygame.font.Font("MODERNA.ttf", 36)
fontBig = pygame.font.Font("MODERNA.ttf", 70)
fontSmall = pygame.font.Font("MODERNA.ttf", 25)

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
table =  pygame.transform.scale(pygame.image.load("./icon/table.png"), (100,100))
station = pygame.transform.scale(pygame.image.load("./icon/station.png"), (110,110))
pickAx= pygame.transform.scale(pygame.image.load('./icon/pickax.png'), (40,40))
message = pygame.transform.scale(pygame.image.load('./icon/message.png'), (40,40))
purpleRock = pygame.transform.scale(pygame.image.load('./icon/rock1.png'), (40,40))
iron = pygame.transform.scale(pygame.image.load('./icon/rock3.png'), (40,40))
coal = pygame.transform.scale(pygame.image.load('./icon/rock2.png'), (40,40))
gold = pygame.transform.scale(pygame.image.load('./icon/rock4.png'), (40,40))
finger = pygame.transform.scale(pygame.image.load('./icon/finger.png'), (60,60))
tomato = pygame.transform.scale(pygame.image.load('./icon/tomato1.png'), (40,40))
tomatoTree = pygame.transform.scale(pygame.image.load('./icon/tomato.png'), (40,40))
apple = pygame.transform.scale(pygame.image.load('./icon/apple.png'), (40,40))
caramel = pygame.transform.scale(pygame.image.load('./icon/caramel.png'), (40,40))
caramelApple = pygame.transform.scale(pygame.image.load('./icon/caramel-apple.png'), (40,40))
grapes = pygame.transform.scale(pygame.image.load('./icon/apple.png'), (40,40))

collectible_items = {
    "game": [
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width-50),
            random.randint(0, screen_height-50)
            ),  
            "goodImage": flippedBannana, 
            "badImage": badBannana,         
            "goodName": "item1",    
            "badName": "badBannana",                                
            "collected": False,
            "bad_after": 10              
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
            "collected": False
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
            "collected": False    
        }
    ],
    "bedroom": [
        {
            "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
            ),
            "goodImage": pickAx,
            "badImage": None,         
            "goodName": "pickAx",
            "badName": None,
            "collected": False    
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
            "collected": False    
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
            "collected": False    
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
            "collected": False    
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
            "collected": False    
        }
    ]
}

item_images = {
    "item1": flippedBannana, 
    "badBannana": badBannana,
    "chocolate": chocolate,
    "pickAx": pickAx,
    "purpleRock": purpleRock,
    "iron": iron,
    "gold": gold, 
    "coal": coal, 
}

def check_item_collision(player_rect):
    current_items = collectible_items.get(current_screen, [])
    for item in current_items:
        if not item["collected"]:  
            item_rect = pygame.Rect(item["pos"].x, item["pos"].y, 40, 40)  
            if player_rect.colliderect(item_rect):  
                if add_to_inventory(item): 
                    item["collected"] = True  

player_pos = pygame.Vector2(screen_width / 2, 10)

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
             random.randint(100, screen_width - 100),
            random.randint(100, screen_height - 100) 
        ),
    }
    for _ in range(numOfCaves)
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

inventory_contents = [None, None, None, None, None, None, None, None]

storage_contents1 = [None] * (storageRows * storageCols)
storage_contents2 = [None] * (storageRows * storageCols)
storage_contents3 = [None] * (storageRows * storageCols)

storage_contents1[0] = "pickAx"

current_storage_contents = storage_contents1.copy()

food_contents = [None] * (foodRows * foodCols)

inventory_timestamps = [None] * len(inventory_contents)

def add_to_inventory(item):
    for i, content in enumerate(inventory_contents):
        if content is None:  # first empty slot
            if totalTime < item.get("bad_after", 0):
                inventory_contents[i] = item["goodName"]
                inventory_timestamps[i] = totalTime 
            else:
                if item["badName"] is not None:
                    inventory_contents[i] = item["badName"]  
                else: 
                    inventory_contents[i] = item["goodName"]  
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

play_music("background", loop=True, volume=2)

running = True 
while running: 
    dt = clock.tick(60) / 1000
    totalTime += dt 
    ufo_rect = pygame.Rect(player_pos.x, player_pos.y, playerSize, playerSize)

    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    
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
            if back_rect.collidepoint(mouse_pos):  
                current_screen = last_screen
                if current_screen == "game": 
                    play_music("background", loop=True, volume=2)
            for i, slot in enumerate(inventory_slots):
                if slot.collidepoint(mouse_pos): 
                    if selected_slot_index is None: 
                        if inventory_contents[i] is not None:
                            selected_slot_index = i 
                            selected_item_from_inventory = True
                    else:
                        if inventory_contents[i] is None: 
                            if selected_item_from_inventory: 
                                inventory_contents[i]= inventory_contents[selected_slot_index]
                                inventory_contents[selected_slot_index]= None
                            else: # storage to inventory 
                                if inStorage:
                                    inventory_contents[i]= current_storage_contents[selected_slot_index]
                                    if not selected_item_from_inventory:
                                        current_storage_contents[selected_slot_index] = None
                                if incraftFood: 
                                    inventory_contents[i]= food_contents[selected_slot_index]
                                    if not selected_item_from_inventory:
                                        food_contents[selected_slot_index] = None
                            selected_slot_index = None
                    break
            if inStorage:
                for i, slot in enumerate(storageSlots):
                    if slot.collidepoint(mouse_pos):  
                        if selected_slot_index is None:  
                            if current_storage_contents[i] is not None:
                                selected_slot_index = i
                                selected_item_from_inventory = False
                                if current_storage_contents[selected_slot_index] == "pickAx": 
                                    axObtained = True
                        else:
                            if current_storage_contents[i] is None:  # Empty slot
                                if selected_item_from_inventory: # Inventory to storage
                                    current_storage_contents[i] = inventory_contents[selected_slot_index]
                                    inventory_contents[selected_slot_index] = None
                                else: # move within storage
                                    current_storage_contents[i] = current_storage_contents[selected_slot_index]
                                    current_storage_contents[selected_slot_index] = None
                            else: # Swap items if target slot is not empty
                                if selected_item_from_inventory:
                                    inventory_contents[selected_slot_index], current_storage_contents[i] = (
                                        current_storage_contents[i],
                                        inventory_contents[selected_slot_index],
                                    )
                                else:
                                    current_storage_contents[selected_slot_index], current_storage_contents[i] = (
                                        current_storage_contents[i],
                                        current_storage_contents[selected_slot_index],
                                    )
                            selected_slot_index = None
                        break  
            if incraftFood: 
                for i, slot in enumerate(foodSlots):
                    if slot.collidepoint(mouse_pos):  
                        if selected_slot_index is None:  
                            if food_contents[i] is not None:
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
       
    screen.blit(bg, (0, 0))

    check_item_collision(ufo_rect)

    # Draw collectible items that are not yet collected
    for item in collectible_items.get(current_screen, []):
        if not item["collected"]:
            if totalTime< item.get("bad_after", 0): 
                screen.blit(item["goodImage"], (item["pos"].x, item["pos"].y))
            elif totalTime>item.get("bad_after", 0): 
                if item["badImage"] is not None:
                    screen.blit(item["badImage"], (item["pos"].x, item["pos"].y))
                else: 
                    screen.blit(item["goodImage"], (item["pos"].x, item["pos"].y))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 400 * dt
    if keys[pygame.K_d]:
        player_pos.x += 400 * dt
    if keys[pygame.K_w]:
        player_pos.y -= 400 * dt
    if keys[pygame.K_s]:
        player_pos.y += 400 * dt

    # player bounds
    player_pos.x = max(0, min(player_pos.x, screen_width - playerSize))
    player_pos.y = max(0, min(player_pos.y, screen_height - playerSize))

    if current_screen == "game":       
        # farmer logic 
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
            if ufo_rect.colliderect(farmer_rect):  
                collisionTracked =True 
        
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
                        screen.blit(crewText, (40, screen_height/2)) 

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
                    play_music("mine", loop=True, volume=3)

        enter_station_rect = pygame.Rect(screen_width-260, 55, 230, 60)  
        stationRect = pygame.Rect(screen_width-200, 120, 100,100)
        stationText = font.render('Enter station', True, (100, 100, 50)) 
        screen.blit(playerImg, (player_pos.x, player_pos.y))

    if ufo_rect.colliderect(stationRect):  
        pygame.draw.rect(screen, "black", enter_station_rect, 50)
        screen.blit(stationText, (enter_station_rect.x + 7, enter_station_rect.y + 10)) 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            current_screen = "hall3"  

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
        if clicked and bedDoorRec.collidepoint(mouse_pos):
            current_screen = "bedroom"
        if clicked and kitchenDoorRec.collidepoint(mouse_pos):
            current_screen = "kitchen"
        
    if current_screen == "bedroom": 
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

    if current_screen == "insideCave1":
        last_screen="game"
        screen.blit(insideCave1, (0, 0))  
        screen.blit(playerImg, (player_pos.x, player_pos.y))
        screen.blit(finger, (xPosFinger, yPosFinger))


    for i, slot in enumerate(inventory_slots):
        color = "gray"
        if selected_slot_index == i and selected_item_from_inventory:
            color= "yellow"
        pygame.draw.rect(screen, color , slot, 3)
        if inventory_contents[i] is not None:
            item_name = inventory_contents[i]
            item_time = inventory_timestamps[i]

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
        screen.blit(backText, (25, 25))

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

    pygame.display.update()
pygame.mixer.music.stop()
pygame.quit()