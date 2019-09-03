import pygame
import pygame.locals
import os

screen_width = 480
screen_height = 320
tile_size = 32
screen_width_in_tiles = int(screen_width / tile_size)
screen_height_in_tiles = int(screen_height / tile_size)
screen_x = 0
screen_y = 0

playtime = 0.0

input_mode = "game"
#    Determines whether the program expects button presses or text
#        "game" processes buttons, eg. "left", "start", "B"
#        "console" processes letters, like the ones we type
game_mode = "map"
#    Determines how the game reacts to buttons
#        "map" moves the cursor around the map
#        "menu" moves the cursor around the menu

# Keys
key_buffer = []
down_pressed = False
down_pressed_at = 0.0
up_pressed = False
up_pressed_at = 0.0
left_pressed = False
left_pressed_at = 0.0
right_pressed = False
right_pressed_at = 0.0
a_pressed = False
a_pressed_at = 0.0
b_pressed = False
b_pressed_at = 0.0
r_pressed = False
r_pressed_at = 0.0
l_pressed = False
l_pressed_at = 0.0
start_pressed = False
start_pressed_at = 0.0
select_pressed = False
select_pressed_at = 0.0
cursor_x = 0
cursor_y = 0

class Sprite(pygame.sprite.Sprite):
    
    frame = 0
    frame_count = 1
    last_update = 0.0
    standing_animation = []
    
    def __init__(self, frames = None):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("." + os.sep + "classes" + os.sep + frames + ".sprite")
        self.frame_count = self.image.get_size()[1] // 128
        for i in range(self.frame_count):
            self.standing_animation.append(self.image.subsurface(0, i * 128, 128, 128).convert_alpha())
        
    def update(self):
        global playtime
        if playtime > self.last_update + 0.15:
            self.last_update = playtime
            self.frame = (self.frame + 1) % self.frame_count
        return self.standing_animation[self.frame]
        
    def kill(self):
        self.kill()
    
    def get_image(self):
        return self.image
        

class Actor():

    def __init__(self, name="Eliwood", uid=0, sprite_loc="general", active=True, x=1, y=1):
        self.name = name
        self.active = active
        self.x = x
        self.y = y
        self.uid = uid
        self.sprite = Sprite(sprite_loc)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_sprite(self):
        return self.sprite

class Level():
    
    map_tiles = []
    map_terrain = []
    map_width = 0
    map_height = 0
    actors = []
    
    def __init__(self, level):
        self.level = level
        self.map_tiles = self.load_map(level)
        self.map_terrain = self.load_map_terrain(level)
        self.actors.append(Actor("Oswin", self.generate_UID(), "general", True, 7, 5))
        self.actors.append(Actor("Oswin", self.generate_UID(), "general", True, 6, 4))
        
    def generate_UID(self):
        out = 0
        for actor in self.actors:
            if out <= actor.uid:
                out = actor.uid + 1
        return out
    
    def load_map_terrain(self, level):
        filename = "." + os.sep + "maps" + os.sep + str(level) + os.sep + str(level) + ".terrain"
        with open(filename, 'r') as f:
            for line in f.readlines():
                tmp = []
                for item in line.split(','):
                    tmp.append(item.replace('\n', ''))
                self.map_terrain.append(tmp)
        return self.map_terrain
        
    def load_map(self, level):
        filename = "." + os.sep + "maps" + os.sep + str(level) + os.sep + str(level) + ".map"
        image = pygame.image.load(filename).convert()
        self.set_map_width(int(image.get_size()[0] / tile_size))
        self.set_map_height(int(image.get_size()[1] / tile_size))
        map_tiles = []
        for tile_x in range(0, self.get_map_width()):
            line = []
            for tile_y in range(0, self.get_map_height()):
                rect = (tile_x * tile_size, tile_y * tile_size, tile_size, tile_size)
                line.append(image.subsurface(rect))
            map_tiles.append(line)
        return map_tiles
    
    def get_map(self):
        return self.map_tiles
    
    def get_map_width(self):
        return self.map_width
    
    def get_map_height(self):
        return self.map_height
    
    def set_map_width(self, width):
        self.map_width = width
    
    def set_map_height(self, height):
        self.map_height = height
    
    def get_map_terrain(self):
        return self.map_terrain
    
    def get_actors(self):
        return self.actors


class PyGame():
    mainloop = True

    console_line = ""
    console_history = []

    def __init__(self, width=480, height=320, fps=30):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.foreground = pygame.Surface(self.screen.get_size()).convert()
        self.menus = pygame.Surface(self.screen.get_size()).convert()
        self.console_screen = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))
        self.foreground.fill((255, 255, 255))
        self.menus.fill((255, 255, 255))
        self.console_screen.fill((255, 255, 255))
        self.foreground.set_colorkey((255, 255, 255))
        self.menus.set_colorkey((255, 255, 255))
        self.console_screen.set_colorkey((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont("mono", 20, bold=True)
        
        # Load Map
        self.level = Level(1)
        
    def run(self):
        while self.mainloop:
            self.update_clock()
            self.handle_input()
            self.game_logic()
            self.render()
        pygame.quit()
        
    def draw_text(self, text, colour, x, y):
        surface = self.font.render(text, True, (colour))
        self.console_screen.blit(surface, (x, y))
        
    def update_clock(self):
        global playtime # Too much work to remove
        playtime = playtime + self.clock.tick(self.fps) / 1000.0
        pygame.display.set_caption("FPS:{:6.3} Time:{:6.3}s X:{} Y:{}".format(self.clock.get_fps(), playtime, (cursor_x - screen_x), (cursor_y - screen_y)))
    
    def handle_input(self):
        global playtime # Too much work to remove
        global input_mode # Necessary evil
        
        global key_buffer # Ugly as fuck. Do remove this
        global down_pressed
        global down_pressed_at
        global up_pressed
        global up_pressed_at
        global left_pressed
        global left_pressed_at
        global right_pressed
        global right_pressed_at
        global a_pressed
        global a_pressed_at
        global b_pressed
        global b_pressed_at
        global r_pressed
        global r_pressed_at
        global l_pressed
        global l_pressed_at
        global start_pressed
        global start_pressed_at
        global select_pressed
        global select_pressed_at
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.mainloop = False
                
            # Process keys in console mode
            if input_mode == "console":  # Close console with `
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE:
                        input_mode = "close_console"
                    elif event.key == pygame.K_RETURN:
                        self.process_console_line(self.console_line)
                        self.console_line = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.console_line = self.console_line[:-1]
                    elif event.key >= 21 and event.key <= 125:
                        self.console_line += chr(event.key)
                        
            # Process keys in game mode
            elif input_mode == "game":
                
                # Key down
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Exiting FEGame")
                        self.mainloop = False
                    elif event.key == pygame.K_BACKQUOTE:  # Open console with `
                        input_mode = "console"
                    elif event.key == pygame.K_DOWN:
                        down_pressed = True
                        down_pressed_at = playtime
                        key_buffer.append(pygame.K_DOWN)
                    elif event.key == pygame.K_UP:
                        up_pressed = True
                        up_pressed_at = playtime
                        key_buffer.append(pygame.K_UP)
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = True
                        right_pressed_at = playtime
                        key_buffer.append(pygame.K_RIGHT)
                    elif event.key == pygame.K_LEFT:
                        left_pressed = True
                        left_pressed_at = playtime
                        key_buffer.append(pygame.K_LEFT)
                    elif event.key == pygame.K_d:
                        a_pressed = True
                        a_pressed_at = playtime
                        key_buffer.append(pygame.K_d)
                    elif event.key == pygame.K_w:
                        b_pressed = True
                        b_pressed_at = playtime
                        key_buffer.append(pygame.K_w)
                        # TODO: Add the rest of the buttons
                    
                # Key up
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        down_pressed = False
                    elif event.key == pygame.K_UP:
                        up_pressed = False
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = False
                    elif event.key == pygame.K_LEFT:
                        left_pressed = False
                    elif event.key == pygame.K_d:
                        a_pressed = False
                    elif event.key == pygame.K_w:
                        b_pressed = False
            
        # Process pressed keys
        key_press_delay = 0.07
        if down_pressed and down_pressed_at < (playtime - key_press_delay):
            key_buffer.append(pygame.K_DOWN)
            down_pressed_at = playtime
        elif up_pressed and up_pressed_at < (playtime - key_press_delay):
            key_buffer.append(pygame.K_UP)
            up_pressed_at = playtime
        elif right_pressed and right_pressed_at < (playtime - key_press_delay):
            key_buffer.append(pygame.K_RIGHT)
            right_pressed_at = playtime
        elif left_pressed and left_pressed_at < (playtime - key_press_delay):
            key_buffer.append(pygame.K_LEFT)
            left_pressed_at = playtime
        elif a_pressed and a_pressed_at < (playtime - key_press_delay):
            key_buffer.append(pygame.K_d)
            a_pressed_at = playtime
        elif b_pressed and b_pressed_at < (playtime - key_press_delay):
            key_buffer.append(pygame.K_w)
            b_pressed_at = playtime
            
        # Cleanup
        if input_mode == "close_console":
            input_mode = "game"
    
    def process_console_line(self, line):

        if len(self.console_history) > 12:
            self.console_history = self.console_history[1:]
        self.console_history.append(line)
        
        # Actually Process
        if line == "exit" or line == "quit":
            self.mainloop = False
        elif line.startswith("load level "):
            level_num = line.split(' ')[2]
            if level_num.isdigit():
                self.level = Level(level_num)
    
    def game_logic(self):
        # TEMP
        global map_terrain
        
        global key_buffer
        global cursor_x
        global cursor_y
        global sreen_width_in_tiles
        global sreen_height_in_tiles
        global screen_x
        global screen_y
        
        # Process key presses
        for key in key_buffer:
            if game_mode == "map":
                # Screen Scrolling Begins
                if key == pygame.K_DOWN:
                    if cursor_y < screen_height_in_tiles - 3:
                        cursor_y = min(cursor_y + 1, screen_height_in_tiles - 1)
                    elif screen_height_in_tiles - screen_y < self.level.get_map_height():
                        screen_y = max(-(self.level.get_map_height() + screen_height_in_tiles), screen_y - 1)
                    else:
                        cursor_y = min(cursor_y + 1, screen_height_in_tiles - 1)
                elif key == pygame.K_UP:
                    if cursor_y >= 3:
                        cursor_y = cursor_y = max(cursor_y - 1, 0)
                    elif screen_y < 0:
                        screen_y = screen_y + 1
                    else:
                        cursor_y = cursor_y = max(cursor_y - 1, 0)
                elif key == pygame.K_RIGHT:
                    if cursor_x < screen_width_in_tiles - 4:
                        cursor_x = min(cursor_x + 1, screen_width_in_tiles - 1)
                    elif screen_width_in_tiles - screen_x < self.level.get_map_width():
                        screen_x = max(-(self.level.get_map_width() + screen_width_in_tiles), screen_x - 1)
                    else:
                        cursor_x = min(cursor_x + 1, screen_width_in_tiles - 1)
                elif key == pygame.K_LEFT:
                    if cursor_x > 3:
                        cursor_x = max(cursor_x - 1, 0)
                    elif screen_x < 0:
                        screen_x = screen_x + 1
                    else:
                        cursor_x = max(cursor_x - 1, 0)
                # End Screen Scrolling
                elif key == pygame.K_d:
                    pass
                elif key == pygame.K_w:
                    pass
                
            if game_mode == "menu":
                pass
        
        # Finish
        key_buffer = []
        
    def draw_cursor(self):
        pygame.draw.rect(self.foreground, (254, 254, 254), (cursor_x * tile_size, cursor_y * tile_size, tile_size, tile_size >> 3))
        pygame.draw.rect(self.foreground, (254, 254, 254), (cursor_x * tile_size, cursor_y * tile_size, tile_size >> 3, tile_size))
        
    def render_console(self):
        global console_line
        pygame.draw.rect(self.menus, (254, 254, 254), (tile_size >> 1, tile_size >> 1, screen_width - tile_size, screen_height - tile_size))
        pygame.draw.rect(self.menus, (0, 0, 0), (tile_size, screen_height - tile_size - 26, screen_width - (tile_size << 1), 1))
        self.draw_text(self.console_line, (0, 0, 0), tile_size, screen_height - tile_size - 16)
        for i in range(len(self.console_history)):
            if self.console_history[i] != "":
                self.draw_text(self.console_history[i], (0, 0, 0), tile_size, tile_size + (i * 16))
                
    def render_menu(self):
        pygame.draw.rect(self.menus, (50, 120, 170), (tile_size >> 1, screen_height - ((tile_size << 1) + (tile_size >> 1)), tile_size << 2, tile_size << 1))
        for actor in self.level.get_actors():
            if actor.x == (cursor_x - screen_x) and actor.y == (cursor_y - screen_y):
                self.draw_text((actor.name + " " + str(actor.uid)), (254, 254, 254), tile_size, screen_height - ((tile_size << 1) + (tile_size >> 1)))
                    # TEMP4
        self.draw_text(self.level.get_map_terrain()[cursor_y - screen_y][cursor_x - screen_x], (254, 254, 254), tile_size, screen_height - (tile_size << 1))
        
    def render_sprites(self):
        for actor in self.level.get_actors():
            self.foreground.blit(actor.sprite.update(), (((screen_x + actor.x) * tile_size) - (tile_size + (tile_size >> 1)), ((screen_y + actor.y) * tile_size) - (tile_size + (tile_size >> 1))))
        
    def render(self):
        global map_tiles
        global tile_size
        global screen_x
        global screen_y
        global game_mode
        # Seems to be running every frame. Destroy and rebuild background every frame?
        self.screen.fill((0, 0, 0))  # Clear screen
        self.foreground.fill((255, 255, 255))  # Clear foreground
        self.menus.fill((255, 255, 255))  # Clear Menus
        self.console_screen.fill((255, 255, 255))  # Clear Menus
        
        if game_mode == "map":
            # Draw background
            for x, row in enumerate(self.level.get_map()):
                for y, tile in enumerate(row):
                    self.screen.blit(tile, ((screen_x + x) * tile_size, (screen_y + y) * tile_size))
        
            # Draw Foreground elements
            self.render_sprites()
                
            # Draw Menu
            self.render_menu()
            
            # Draw Cursor
            self.draw_cursor()
        
        if input_mode == "console":
            self.render_console()
        
        # Update screen
        self.screen.blit(self.foreground, (0, 0))
        self.screen.blit(self.menus, (0, 0))
        self.screen.blit(self.console_screen, (0, 0))
        
        pygame.display.flip()

        
# ## Start
if __name__ == "__main__":
    PyGame(screen_width, screen_height).run()

''' TO GET BACK TO
-Fix bug where overlapping sprites overwrite eachother
-Finish adding in all the buttons
-Make the entire thing OOP and remove all the global variables
-Bugtest

### TO DO
- Add sprites
- Add Loader for terrain, actors, characters, classes
- Add class for terrain, character (maybe?), class
- Add movement + combat

'''