from turtle import Screen
from game_manager import GameManager
from animator import Animator
from player import Player
from ui import UI
from items import Mask, Medkit, Vaccine
import random
import time

# Set up the screen
screen = Screen()
screen.setup(width= 1500, height= 800)
screen.title("Virus Pandemic Revolution 2 : Beyond the Fortress")
screen.register_shape("./graphics/play_btn.gif")
screen.register_shape("./graphics/player.gif")
screen.register_shape("./graphics/bullet.gif")
screen.tracer(0)

# Shapes to register
SPRITESHAPES = ["./graphics/player_walk_frm1.gif", "./graphics/player_walk_frm2.gif", "./graphics/player_shoot.gif", "./graphics/death.gif", "./graphics/alpha.gif", "./graphics/beta.gif", "./graphics/delta.gif", "./graphics/omicron.gif", "./graphics/food.gif", "./graphics/mask.gif", "./graphics/shield.gif", "./graphics/medkit.gif", "./graphics/vaccine.gif"]
SPAWNPOINTS = (700, 1200, -150, 250, -350, 350)
frames = ["./graphics/player_walk_frm1.gif", "./graphics/player_walk_frm2.gif", "./graphics/player_shoot.gif"]
sprites = []    # To render the sprites
running = True

animator = Animator(frames, screen)
player = Player("./graphics/player.gif", "./graphics/bullet.gif", animator)
ui = UI(player)
game_manager = GameManager(screen, ui)
game_manager.registerShapes(SPRITESHAPES)
mask = Mask("./graphics/mask.gif", "./graphics/shield.gif", random.randint(SPAWNPOINTS[4], SPAWNPOINTS[5]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
medkit = Medkit("./graphics/medkit.gif", random.randint(SPAWNPOINTS[4], SPAWNPOINTS[5]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
vaccine = Vaccine("./graphics/vaccine.gif")

# Prepare sprites 
sprites.append(player)
sprites.append(mask)
sprites.append(medkit)

viruses = game_manager.spawnViruses(4, 3, 2, 1)
foods = game_manager.generateFoods(2)

for virus in viruses:
    virus.goto(random.randint(SPAWNPOINTS[0], SPAWNPOINTS[1]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
    sprites.append(virus)

for food in foods:
    food.goto(random.randint(SPAWNPOINTS[4], SPAWNPOINTS[5]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
    sprites.append(food)

game_manager.setupSprites(sprites)  # Export sprites to the game_manager.py
game_manager.start()
game_manager.play_btn.onclick(game_manager.startGame)

screen.onkeypress(player.moveRight, "Right")
screen.onkeypress(player.moveLeft, "Left")
screen.onkeypress(player.moveUp, "Up")
screen.onkeypress(player.moveDown, "Down")
screen.onkeyrelease(player.stopAnimation, "Right")
screen.onkeyrelease(player.stopAnimation, "Left")
screen.onkeyrelease(player.stopAnimation, "Up")
screen.onkeyrelease(player.stopAnimation, "Down")
screen.onkey(player.fire, "space")
screen.listen()

animator.playerWalk()   # Player Walk Animation

while running:
    screen.update()
    mask.followPlayer(player)
    player.moveBullet()
    animator.updatePos(player)

    # Victory
    if player.distance(vaccine) < 200 and vaccine.in_game:
        game_manager.final_result = "Victory"
        ui.notification.color("#ddc600")
        ui.notification.write("Victory!", False, "center", ui.huge_font)
        running = False

    # Zone Transition
    if player.xcor() > 650 and player.current_zone < 2:
        player.current_zone += 1
        game_manager.switchZone(player, [mask, medkit])
        new_viruses = game_manager.spawnViruses(1, 1, 1, 2)
        for new in new_viruses:
            viruses.append(new)
            new.showturtle()
            new.in_game = True
        for virus in viruses:
            virus.goto(random.randint(SPAWNPOINTS[0], SPAWNPOINTS[1]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
        for food in foods:
            food.goto(random.randint(SPAWNPOINTS[4], SPAWNPOINTS[5]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))

        if player.current_zone == 2:
            vaccine.showturtle()
            vaccine.in_game = True       
    
    # Checking Attack Range
    if player.distance(player.weapon.position()) > player.weapon.atk_range:
        player.reload()
    elif player.weapon.xcor() > 680:
        player.reload()

    # Items Collision Detection
    if mask.distance(player) < 130:
        mask.openShield(player)
        ui.updateShields(mask.shield.stacks)
        ui.updateScore()
    if medkit.distance(player) < 130:
        medkit.superHeal(player)
        ui.updateHealth()
        ui.updateScore()

    # Virus Collision Detections
    for virus in viruses:
        virus.move()

        # Attacked by player
        if player.weapon.distance(virus) < 45 and player.weapon.in_game:
            player.dealDMG(virus, random.randint(SPAWNPOINTS[0], SPAWNPOINTS[1]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
            ui.updateScore()

        # Collision with Player
        elif virus.distance(player) < 130:
            if mask.shield.stacks < 1:
                virus.dealDMG(player, random.randint(SPAWNPOINTS[0], SPAWNPOINTS[1]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
                ui.updateInfo()
                # Game Over   
                if player.in_game != True:
                    game_manager.final_result = "Game Over"
                    ui.notification.color("#ae0000")
                    ui.notification.write("Game Over!", False, "center", ui.huge_font)
                    running = False
            else:
                mask.closeShield(virus, random.randint(SPAWNPOINTS[0], SPAWNPOINTS[1]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
                ui.updateShields(mask.shield.stacks)

        # Render the virus only inside the camera
        elif virus.xcor() < -700:
            virus.goto(random.randint(SPAWNPOINTS[0], SPAWNPOINTS[1]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))

        elif virus.xcor() < 680:
            virus.showturtle()
        else:
            virus.hideturtle()

    # Food Collision Detection
    for food in foods:
        if food.distance(player) < 130:
            food.heal(player, random.randint(SPAWNPOINTS[4], SPAWNPOINTS[5]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
            ui.updateHealth()
            ui.updateScore()

# Wait for a while before displaying the results
time.sleep(1.5)

# Display the Final Results
if game_manager.final_result == "Victory":
    data = [player.score, player.lives, player.viruses_killed, player.infected_times, player.items_collected]
    display = ["Your Score", "Lives Remaining", "Viruses Killed", "Infected Times", "Items Collected"]
    game_manager.victory(display, data)

else:
    data = [player.score, player.lives, player.viruses_killed, player.infected_times, player.items_collected]
    display = ["Your Score", "Lives Remaining", "Viruses Killed", "Infected Times", "Items Collected"]
    game_manager.gameOver(display, data)

screen.exitonclick()