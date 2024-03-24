#200501001 Hatice Reyhan Çalışkan 220501009 Betül Canol 
import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[0] * width for _ in range(height)]

    def draw(self, screen, offset_x, offset_y):
        for y in range(self.height):
            for x in range(self.width):
                color = WHITE if (x + y) % 2 == 0 else GRAY
                pygame.draw.rect(screen, color, (offset_x + x * self.cell_size, offset_y + y * self.cell_size, self.cell_size, self.cell_size))

                #Checking if there's a warrior on the cell
                if self.grid[y][x] != 0:
                    warrior_color = self.grid[y][x]
                    pygame.draw.circle(screen, warrior_color, (offset_x + x * self.cell_size + self.cell_size // 2, offset_y + y * self.cell_size + self.cell_size // 2), self.cell_size // 3)

    def place_warrior(self, x, y, color):
        self.grid[y][x] = color

#WARRIOR CALSS
class Warrior:
    def __init__(self, name, resource, health, target, damage):
        self.name = name
        self.resource = resource
        self.health = health
        self.target = target
        self.damage = damage

    def attack_enemy(self, target):
        raise NotImplementedError("attack_enemy method must be implemented in subclass")
    
#MUHAFIZ
class Guardian(Warrior):
    def __init__(self, name):
        super().__init__(name, resource = 10, health = 80, target = None, damage = 20)
        self.range_horizontal = 1
        self.range_vertical = 1
        self.range_diagonal = 1

    def attack_enemy(self, target):
        print(f"{self.name} attacks {target.name} for {self.damage} damage.")
#OKÇU
class Archer(Warrior):
    def __init__(self, name):
        super().__init__(name, resource = 20, health = 30, target = None, damage = 60)
        self.range_horizontal = 2
        self.range_vertical = 2
        self.range_diagonal = 2

    def attack_enemy(self, target):
        print(f"{self.name} hits {target.name} for {self.damage} damage.")
#TOPÇU
class Artillery(Warrior):
    def __init__(self, name):
        super().__init__(name, resource = 50, health = 30, target = None, damage = 100)
        self.range_horizontal = 2
        self.range_vertical = 2
        self.range_diagonal = 0

    def attack_enemy(self, target):
        print(f"{self.name} hits {target.name} for {self.damage} damage.")
#ATLI
class Cavalry(Warrior):
    def __init__(self, name):
        super().__init__(name, resource = 30, health = 40, target = None, damage = 30)
        self.range_horizontal = 0
        self.range_vertical = 0
        self.range_diagonal = 3
    
    def attack_enemy(self, target):
        print(f"{self.name} hits {target.name} for {self.damage} damage.")
#CANCI
class Healer(Warrior):
    def __init__(self, name):
        super().__init__(name, resource = 10, health = 100, target = None, damage = 0)
        self.heal = 50
        self.range_horizontal = 2
        self.range_vertical = 2
        self.range_diagonal = 2

    def attack_enemy(self, target):
        print(f"{self.name} heals {target.name} for {self.heal} HP.")
        target.health += self.heal


#PLAYER CLASS
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.inventory = []
        self.resource = 200  #Starting 200 resources
        self.life = 1  # Starting 1 life

#GAME CLASS
class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.selected_x = None
        self.selected_y = None
        self.custom_size = False
        self.board_width = 8  
        self.board_height = 8  
        self.cell_size = 50  
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Board Game")
        self.font = pygame.font.Font(None, 36)
        self.offset_x = 0
        self.offset_y = 0
        self.players = []
        self.current_player_index = 0  #index of the current player
        self.warrior_placements = {}
        self.max_warrior_placements = 2
        self.player_colors = [RED, GREEN, BLUE, YELLOW]
        #PASS BUTTON??????
        self.pass_button_rect = pygame.Rect(100, 500, 100, 50)
        self.pass_button_text = "Pass"
        self.pass_button_font = pygame.font.Font(None, 36)
        self.pass_button_color = (100, 100, 100)
        self.pass_button_hover_color = (150, 150, 150)

    def get_board_size(self):
        while True:
            self.screen.fill(BLACK)
            self.render_text("Choose the size of the grid:", (100, 200))
            self.render_text("1. 8x8", (100, 250))
            self.render_text("2. 16x16", (100, 300))
            self.render_text("3. 24x24", (100, 350))
            self.render_text("4. 32x32", (100, 400))
            self.render_text("5. Custom size", (100, 450))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.board_width = self.board_height = 8
                        self.cell_size = 50
                        return
                    elif event.key == pygame.K_2:
                        self.board_width = self.board_height = 16
                        self.cell_size = 40
                        return
                    elif event.key == pygame.K_3:
                        self.board_width = self.board_height = 24
                        self.cell_size = 30
                        return
                    elif event.key == pygame.K_4:
                        self.board_width = self.board_height = 32
                        self.cell_size = 25
                        return
                    elif event.key == pygame.K_5:
                        self.custom_size = True
                        size_input = ""
                        while True:
                            self.screen.fill(BLACK)
                            size_text = self.font.render("Enter the size of the grid (between 8 and 32):", True, WHITE)
                            size_input_text = self.font.render(size_input, True, WHITE)
                            self.screen.blit(size_text, (100, 200))
                            self.screen.blit(size_input_text, (100, 250))
                            self.render_text("Press ENTER to confirm", (100, 300))
                            pygame.display.flip()

                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        try:
                                            size = int(size_input)
                                            if 8 <= size <= 32:
                                                self.board_width = self.board_height = size
                                                self.cell_size = int(400 / size)  #Adjust cell size based on the board size!!
                                                return
                                            else:
                                                size_input = ""
                                        except ValueError:
                                            size_input = ""
                                    elif event.key == pygame.K_BACKSPACE:
                                        size_input = size_input[:-1]
                                    else:
                                        size_input += event.unicode

                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                    pygame.display.flip()

    def get_player_count(self):
        while True:
            self.screen.fill(BLACK)
            self.render_text("Enter the number of players (1-4):", (100, 200))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_4:
                        return event.key - pygame.K_1 + 1

    def get_player_names(self, player_count):
        names = []
        for i in range(player_count):
            name = ""
            while True:
                self.screen.fill(BLACK)
                self.render_text(f"Enter the name for Player {i+1}:", (100, 200))
                self.render_text(name, (100, 250))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if name:    #Checks if the name is empty
                                names.append(name)
                                name = "" #Clear the name for the next player!!
                                break
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            name += event.unicode
                if len(names) > i:
                    break
        return names

    def generate_players(self, player_count):
        names = self.get_player_names(player_count)
        bot_count = max(0, 4 - player_count)
        for i in range(player_count):
            self.players.append(Player(names[i], random.choice([RED, GREEN, BLUE, YELLOW])))
        for i in range(bot_count):
            self.players.append(Player(f"Bot{i+1}", random.choice([RED, GREEN, BLUE, YELLOW])))


#RUN
    def run(self):
        self.get_board_size()
        player_count = self.get_player_count()
        self.generate_players(player_count)
        self.board = Board(self.board_width, self.board_height, self.cell_size)

        for i, player in enumerate(self.players):
            corner_x = 0 if i % 2 == 0 else self.board_width - 1
            corner_y = 0 if i < 2 else self.board_height - 1
            guardian = Guardian(f"{player.name}'s Guardian")
            self.board.place_warrior(corner_x, corner_y, player.color)
            self.warrior_placements[player] = self.warrior_placements.get(player, 0) + 1

        running = True
        selecting_warrior = False
        selected_warrior = None


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    self.handle_click(x, y)
                elif event.type == pygame.KEYDOWN:
                    if selecting_warrior:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            index = event.key - pygame.K_1
                            if index < len(self.players[self.current_player_index].inventory):
                                selected_warrior = self.players[self.current_player_index].inventory[index]
                                selecting_warrior = False
                    elif event.key == pygame.K_SPACE:
                        selecting_warrior = True

            self.screen.fill(BLACK)
            self.offset_x = (self.screen.get_width() - self.board_width * self.cell_size) // 2
            self.offset_y = (self.screen.get_height() - self.board_height * self.cell_size) // 2
            self.board.draw(self.screen, self.offset_x, self.offset_y)
            self.draw_inventories()
            
            #Displaying Turns
            current_player = self.players[self.current_player_index]
            turn_text = f"Turn: {current_player.name}"
            turn_text_surface = self.font.render(turn_text, True, WHITE)
            text_width, text_height = turn_text_surface.get_size()
            text_x = (self.screen.get_width() - text_width) // 2
            text_y = 20  #vertical position of the text
            self.screen.blit(turn_text_surface, (text_x, text_y))

            if self.selected_x is not None and self.selected_y is not None:
                pygame.draw.rect(self.screen, (255, 0, 0), (self.offset_x + self.selected_x * self.cell_size, self.offset_y + self.selected_y * self.cell_size, self.cell_size, self.cell_size), 3)

            if selecting_warrior:
                self.render_text("Select a warrior to place: ", (100, 200))
                y_offset = 250
                for i, warrior in enumerate(self.players[self.current_player_index].inventory):
                    warrior_text = f"{i + 1}. {warrior.name} (Resource: {warrior.resource})"
                    self.render_text(warrior_text, (100, y_offset))
                    y_offset += 30
            

            pygame.display.flip()
            self.clock.tick(30)

    def generate_players(self, player_count):
        names = self.get_player_names(player_count)
        bot_count = max(0, 4 - player_count)
        for i in range(player_count):
            self.players.append(Player(names[i], self.player_colors[i]))
        for i in range(bot_count):
            self.players.append(Player(f"Bot{i+1}", self.player_colors[player_count + i]))
    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

#handle click
    def handle_click(self, x, y):
        grid_x = (x - self.offset_x) // self.cell_size
        grid_y = (y - self.offset_y) // self.cell_size

        # Check if the pass button is clicked
        pass_button_area = pygame.Rect(100, 500, 100, 50)  #Define pass button area??????
        if pass_button_area.collidepoint(x, y):
            self.switch_turn()  #Skip the player's turn without placing any warriors
            return

        if 0 <= grid_x < self.board_width and 0 <= grid_y < self.board_height:
            player_index = self.current_player_index
            current_player = self.players[player_index]

            # Check if the player can place warriors in the current turn
            if self.warrior_placements.get(current_player, 0) < self.max_warrior_placements:
                # Check if the player is trying to place a warrior
                if self.selected_x is not None and self.selected_y is not None:
                    warrior = self.select_warrior(current_player)
                    if warrior is not None:
                        # Deduct resource cost from the player's inventory
                        if current_player.resource >= warrior.resource:
                            current_player.resource -= warrior.resource
                            self.board.place_warrior(grid_x, grid_y, current_player.color)
                            self.board.grid[grid_y][grid_x] = current_player.color
                            self.selected_x = None
                            self.selected_y = None
                            self.warrior_placements[current_player] = self.warrior_placements.get(current_player, 0) + 1
                            if self.warrior_placements[current_player] == self.max_warrior_placements:
                                self.switch_turn()
                        else:
                            print("Not enough resources to place the warrior.")
                else:
                    self.selected_x = grid_x
                    self.selected_y = grid_y
            else:
                self.switch_turn()
    
#WARRIOR SELECTION
    def select_warrior(self, player):
        self.screen.fill(BLACK)
        self.render_text("Select a warrior to place:", (100, 200))
        y_offset = 250
        warrior_classes = [Guardian, Archer, Artillery, Cavalry, Healer]
        for i, warrior_class in enumerate(warrior_classes):
            warrior = warrior_class(f"{player.name}'s {warrior_class.__name__}")
            if player.resource >= warrior.resource:  #Checking if the player can afford the warrior
                warrior_text = f"{i + 1}. {warrior.name} (Resource: {warrior.resource})"
                self.render_text(warrior_text, (100, y_offset))
                y_offset += 30
        
        pygame.display.flip()

        #Waiting for player input to select a warrior
        selected_warrior_index = None
        while selected_warrior_index is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_5:
                        index = event.key - pygame.K_1
                        if index < len(warrior_classes):
                            warrior_class = warrior_classes[index]
                            warrior = warrior_class(f"{player.name}'s {warrior_class.__name__}")
                            if player.resource >= warrior.resource:
                                return warrior
        return None

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, position)
    

#INVENTORY
    def draw_inventories(self):
        player_colors = [RED, GREEN, BLUE, YELLOW]
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
        corner_positions = [(10, 10),                       #Top left 
                        (screen_width - 200, 10),           #Top right 
                        (10, screen_height - 150),          #Bottom left 
                        (screen_width - 200, screen_height - 150)]  #Bottom right 

        for i, player in enumerate(self.players):
            color = player_colors[i % len(player_colors)]
            position = corner_positions[i % len(corner_positions)]
        
            #Display Player Name
            player_name_text = f"{player.name}:"
            player_name_text_surface = self.font.render(player_name_text, True, color)
            player_name_text_position = position
            self.screen.blit(player_name_text_surface, player_name_text_position)
        
            #Display Resources
            resources_text = f"Resources: {player.resource}"
            resources_text_surface = self.font.render(resources_text, True, color)
            resources_text_position = (position[0], position[1] + 30)
            self.screen.blit(resources_text_surface, resources_text_position)
        
            #Display Life
            life_text = f"Life: {player.life}"
            life_text_surface = self.font.render(life_text, True, color)
            life_text_position = (position[0], position[1] + 60)
            self.screen.blit(life_text_surface, life_text_position)


if __name__ == "__main__":
    game = Game()
    game.run()