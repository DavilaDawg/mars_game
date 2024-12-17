import pygame
import random

pygame.mixer.init()
pygame.init()

music_files = {
    "background": "./sound/background1.mp3",
    "gameover": "gameover.mp3",
    "clock3" : "clock3.mp3",
}

def play_music(music_key, loop=True, volume=1):
    if music_key in music_files:
        pygame.mixer.music.load(music_files[music_key])
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
    else:
        print(f"Error: {music_key} not found in music_files.")

play_music("background", loop=True, volume=2)

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Mars game")
clock = pygame.time.Clock()
dt = 0
totalTime = 0

screen_width, screen_height = screen.get_size()
bg = pygame.transform.scale(pygame.image.load("./icon/background.webp"), (screen_width, screen_height))
bg2 = pygame.transform.scale(pygame.image.load("./icon/black.png"), (screen_width, screen_height))
tileSize = 40
playerSize = 80
cowSize= 80
farmerSize= 60

playerImg = pygame.transform.scale(pygame.image.load('./icon/astronaut.png'), (playerSize, playerSize))
cowImg = pygame.transform.scale(pygame.image.load('./icon/alien.png'), (cowSize, cowSize))
farmImg = pygame.transform.scale(pygame.image.load('./icon/farm.png'), (90, 90))
cave1Img = pygame.transform.scale(pygame.image.load('./icon/cave1.png'), (100, 100))
cave2Img = pygame.transform.scale(pygame.image.load('./icon/cave2.png'), (100, 100))

numOfCows = 5
numOfFarmers = 2
numOfCaves = random.randint(0, 4)
game_over= False

current_screen = "game" 

mining = False

back_rect = pygame.Rect(495, 620, 300, 80)

font = pygame.font.Font("MODERNA.ttf", 36)
fontBig = pygame.font.Font("MODERNA.ttf", 70)
fontSmall = pygame.font.Font("MODERNA.ttf", 29)

# Icons 
bannana = pygame.transform.scale(pygame.image.load('./icon/bannana.png'), (40, 40))
flippedBannana = pygame.transform.flip(bannana, True, False)
badBannana = pygame.transform.scale(pygame.image.load('./icon/badBannana.png'), (40, 40))
rocket = pygame.transform.scale(pygame.image.load("./icon/rocket.png"), (150,150))
table =  pygame.transform.scale(pygame.image.load("./icon/table.png"), (100,100))
chocolate =  pygame.transform.scale(pygame.image.load("./icon/chocolate-bar.png"), (50,50))


collectible_items = [
    {
        "pos": pygame.Vector2(200, 200),  
        "image": flippedBannana,          
        "name": "item1",                  
        "collected": False                
    },
    {
        "pos": pygame.Vector2(600, 400),
        "image": badBannana,
        "name": "badBannana",
        "collected": False
    },
    {
        "pos": pygame.Vector2(100, 400),
        "image": chocolate,
        "name": "chocolate",
        "collected": False    
    }
]

item_images = {
    "item1": flippedBannana, 
    "badBannana": badBannana,
    "chocolate": chocolate
}

def check_item_collision(player_rect):
    for item in collectible_items:
        if not item["collected"]:  
            item_rect = pygame.Rect(item["pos"].x, item["pos"].y, 40, 40)  
            if player_rect.colliderect(item_rect):  
                if add_to_inventory(item["name"]): 
                    print(f"Collected {item['name']}")
                    item["collected"] = True  
                else:
                    print("Inventory full!")

player_pos = pygame.Vector2(screen_width / 2, 10)

farmers= [
    {
    "pos": pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
        ),
    "speed": random.randint(2, 15),
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
        "speed": random.randint(2, 15),
        "direction": pygame.Vector2(random.choice([-1, 1]), 0),
        "selected": False,
        "captured": False,
        "time_since_last_change": 0,
        "time_since_last_jump": 0,
        "time_below": 0,
        "sound_played": False
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

for row in range(inventory_rows):
    for col in range(inventory_cols):
        x = inventory_start_x + col * (inventory_slot_size + inventory_margin)
        y = inventory_start_y + row * (inventory_slot_size + inventory_margin)
        inventory_slots.append(pygame.Rect(x, y, inventory_slot_size, inventory_slot_size))

inventory_contents = ["item1", None, None, None, None, None, None, None]


def add_to_inventory(item_name):
    for i, content in enumerate(inventory_contents):
        if content is None:  # Find the first empty slot
            inventory_contents[i] = item_name
            return True
    return False  # Inventory is full
    

running = True 
while running: 
    dt = clock.tick(60) / 1000
    totalTime += dt 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()                
            
    screen.blit(bg, (0, 0))

    if totalTime < 10: # MAKE DISAPERE IF COLLECTED
        screen.blit(flippedBannana, (200, 200))
    else:
        screen.blit(badBannana, (200, 200))

    screen.blit(rocket, (screen_width-150, 100))

    ufo_rect = pygame.Rect(player_pos.x, player_pos.y, playerSize, playerSize)

    check_item_collision(ufo_rect)

    # Draw collectible items that are not yet collected
    for item in collectible_items:
        if not item["collected"]:
            screen.blit(item["image"], (item["pos"].x, item["pos"].y))

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
    player_pos.y = max(0, min(player_pos.y, screen_height - playerSize))

    # farmer logic 
    for farmer in farmers:
        # Wandering 
        farmer["time_since_last_change"] += dt
        if farmer["time_since_last_change"] >= 6:
            farmer["direction"] = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
            farmer["time_since_last_change"] = 0

        farmer["pos"] += farmer["direction"] * farmer["speed"] * dt

        # farmer bounds
        if farmer["pos"].x <= 0 or farmer["pos"].x >= screen_width - farmerSize:
            farmer["direction"].x *= -1
        if farmer["pos"].y <= 0 or farmer["pos"].y >= screen_height - farmerSize:
            farmer["direction"].y *= -1

        screen.blit(cowImg, (farmer["pos"].x, farmer["pos"].y))

    
        farmer_rect = pygame.Rect(farmer["pos"].x, farmer["pos"].y, farmerSize, farmerSize)
        if ufo_rect.colliderect(farmer_rect):  
            collisionTracked =True 


    for cave in caves:
        screen.blit(cave1Img, (cave["pos"].x, cave["pos"].y))

        enter_cave_rect = pygame.Rect(cave["pos"].x - 50, cave["pos"].y - 40, 200, 60)  

        mineText = font.render('Enter cave', True, (100, 100, 50)) 

        cave_rect = pygame.Rect(cave["pos"].x, cave["pos"].y, 100, 100)
        if ufo_rect.colliderect(cave_rect):  
            mining = True 
            pygame.draw.rect(screen, "black", enter_cave_rect, 50)
            screen.blit(mineText, (enter_cave_rect.x + 7, enter_cave_rect.y + 10)) 

    # cows logic
    for cow in cows:
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

    screen.blit(cowImg, (cow["pos"].x, cow["pos"].y))

    # Draw items in inventory
    for i, slot in enumerate(inventory_slots):
        if inventory_contents[i] is not None:
            item_img = pygame.transform.scale(item_images[inventory_contents[i]], (inventory_slot_size, inventory_slot_size))
            screen.blit(item_img, (slot.x, slot.y))

    # Draw inventory slots
    for slot in inventory_slots:
        pygame.draw.rect(screen, "gray", slot, 3) 

    screen.blit(playerImg, (player_pos.x, player_pos.y))

    # game over page 
    if (game_over):   
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
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