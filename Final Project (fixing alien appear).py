"""
#Work with Sofia Antonia Vazquez from CISC-108
#The link to my demonstration video: https://youtu.be/HfdfO-CTl2A

NOTE:
We didn't do "alien wrap" because our alien don't
move horizontally off the edge of the screen.


## Galaga Features
# Milestone 1
[X] Spaceship exists
[X] Spaceship moves
[X] Holding keys
[X] Screen limits
# Milestone 2
[x] Aliens exist
[x] Aliens move
[x] Aliens wrap
[x] Aliens reset
[x] Aliens hurt
# Milestone 3
[X] Shoot lasers
[X] Lasers move
[X] Offscreen lasers
[X] Lasers hurt
[X] Game over
[X] Show stats
# Extra Credit
[X] Explosions
[ ] Menus
[X] Items
[ ] Tractor Beams
"""

from dataclasses import dataclass
from designer import *
from random import randint

Rocket_speed = 8
set_window_color("black")


@dataclass
class World:
    rocket: DesignerObject
    rocket_speed: int
    aliens: list[DesignerObject]
    life: int
    counter: DesignerObject
    lasers: list[DesignerObject]
    score: int
    explosions: list[DesignerObject]
    heart_powerups: list[DesignerObject]
    multi_shot_powerups  :list[DesignerObject]


Player_life = 3


def create_world() -> World:
    """ Create the world """
    return World(create_rocket(), 0, [], Player_life,
                 text("white", "hello", 30, get_width() * (1 / 2), get_height() * (1 / 2)), [], 0, [], [],[])


def create_rocket() -> DesignerObject:
    """ Create the rocket at the bottom of screen"""
    rocket = emoji("rocket")
    rocket.y = get_height() - 120
    rocket.flip_x = True
    turn_left(rocket, 45)
    return rocket


def head_left(world: World):
    """ Make the rocket start moving left  """
    world.rocket_speed = -Rocket_speed
    world.rocket.flip_x = False


def head_right(world: World):
    """ Make the rocket start moving left """
    world.rocket_speed = Rocket_speed
    world.rocket.flip_x = True


def move_rocket(world: World):
    """ Move the rocket horizontally"""
    world.rocket.x += world.rocket_speed


def flip_rocket(world: World, key: str):
    """ Change the moving direction of the rocket
    when left or right key is pressed down"""
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)


def stop_rocket(world: World, key: str):
    """Stop the rocket when left or right key is released"""
    if key == "left" or key == "right":
        world.rocket_speed = 0


def limit_rocket_when_typing(world: World, key: str):
    """ limit the rocket horizontal movement when
    pressing the arrow key so that it cannot move off-screen"""
    if world.rocket.x > get_width() - 30 and key == "right":
        world.rocket_speed = 0
    elif world.rocket.x < 30 and key == "left":
        world.rocket_speed = 0


def limit_rocket(world: World):
    """ limit the rocket horizontal movement when updating
    so that the rokcet cannot move off-screen"""
    if world.rocket.x > get_width() - 30:
        world.rocket_speed = 0
    elif world.rocket.x < 30:
        world.rocket_speed = 0


def create_alien() -> DesignerObject:
    """create the alien that appears at the top of the screen"""
    alien = emoji("👾")
    alien.x = randint(10, get_width() - 10)
    return alien


def not_to_many_aliens(world: World):
    """limit the number of aliens on screen to a certain amount"""
    return len(world.aliens) <= 12


def aliens_appear(world: World):
    """make aliens appear in a pyramid structure, stop generating
    any alien when there is still alien on screen"""

    pyramid_height = 6
    pyramid_spacing = 100
    if len(world.aliens) == 0:
        for row in range(pyramid_height):
                for col in range(row + 1):
                    new_alien = create_alien()
                    new_alien.x = get_width() // 2 - (row * pyramid_spacing // 2) + col * pyramid_spacing
                    new_alien.y = 5 + row * 30
                    world.aliens.append(new_alien)
                    
        


alien_speed = 4


def make_aliens_move(world: World):
    """make aliens on-screen move at a certain speed"""
    for alien in world.aliens:
        alien.y += alien_speed


def wrap_aliens(world: World):
    """wrap the aliens back to the top of the screen
    if it exceeds the bottom on the screen"""
    for alien in world.aliens:
        if alien.y > get_height():
            alien.y = 0


def reset_rocket_position(world: World):
    """helper function, reset the rocket position to the center of the screen"""
    world.rocket.x = get_width() * (1 / 2)


def alien_hurts(world: World):
    """when alien and rocket collide, take off 1 layer life,
    remove the correspond alien, and respawn rocket back to the center of the screen"""
    alien_gone = []
    for alien in world.aliens:
        if colliding(alien, world.rocket):
            world.explosions.append(create_explosion(alien.x, alien.y))
            alien_gone.append(alien)
            reset_rocket_position(world)
            if world.life > 0:
                world.life -= 1
    world.aliens = filter_from(world.aliens, alien_gone)


def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    """This takes in an old list and a list of elements not
    to keep. First, it creates an empty list called to_keep.
    Then, it iterates the old_list and if any element from old_list
    is in elements_to_not_keep, it destroys it. If not, it adds it to
    the list to_keep and returns that list."""
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values


def update_life(world: World):
    """Update the score"""
    world.counter.text = "You have:" + str(world.life) + ' Lives,'


def no_life(world: World):
    """Return True if there are no more lives,
so that we know when to execute flash_game_over"""
    has_no_life = False
    if world.life <= 0:
        has_no_life = True
    return has_no_life


def flash_game_over(world):
    """ Show the game over message """
    world.counter.text = "GAME OVER! Score:" + str(world.score)


# phase 3
laser_speed = -9


def create_laser() -> DesignerObject:
    """Create a laser shot whenever this function is called"""
    the_laser = ellipse("lightblue", 8, 20)  # emoji("💣")
    return the_laser


def shoot_laser(world: World, key: str):
    """Craete a laser shot when space key is pressed. The player would
    not be able to shoot lasers after the rocket is dead"""
    if key == "space" and world.life > 0:
        new_laser = create_laser()
        new_laser.x = world.rocket.x
        new_laser.y = world.rocket.y - 30
        world.lasers.append(new_laser)


def laser_moves(world: World):
    """move the existing laser at a constant speed"""
    for the_laser in world.lasers:
        the_laser.y += laser_speed


def laser_alien_collides(world: World):
    """When the laser hits the alien, laser and alien both got destroyed, player gain 1 score"""
    alien_gone = []
    laser_gone = []
    for alien in world.aliens:
        for laser in world.lasers:
            if colliding(alien, laser):
                world.explosions.append(create_explosion(laser.x, laser.y))
                alien_gone.append(alien)
                laser_gone.append(laser)
                world.score += 1
    world.aliens = filter_from(world.aliens, alien_gone)
    world.lasers = filter_from(world.lasers, laser_gone)


def destroy_offscreen_lasers(world: World):
    """destroy any lasers that reached the top of the screen"""
    laser_kept = []
    for laser in world.lasers:
        if laser.y > 20:
            laser_kept.append(laser)
        else:
            destroy(laser)
    world.lasers = laser_kept


def update_score(world: World):
    """Update the score"""
    if world.life > 0:
        world.counter.text += "  Score:" + str(world.score)


def create_explosion(x_position: int, y_position: int) -> DesignerObject:
    """create an explosion at a destined position"""
    explosion = emoji("💥")
    explosion.x = x_position
    explosion.y = y_position
    explosion.visible = True
    explosion.alpha = 1.0
    return explosion


def fade_explosions(world: World):
    """expande the size of explosions and fade explosions away"""
    for explosion in world.explosions:
        if explosion.scale_x > 0 and explosion.scale_y > 0:
            explosion.scale_x += .05
            explosion.scale_y += .05
            explosion.alpha -= .05

def destroy_explosion(world:World):
    """destroy all of the explosion designerobjects that are faded away"""
    kept = []
    for explosion in world.explosions:
        if explosion.alpha > 0.2:
            kept.append(explosion)
        else:
            destroy(explosion)
    world.explosions = kept
            
        

def create_hearts() -> DesignerObject:
    """a heart emoji, if the rocket gets the emoji, player gain 1 life."""
    heart = emoji("💓")
    return heart


def heart_adds_a_life(world: World):
    """add 1 player life when the rocket collides with the heart powerup
    by checking the position of the heart and rocket. Once they collided together,
    the heart powerup would disappear
    Once player's life reached 0, colliding rocket with heart powerup won't add life anymore"""
    heart_gone = []
    for heart in world.heart_powerups:
        if colliding(heart, world.rocket) and world.life>0:
            world.life += 1
            heart_gone.append(heart)
    world.heart_powerups = filter_from(world.heart_powerups, heart_gone)

def create_multituple_shots() -> DesignerObject:
    """a function that would create the multi-shot powerup when it's called"""
    multi_shot = emoji("✨")
    return multi_shot

def multi_shot_shots(world:World):
    """a funciton that create 18 randomly positioned laser shots when rocket
    collides with the multi-shot powerup by checking the position of the
    multi-shot poweup and the rocket. Once both collides, the multi-shot powerup disappears
    Once the life reached 0, colliding rocket with multi-shot powerup will not have any effect.
    """
    multi = 18
    multi_shot_powerup_gone = []
    for multi_shot in world.multi_shot_powerups:
        if colliding(multi_shot, world.rocket) and world.life>0:
            for shot in range(multi):
                shot = create_laser()
                shot.x = randint(10, get_width() - 10)
                shot.y = world.rocket.y
                world.lasers.append(shot)
            multi_shot_powerup_gone.append(multi_shot)
    world.multi_shot_powerups = filter_from(world.multi_shot_powerups, multi_shot_powerup_gone)


def destroy_offscreen_multishot_powerups(world:World):
    """destroy all multi-shot powerups that moved offscreen"""
    kept = []
    for multi_shot in world.multi_shot_powerups:
        if multi_shot.y < get_height():
            kept.append(multi_shot)
        else:
            destroy(multi_shot)
    world.multi_shot_powerups = kept

def destroy_offscreen_heart_powerups(world:World):
    """destroy all heart powerups that moved offscreen"""
    kept = []
    for heart in world.heart_powerups:
        if heart.y < get_height():
            kept.append(heart)
        else:
            destroy(heart)
    world.heart_powerups = kept
    
powerup_speed = 5


def create_powerup(world: World):
    """a function that creates powerup at a chance of 1/50 every frame.
    The function would stop creating new heart powerups once player reached 5 lives
    The function would only allow at most 5 multi-shot powerups on screen at the same time"""
    chance_for_powerups = randint(1, 50)
    if chance_for_powerups == 1 and world.life <= 5:
        new_heart = create_hearts()
        new_heart.y = 5
        new_heart.x = randint(5, get_width())
        world.heart_powerups.append(new_heart)
    if chance_for_powerups == 2 and len(world.multi_shot_powerups) <= 5:
        multi_powerup = create_multituple_shots()
        multi_powerup.y=5
        multi_powerup.x = randint(5, get_width())
        world.multi_shot_powerups.append(multi_powerup)
        


def powerup_moves(world: World):
    """makes all powerups move at a certain speed downward"""
    for heart in world.heart_powerups:
        heart.y += powerup_speed
    for multi_shot in world.multi_shot_powerups:
        multi_shot.y += powerup_speed


when("updating", update_life)
when("updating", alien_hurts)
when("typing", flip_rocket)
when("done typing", stop_rocket)
when("updating", move_rocket)
when("updating", limit_rocket)
when("typing", limit_rocket_when_typing)
when("updating", aliens_appear)
when("updating", make_aliens_move)
when("updating", wrap_aliens)
when(no_life, flash_game_over)
when("typing", shoot_laser)
when("updating", laser_moves)
when("updating", laser_alien_collides)
when("updating", update_score)
when("updating", destroy_offscreen_lasers)
when("updating", destroy_offscreen_multishot_powerups)
when("updating", destroy_offscreen_heart_powerups)
when("updating", destroy_explosion)
when("updating", fade_explosions)
when("updating", create_powerup)
when("updating", powerup_moves)
when("updating", heart_adds_a_life)
when("updating", multi_shot_shots)
when("starting", create_world)

start()
