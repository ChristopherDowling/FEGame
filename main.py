import pygame
import pygame.locals
import os
import csv

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

any_selected = False


class Sprite(pygame.sprite.Sprite):
    
    frame = 0
    frame_count = 1
    last_update = 0.0
    standing_animation = []
    size = 0
    pos = (0, 0)
    uid = 0
    
    def __init__(self, frames=None, uid=0, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        global tile_size
        global screen_x
        global screen_y
        
        self.source = pygame.image.load("." + os.sep + "classes" + os.sep + frames + ".sprite").convert_alpha()
        self.size = self.source.get_size()[0]
        self.frame_count = self.source.get_size()[1] // self.size
        for i in range(self.frame_count):
            self.standing_animation.append(self.source.subsurface(0, i * self.size, self.size, self.size))
        
        self.pos = (pos[0], pos[1])  # TODO: OOP
        self.rect = ((pos[0] * tile_size) - (self.size - tile_size >> 1), (pos[1] * tile_size) - (self.size - tile_size >> 1), self.size, self.size)
        
    def update(self, *args):
        global playtime
        if playtime > self.last_update + 0.15:
            self.last_update = playtime
            self.frame += 1
        self.image = self.standing_animation[(self.frame) % self.frame_count]
        self.rect = (((self.pos[0] + screen_x) * tile_size) - (self.size - tile_size >> 1), ((self.pos[1] + screen_y) * tile_size) - (self.size - tile_size >> 1), self.size, self.size)
        
    def kill(self):
        self.kill()
    
    def get_image(self):
        return self.image
    
    def get_pos(self):
        return self.pos
    
    def set_pos(self, pos):
        self.pos = pos
        

class Item():

    def __init__(self, NAME, ICON, Type, RANK, RANGE, WT, MT, HIT, CRIT, MAX_DUR, WORTH, WEX, SPC):
        self.NAME = NAME
        self.ICON = ICON
        self.Type = Type
        self.RANK = RANK
        self.RANGE = RANGE
        self.WT = WT
        self.MT = MT
        self.HIT = HIT
        self.CRIT = CRIT
        self.MAX_DUR = MAX_DUR
        self.DUR = MAX_DUR
        self.WORTH = WORTH
        self.WEX = WEX
        self.SPC = SPC
        self.image = pygame.image.load("." + os.sep + "resources" + os.sep + "items" + os.sep + ICON + ".png").convert_alpha


class Actor():
    
    items = []

    def __init__(self, NAME, UID, MUG, CLASS, DESC, SPC, LEVEL, BASE_HP, BASE_STR, BASE_SKL, BASE_SPD, BASE_LUK, BASE_DEF, BASE_RES, HP_GROWTH, STR_GROWTH, SKL_GROWTH, SPD_GROWTH, LUK_GROWTH, DEF_GROWTH, RES_GROWTH, MOVE, MOVE_TYPE, CON, AID, AFFIN, SWORD, AXE, LANCE, BOW, ANIMA, DARK, LIGHT, STAFF, ITEM_1, ITEM_2, ITEM_3, ITEM_4, ITEM_5, SUPPORT_1, SUPPORT_1_BASE, SUPPORT_1_GROWTH, SUPPORT_2, SUPPORT_2_BASE, SUPPORT_2_GROWTH, SUPPORT_3, SUPPORT_3_BASE, SUPPORT_3_GROWTH, SUPPORT_4, SUPPORT_4_BASE, SUPPORT_4_GROWTH, SUPPORT_5, SUPPORT_5_BASE, SUPPORT_5_GROWTH):
        self.NAME = NAME
        self.UID = UID
        self.MUG = pygame.image.load("." + os.sep + "characters" + os.sep + MUG + ".png").convert_alpha()
        self.CLASS = CLASS
        self.DESC = DESC
        self.SPC = SPC
        self.LEVEL = LEVEL
        self.EXP = "0"
        self.MAX_HP = BASE_HP
        self.CURRENT_HP = self.MAX_HP
        self.STR = BASE_STR
        self.SKL = BASE_SKL
        self.SPD = BASE_SPD
        self.LUK = BASE_LUK
        self.DEF = BASE_DEF
        self.RES = BASE_RES
        self.HP_GROWTH = HP_GROWTH
        self.STR_GROWTH = STR_GROWTH
        self.SKL_GROWTH = SKL_GROWTH
        self.SPD_GROWTH = SPD_GROWTH
        self.LUK_GROWTH = LUK_GROWTH
        self.DEF_GROWTH = DEF_GROWTH
        self.RES_GROWTH = RES_GROWTH
        self.STR_PART = "0.0"
        self.SKL_PART = "0.0"
        self.SPD_PART = "0.0"
        self.LUK_PART = "0.0"
        self.DEF_PART = "0.0"
        self.RES_PART = "0.0"
        self.MOVE = MOVE
        self.MOVE_TYPE = MOVE_TYPE
        self.CON = CON
        self.AID = AID
        self.TRV = None
        self.AFFIN = AFFIN
        self.COND = None
        self.SWORD = SWORD
        self.AXE = AXE
        self.LANCE = LANCE
        self.BOW = BOW
        self.ANIMA = ANIMA
        self.DARK = DARK
        self.LIGHT = LIGHT
        self.STAFF = STAFF
        for item in PyGame.items:
            if ITEM_1 == item.NAME:
                self.items.append(item)
            if ITEM_2 == item.NAME:
                self.items.append(item)
            if ITEM_3 == item.NAME:
                self.items.append(item)
            if ITEM_4 == item.NAME:
                self.tems.append(item)
            if ITEM_5 == item.NAME:
                self.items.append(item)
        self.SUPPORT_1 = SUPPORT_1
        self.SUPPORT_1_BASE = SUPPORT_1_BASE
        self.SUPPORT_1_GROWTH = SUPPORT_1_GROWTH
        self.SUPPORT_2 = SUPPORT_2
        self.SUPPORT_2_BASE = SUPPORT_2_BASE
        self.SUPPORT_2_GROWTH = SUPPORT_2_GROWTH
        self.SUPPORT_3 = SUPPORT_3
        self.SUPPORT_3_BASE = SUPPORT_3_BASE
        self.SUPPORT_3_GROWTH = SUPPORT_3_GROWTH
        self.SUPPORT_4 = SUPPORT_4
        self.SUPPORT_4_BASE = SUPPORT_4_BASE
        self.SUPPORT_4_GROWTH = SUPPORT_4_GROWTH
        self.SUPPORT_5 = SUPPORT_5
        self.SUPPORT_5_BASE = SUPPORT_5_BASE
        self.SUPPORT_5_GROWTH = SUPPORT_5_GROWTH
        self.status = "idle"
        self.pos = (0, 0)
        self.sprite = Sprite(self.CLASS.lower(), self.UID, self.pos)
        PyGame.sprites.add(self.sprite)

    def get_pos(self):
        return self.pos
    
    def set_pos(self, pos):
        self.pos = pos
        self.sprite.set_pos(pos)

    def get_sprite(self):
        return self.sprite
    
    def set_sprite(self, sprite):
        self.sprite = sprite
    
    def get_uid(self):
        return self.UID


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
        
        self.load_characters()
        
    def load_characters(self, loc="." + os.sep + "data" + os.sep + "characters.csv"):
        data = list(csv.reader(open(loc)))
        del data[0]
        self.actors = []
        for l in data:  # Ugly as fuck but who cares?
            self.actors.append(Actor(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11], l[12], l[13], l[14], l[15], l[16], l[17], l[18], l[19], l[20], l[21], l[22], l[23], l[24], l[25], l[26], l[27], l[28], l[29], l[30], l[31], l[32], l[33], l[34], l[35], l[36], l[37], l[38], l[39], l[40], l[41], l[42], l[43], l[44], l[45], l[46], l[47], l[48], l[49], l[50], l[51], l[52], l[53]))
        
    def load_units(self, loc="." + os.sep + "data" + os.sep + "characters.csv"):
        pass
    
    def save_units(self, loc):
        location = "." + os.sep + "saves" + os.sep + loc + ".save"
        print("Saving to: ", location)
        file = open(location, "w+")
        file.close()
        file = open(location, "a+")
        for actor in self.actors:
            if actor.TRV == None:
                actor.TRV = "None"
            if actor.COND == None:
                actor.COND = "None"
            file.write(actor.NAME + "," + actor.UID + "," + actor.MUG + "," + actor.CLASS + "," + actor.DESC + "," + actor.SPC + "," + actor.LEVEL + "," + actor.EXP + "," + actor.MAX_HP + "," + actor.CURRENT_HP + "," + actor.STR + "," + actor.SKL + "," + actor.SPD + "," + actor.LUK + "," + actor.DEF + "," + actor.RES + "," + actor.HP_GROWTH + "," + actor.STR_GROWTH + "," + actor.SKL_GROWTH + "," + actor.SPD_GROWTH + "," + actor.LUK_GROWTH + "," + actor.DEF_GROWTH + "," + actor.RES_GROWTH + actor.HP_GROWTH + "," + actor.STR_PART + "," + actor.SKL_PART + "," + actor.SPD_PART + "," + actor.LUK_PART + "," + actor.DEF_PART + "," + actor.RES_PART + "," + actor.MOVE + "," + actor.MOVE_TYPE + "," + actor.CON + "," + actor.AID + "," + actor.TRV + "," + actor.AFFIN + "," + actor.COND + "," + actor.SWORD + "," + actor.AXE + "," + actor.LANCE + "," + actor.BOW + "," + actor.ANIMA + "," + actor.DARK + "," + actor.LIGHT + "," + actor.STAFF + "," + actor.ITEM_1 + "," + actor.ITEM_2 + "," + actor.ITEM_3 + "," + actor.ITEM_4 + "," + actor.ITEM_5 + "," + actor.SUPPORT_1 + "," + actor.SUPPORT_1_BASE + "," + actor.SUPPORT_1_GROWTH + "," + actor.SUPPORT_2 + "," + actor.SUPPORT_2_BASE + "," + actor.SUPPORT_2_GROWTH + "," + actor.SUPPORT_3 + "," + actor.SUPPORT_3_BASE + "," + actor.SUPPORT_3_GROWTH + "," + actor.SUPPORT_4 + "," + actor.SUPPORT_4_BASE + "," + actor.SUPPORT_4_GROWTH + "," + actor.SUPPORT_5 + "," + actor.SUPPORT_5_BASE + "," + actor.SUPPORT_5_GROWTH)
        file.close()
        
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
    
    sprites = pygame.sprite.Group()
    
    blue_square = None
    
    r_screen = "stats"
    #    "stats" displays stats
    #    "inv" displays inventory and combat stats
    #    "supports" displays weapon levels and supports
    focus_actor = None
    
    items = []

    def __init__(self, width=480, height=320, fps=30):
        pygame.init()
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.midground = pygame.Surface(self.screen.get_size()).convert()
        self.foreground = pygame.Surface(self.screen.get_size()).convert()
        self.menus = pygame.Surface(self.screen.get_size()).convert()
        self.console_screen = pygame.Surface(self.screen.get_size()).convert()
        
        self.background.fill((0, 0, 0))
        self.midground.fill((0, 0, 0))
        self.foreground.fill((0, 0, 0))
        self.menus.fill((0, 0, 0))
        self.console_screen.fill((0, 0, 0))
        
        self.midground.set_colorkey((0, 0, 0))
        self.foreground.set_colorkey((0, 0, 0))
        self.menus.set_colorkey((0, 0, 0))
        self.console_screen.set_colorkey((0, 0, 0))
        
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont("mono", 20, bold=True)
        
        # Load Resources
        self.load_resources()
        
        # Load Map
        self.level = Level(1)
        
    def run(self):
        while self.mainloop:
            self.update_clock()
            self.handle_input()
            self.game_logic()
            self.render()
        pygame.quit()
        
    def load_resources(self):
        blue_square = pygame.image.load("." + os.sep + "resources" + os.sep + "blue_square.png").convert_alpha
        
        data = list(csv.reader(open("." + os.sep + "data" + os.sep + "items.csv")))
        del data[0]
        for l in data:
            self.items.append(Item(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11], l[12]))
        
    def draw_text(self, text, colour, x, y):
        surface = self.font.render(text, True, (colour))
        self.console_screen.blit(surface, (x, y))
        
    def update_clock(self):
        global playtime  # Too much work to remove
        playtime = playtime + self.clock.tick(self.fps) / 1000.0
        pygame.display.set_caption("FPS:{:6.3} Time:{:6.3}s X:{} Y:{}".format(self.clock.get_fps(), playtime, (cursor_x - screen_x), (cursor_y - screen_y)))
    
    def handle_input(self):
        global playtime  # Too much work to remove
        global input_mode  # Necessary evil
        global key_buffer
        
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
        global b_pressed_at  # Ugly as fuck. Do remove this
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
                print("Exiting FEGame")
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
                    elif event.key == pygame.K_s:
                        r_pressed = True
                        r_pressed_at = playtime
                        key_buffer.append(pygame.K_s)
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
                    elif event.key == pygame.K_s:
                        r_pressed = False
            
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
        elif r_pressed and r_pressed_at < (playtime - key_press_delay):
            key_buffer.append(pygame.K_s)
            r_pressed_at = playtime
            
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
            print("Exiting FEGame")
        elif line.startswith("load level "):
            level_num = line.split(' ')[2]
            if level_num.isdigit():
                self.level = Level(level_num)
        elif line.startswith("move "):
            args = line.split(" ")
            for actor in self.level.actors:
                if str(actor.get_uid()) == args[1]:
                    actor.set_pos((int(args[2]), int(args[3])))
        elif line.startswith("list actors"):
            for actor in self.level.actors:
                print(actor.name, actor.uid, actor.pos, actor.status)
        elif line.startswith("save units "):
            arg = line.split(" ")[2]
            self.level.save_units(arg)
        elif line.startswith("list items"):
            for item in Items:
                print("TEMP")
    
    def game_logic(self):
        # TEMP
        global map_terrain
        global game_mode
        
        global key_buffer
        global cursor_x
        global cursor_y
        global sreen_width_in_tiles
        global sreen_height_in_tiles
        global screen_x
        global screen_y
        global any_selected
        
        # Process key presses
        for key in key_buffer:
            if game_mode == "r_screen":
                if key == pygame.K_s:
                    game_mode = "set_to_map"
                elif key == pygame.K_RIGHT:
                    if r_screen == "stats":
                        r_screen = "inv"
                    elif r_screen == "inv":
                        r_screen = "supports"
                    elif r_screen == "supports":
                        r_screen = "stats"
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
                    self.try_to_move((cursor_x, cursor_y))
                elif key == pygame.K_w:
                    any_selected = False
                    for actor in self.level.actors:
                        actor.status = "idle"
                elif key == pygame.K_s:
                    if game_mode == "map":
                        for actor in self.level.actors:
                            if actor.pos == (cursor_x, cursor_y):
                                self.focus_actor = actor
                                game_mode = "r_screen"
        
        # Finish
        key_buffer = []
        if game_mode == "set_to_map":
            game_mode = "map"
        
    def draw_cursor(self):
        pygame.draw.rect(self.foreground, (254, 254, 254), (cursor_x * tile_size, cursor_y * tile_size, tile_size, tile_size >> 3))
        pygame.draw.rect(self.foreground, (254, 254, 254), (cursor_x * tile_size, cursor_y * tile_size, tile_size >> 3, tile_size))
        
    def render_console(self):
        global console_line
        
        self.menus.fill((0, 0, 0))  # Clear Menus
        pygame.draw.rect(self.menus, (254, 254, 254), (tile_size >> 1, tile_size >> 1, screen_width - tile_size, screen_height - tile_size))
        pygame.draw.rect(self.menus, (1, 1, 1), (tile_size, screen_height - tile_size - 26, screen_width - (tile_size << 1), 1))
        self.draw_text(self.console_line, (1, 1, 1), tile_size, screen_height - tile_size - 16)
        for i in range(len(self.console_history)):
            if self.console_history[i] != "":
                self.draw_text(self.console_history[i], (1, 1, 1), tile_size, tile_size + (i * 16))
                
    def render_mini_menu(self):
        pygame.draw.rect(self.menus, (64, 128, 200), (tile_size >> 1, screen_height - ((tile_size << 1) + (tile_size >> 1)), tile_size << 2, tile_size << 1))
        for actor in self.level.get_actors():
            if actor.get_pos()[0] == (cursor_x - screen_x) and actor.get_pos()[1] == (cursor_y - screen_y):
                self.draw_text((actor.NAME + " " + str(actor.UID)), (254, 254, 254), tile_size, screen_height - ((tile_size << 1) + (tile_size >> 1)))
                    # TEMP4
        self.draw_text(self.level.get_map_terrain()[cursor_y - screen_y][cursor_x - screen_x], (254, 254, 254), tile_size, screen_height - (tile_size << 1))
        
    def render_movement_graph(self):
        global any_selected
        global tile_size
        global cursor_x
        global cursor_y
        global screen_x
        global screen_y
        
        movement = 0
        movement_type = 0
        pos = (0, 0)
        
        if any_selected:
            for actor in self.level.actors:
                if actor.status == "selected":
                    movement = actor.movement
                    movement_type = actor.movement_type
                    pos = actor.pos
            
            for x in range(-movement, movement):
                for y in range(-movement, movement):
                    if -movement <= x + y <= movement:
                        self.foreground.blit(self.blue_square, ((actor.pos[0] + x + screen_x) * tile_size, (actor.pos[1] + y + screen_y) * tile_size))
        
    def try_to_move(self, pos):
        '''
        global any_selected
        if any_selected:
            for actor in self.level.actors:
                if actor.status == "selected":
                    print("Moving from", actor.pos, "to", (cursor_x, cursor_y))
                    actor.set_pos((pos[0] - screen_x, pos[1] - screen_y))
                    actor.status == "idle"
                    any_selected = False
        else:
            for actor in self.level.actors:
                if actor.pos == (cursor_x, cursor_y):
                    actor.status = "selected"
                    any_selected = True
                    '''
        
        # Check if hasn't moved this turn
        # Produce an array of squares they can move to
        #
        
    def render_r_screen(self):
        global screen_width, screen_height
        # pygame.draw.rect(self.menus, (24, 155, 13), (0, 0, screen_width, screen_height))
        pygame.draw.rect(self.menus, (64, 128, 200), (200, 44, 266, 204)) # Big box on the right
        pygame.draw.rect(self.menus, (64, 128, 200), (16, 240, 170, 64)) # Small bottom-left box
        self.menus.blit(self.focus_actor.MUG, (8, 8))
        
        self.draw_text("{}".format(self.focus_actor.CLASS), (255, 255, 255), 16, 240)
        self.draw_text("LVL: {} EXP: {}".format(self.focus_actor.LEVEL.rjust(2, ' '), self.focus_actor.EXP).rjust(2, ' '), (255, 255, 255), 16, 260)
        self.draw_text("HP: {}/{}".format(self.focus_actor.CURRENT_HP.rjust(2, ' '), self.focus_actor.MAX_HP).rjust(2, ' '), (255, 255, 255), 16, 280)
        
        self.draw_text("STR: {}   MOVE: {}".format(self.focus_actor.STR.rjust(2, ' '), self.focus_actor.MOVE).rjust(2, ' '), (255, 255, 255), 216, 52)
        self.draw_text("SKL: {}    CON: {}".format(self.focus_actor.SKL.rjust(2, ' '), self.focus_actor.CON).rjust(2, ' '), (255, 255, 255), 216, 74)
        self.draw_text("SPD: {}    AID: {}".format(self.focus_actor.SPD.rjust(2, ' '), self.focus_actor.AID).rjust(2, ' '), (255, 255, 255), 216, 96)
        
        if self.r_screen == "stats":
            self.draw_text("STR: {}   MOVE: {}".format(self.focus_actor.STR.rjust(2, ' '), self.focus_actor.MOVE).rjust(2, ' '), (255, 255, 255), 216, 52)
            self.draw_text("SKL: {}    CON: {}".format(self.focus_actor.SKL.rjust(2, ' '), self.focus_actor.CON).rjust(2, ' '), (255, 255, 255), 216, 74)
            self.draw_text("SPD: {}    AID: {}".format(self.focus_actor.SPD.rjust(2, ' '), self.focus_actor.AID).rjust(2, ' '), (255, 255, 255), 216, 96)
            self.draw_text("LUK: {}    TRV: {}".format(self.focus_actor.LUK.rjust(2, ' '), self.focus_actor.TRV).rjust(2, ' '), (255, 255, 255), 216, 118)
            self.draw_text("DEF: {}   AFFN: {}".format(self.focus_actor.DEF.rjust(2, ' '), self.focus_actor.AFFIN).rjust(2, ' '), (255, 255, 255), 216, 140)
            self.draw_text("RES: {}   COND: {}".format(self.focus_actor.RES.rjust(2, ' '), self.focus_actor.COND).rjust(2, ' '), (255, 255, 255), 216, 162)
        elif self.r_screen == "inv":
            self.draw_text("STR: {}   MOVE: {}".format(self.focus_actor.STR.rjust(2, ' '), self.focus_actor.MOVE).rjust(2, ' '), (255, 255, 255), 216, 52)
        elif self.r_screen == "supports":
            pass
    
    def render(self):
        global map_tiles
        global tile_size
        global screen_x
        global screen_y
        global game_mode
        # Seems to be running every frame. Destroy and rebuild background every frame?
        self.screen.fill((0, 0, 0))  # Clear screen
        self.midground.fill((0, 0, 0))
        self.foreground.fill((0, 0, 0))  # Clear foreground
        self.menus.fill((0, 0, 0))  # Clear Menus
        self.console_screen.fill((0, 0, 0))  # Clear Menus
        self.sprites.clear(self.foreground, self.background)
        
        # Draw background
        for x, row in enumerate(self.level.get_map()):
            for y, tile in enumerate(row):
               self.screen.blit(tile, ((screen_x + x) * tile_size, (screen_y + y) * tile_size))
        
        # Draw Foreground elements
        self.sprites.update(self.foreground)
        self.sprites.draw(self.foreground)
            
        # Draw Movement Graph
        self.render_movement_graph()
            
        # Draw Menu
        if input_mode != "console" and game_mode != "r_screen":
            self.render_mini_menu()
            
        # Draw Cursor
        self.draw_cursor()
            
        if game_mode == "r_screen":
            self.render_r_screen()
        
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
-Finish adding in all the buttons
-Make the entire thing OOP and remove all the global variables
-Bugtest

### TO DO
- Add sprites
- Add Loader for terrain, actors, characters, classes
- Add class for terrain, character (maybe?), class
- Add movement + combat

'''
