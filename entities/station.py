import pygame
from core.constants import STATION_RADIUS, WHITE

class Station:
    def __init__(self, x, y, shape_type):
        self.pos = pygame.math.Vector2(x, y)
        self.shape_type = shape_type
        self.passengers = []
        self.radius = STATION_RADIUS
        
    def add_passenger(self, passenger):
        self.passengers.append(passenger)
    
    def get_passenger_count(self):
        return self.passengers
    
    def unload_all_passenger(self):
        passengers_to_board = self.passengers
        self.passengers = []
        return passengers_to_board

    def draw(self, screen):
        match self.shape_type:
            case "circle":
                pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius, 2)
            case "square":
                pygame.draw.rect(screen, WHITE, pygame.Rect(self.pos.x, self.pos.y, 15, 15), 2)
            case "triangle":
                pygame.draw.polygon(screen, WHITE, [(int(self.pos.x), int(self.pos.y)),(int(self.pos.x+10), int(self.pos.y)),( int(self.pos.x+5), int(self.pos.y-10))],  2)
        
        font = pygame.font.Font(None, 24)
        text = font.render(str(len(self.passengers)), True, WHITE)
        screen.blit(text, (self.pos.x + self.radius + 5, self.pos.y - 10))