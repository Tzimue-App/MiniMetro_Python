import pygame

from core.constants import STATION_RADIUS, WHITE, SHAPE_TYPE

class Station:
    def __init__(self, x, y, shape_type):
        self.pos = pygame.math.Vector2(x, y)
        self.shape_type = shape_type
        self.passengers = {shape: [] for shape in SHAPE_TYPE}
        self.radius = STATION_RADIUS
        
    def add_passenger(self, passenger):
        self.passengers[passenger.shape_type].append(passenger)
    
    def board_passengers(self, max_count):
        passengers_to_board = []
        space_left = max_count

        for shape in SHAPE_TYPE:
            queue = self.passengers[shape]
            
            if space_left <= 0:
                break
            
            num_to_take = min(space_left, len(queue))
            
            passengers_to_board.extend(queue[:num_to_take])
            
            self.passengers[shape] = queue[num_to_take:]
            
            space_left -= num_to_take
            
        return passengers_to_board


    def draw(self, screen):
        match self.shape_type:
            case "circle":
                pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius, 2)
            case "square":
                pygame.draw.rect(screen, WHITE, pygame.Rect(self.pos.x, self.pos.y, 15, 15), 2)
            case "triangle":
                pygame.draw.polygon(screen, WHITE, [(int(self.pos.x), int(self.pos.y)),(int(self.pos.x+10), int(self.pos.y)),( int(self.pos.x+5), int(self.pos.y-10))],  2)
        
        total_passengers = sum(len(queue) for queue in self.passengers.values())

        font = pygame.font.Font(None, 24)
        text = font.render(str(total_passengers), True, WHITE)
        screen.blit(text, (self.pos.x + self.radius + 5, self.pos.y - 10))