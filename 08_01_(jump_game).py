import os
import pygame
import map_reading

pygame.init()

script_dir = os.path.dirname(__file__)

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("super_mario")

#################################################################################################        

player_image = f"{script_dir}\images\player.png"
enemy_image = f"{script_dir}\images\enemy.png"
block_image = f"{script_dir}\images//block.png"

clock = pygame.time.Clock()
myFont = pygame.font.SysFont(None, 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


#################################################################################################
def scroll_move(xto):
    for i in range(1,enemy_count+1):
        globals()[f"enemy{i}"].x_lot -= xspeed * speed * dt
    for i in range(1,block_count+1):
        globals()[f"block{i}"].x_lot -= xspeed * speed * dt

class Unit:
    def __init__(self,image, x_lot, y_lot):
        self.image = pygame.image.load(image)
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.x_lot = x_lot
        self.y_lot = y_lot

    def bump(self,bump_unit):
        self.rect = self.image.get_rect()
        self.rect.left = self.x_lot
        self.rect.top = self.y_lot
        bump_unit_rect = bump_unit.image.get_rect()
        bump_unit_rect.left = bump_unit.x_lot
        bump_unit_rect.top = bump_unit.y_lot

        if self.rect.colliderect(bump_unit_rect):
            return True
        
    def cant_pass(self,bump_unit):
        global able_jump
        global jump_power
        self.rect = self.image.get_rect()
        self.rect.left = self.x_lot
        self.rect.top = self.y_lot
        bump_unit_rect = bump_unit.image.get_rect()
        bump_unit_rect.left = bump_unit.x_lot
        bump_unit_rect.top = bump_unit.y_lot
        bump_unit_rect.right = bump_unit_rect.left + bump_unit.width
        bump_unit_rect.bottom = bump_unit.y_lot + bump_unit.height
        is_right = bump_unit_rect.right - player.x_lot
        is_left = player.x_lot - (bump_unit_rect.left - player.width)
        is_bottom = bump_unit_rect.bottom - player.y_lot
        is_top = player.y_lot - (bump_unit_rect.top - player.height)

        right_or_left = 1
        the_x_lot = 1
        top_or_bottom = 1
        the_y_lot = 1
        
        if self.bump(bump_unit):

            if is_left < is_right:
                right_or_left = is_left
                the_x_lot = (bump_unit_rect.left - player.width)
            elif is_left > is_right:
                right_or_left = is_right
                the_x_lot = bump_unit_rect.right
            else:
                right_or_left = 100

            if is_top < is_bottom:
                top_or_bottom = is_top
                able_jump = True
                the_y_lot = (bump_unit_rect.top - player.height)  +1
            elif is_top > is_bottom:
                top_or_bottom = is_bottom
                able_jump = False
                the_y_lot = bump_unit_rect.bottom
            else:
                top_or_bottom = 100

            if right_or_left < top_or_bottom:
                player.x_lot = the_x_lot
                able_jump = False
                if top_or_bottom > 5:
                    global xspeed
                    xspeed = 0

            
            elif right_or_left > top_or_bottom:
                player.y_lot = the_y_lot
                if right_or_left > 5 and able_jump == False and jump_power > 0:
                    jump_power = 0

        else:
            able_jump = False
            global gravity
            gravity = Gravity

        if able_jump == True:
            jump_power = 0
            gravity = 0


    def move(self,xto,yto):
        global xspeed
        if xto == 0:
            xspeed = xspeed * 0.95
        xspeed += xto * 0.3
        if abs(xto * speed * dt) <= -xspeed* speed * dt and xto != 0 or xspeed* speed * dt >= abs(xto * speed * dt) and xto != 0:
            xspeed = xto
            
        self.x_lot += xspeed * speed * dt
        self.y_lot += yto * speed * dt


        if self.x_lot < 300:
            self.x_lot = 300
            scroll_move(xto)
        if self.x_lot > screen_width - self.width - 300:
            self.x_lot = screen_width - self.width -300
            scroll_move(xto)

        if self.y_lot > screen_height - self.height:
            self.y_lot = screen_height - self.height
    
def jump(block):
    global gravity
    gravity = Gravity
    block.top = block.y_lot
    player.bottom = player.y_lot + player.height
    if player.bump(block) == True:
        if block.top - 2 < player.bottom < block.top + 2:
            if Jump == True:
                global jump_power
                jump_power = jump_power_set
    

def summon_block(x_lot, y_lot):
    global block_count
    block_count += 1
    globals()[f"block{block_count}"] = Unit(block_image,x_lot,y_lot)

def summon_enemy(x_lot, y_lot):
    global enemy_count
    enemy_count += 1
    globals()[f"enemy{enemy_count}"] = Unit(enemy_image,x_lot,y_lot)
    
def dead():
    global running
    running = False



#################################################################################################   



player = Unit(player_image,0,0)
player.x_lot = 325
player.y_lot = 400
enemy = Unit(enemy_image,0,0)
block = Unit(block_image,0,0)
PlayerXto = 0
PlayerYto = 0
xspeed = 0


speed = 0.5
Gravity = 1.5
gravity = Gravity

enemy_count = 0
block_count = 0

Jump = False
jump_power = 0
jump_power_set =80
able_jump = False

#################################################################################################

for line in range(map_reading.line_count):
    for char in range(map_reading.count_line[line]):
        map_line = map_reading.whole_line[line]
        map_char = map_line[char]
        if map_char == '_':
            pass
        elif map_char == 'b':
            summon_block(-500 + char * 50, line * 50)
        elif map_char == 'e':
            summon_enemy(-500 + char * 50, line * 50)
            pass



################################################################################################
running = True

while running:
    dt = clock.tick(120)
    for i in range(1,block_count+1):
        player.cant_pass(globals()[f"block{i}"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Jump = True
            if event.key == pygame.K_DOWN:
                Dash = True
            if event.key == pygame.K_RIGHT:
                PlayerXto += 1
            if event.key == pygame.K_LEFT:
                PlayerXto -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                Jump = False
            if event.key == pygame.K_DOWN:
                Dash = False
            if event.key == pygame.K_RIGHT:
                PlayerXto -= 1
            if event.key == pygame.K_LEFT:
                PlayerXto += 1


    for i in range(1,block_count+1):
        jump(globals()[f"block{i}"])
    player.y_lot -= jump_power / 10
    jump_power -= gravity
    
    player.move(PlayerXto,0)

    for i in range(1,enemy_count+1):
        if player.bump(globals()[f"enemy{i}"]) == True:
            dead()
    if player.y_lot >= 750:
        dead()

    pygame.draw.rect(screen, BLACK, [0,0, screen_width,screen_height])
    for i in range(1,enemy_count+1):
        screen.blit(globals()[f"enemy{i}"].image, (globals()[f"enemy{i}"].x_lot, globals()[f"enemy{i}"].y_lot))
    for i in range(1,block_count+1):
        player.cant_pass(globals()[f"block{i}"])
        screen.blit(globals()[f"block{i}"].image, (globals()[f"block{i}"].x_lot, globals()[f"block{i}"].y_lot))
    screen.blit(player.image, (player.x_lot, player.y_lot))


    pygame.display.flip()