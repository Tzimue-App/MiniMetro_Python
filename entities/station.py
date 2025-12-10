import pygame

from core.constants import STATION_RADIUS, WHITE, RED, SHAPE_TYPE, GRID_SIZE, LONG_WAIT_THRESHOLD

class Station:
    def __init__(self, grid_x, grid_y, shape_type):
        self.grid_pos = (grid_x, grid_y)

        center_x = grid_x * GRID_SIZE + GRID_SIZE // 2
        center_y = grid_y * GRID_SIZE + GRID_SIZE // 2

        self.pos = pygame.math.Vector2(center_x, center_y)

        self.shape_type = shape_type
        self.passengers = {shape: [] for shape in SHAPE_TYPE}
        self.radius = STATION_RADIUS

        self.is_overcrowded = False
        
    def add_passenger(self, passenger):
        self.passengers[passenger.shape_type].append(passenger)
    
    def get_boarding_candidates(self, boarding_priority_shape):
        passengers_to_board = []

        for shape in boarding_priority_shape:
            queue = self.passengers[shape]
            
            passengers_to_board.extend(queue)
            
        return passengers_to_board
    
    def remove_passenger(self, passenger):
        self.passengers[passenger.shape_type].remove(passenger)

    def draw(self, screen):

        self.is_overcrowded = False
        
        for queue in self.passengers.values():
            for passenger in queue:
                if passenger.waiting_timer > LONG_WAIT_THRESHOLD:
                    self.is_overcrowded = True
                    break
            if self.is_overcrowded:
                break
                
        station_color = RED if self.is_overcrowded else WHITE

        match self.shape_type:
            case "circle":
                pygame.draw.circle(screen, station_color, (int(self.pos.x), int(self.pos.y)), self.radius, 2)
            case "square":
                rect_size = 15
                rect_pos = (self.pos.x - rect_size / 2, self.pos.y - rect_size / 2)
                pygame.draw.rect(screen, station_color, pygame.Rect(rect_pos[0], rect_pos[1], rect_size, rect_size), 2)
            case "triangle":
                p1 = (int(self.pos.x), int(self.pos.y - 10))
                p2 = (int(self.pos.x - 10), int(self.pos.y + 5))
                p3 = (int(self.pos.x + 10), int(self.pos.y + 5))
                pygame.draw.polygon(screen, station_color, [p1, p2, p3], 2)
        
        
        font = pygame.font.Font(None, 18)
        y_offset = -40
        
        passenger_counts = {shape: len(queue) for shape, queue in self.passengers.items()}

        for shape, count in passenger_counts.items():
            if count > 0:
                text = font.render(f"{shape[0].upper()}: {count}", True, station_color) 
                
                screen.blit(text, (self.pos.x + self.radius + 5, self.pos.y + y_offset))
                y_offset += 15

    def update(self):
        for shape_type, queue in self.passengers.items():

            for passenger in queue:
                passenger.waiting_timer += 1