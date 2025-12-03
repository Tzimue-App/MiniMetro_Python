import pygame

class Train:

    def __init__(self, line):
        self.line = line
        self.pos = line.stations[0].pos.copy()
        self.target_station_index = 1
        self.speed = 1
        self.passengers = []
        self.direction = 1

    def draw (self, screen):
        pygame.draw.circle(screen, self.line.color, self.pos, 5)
    
    def update(self):
        target_station = self.line.stations[self.target_station_index]
        target_pos = target_station.pos.copy()
        
        direction_vector = target_pos - self.pos
        distance_remaining = direction_vector.length()

        if distance_remaining > 0: 
            
            if self.speed >= distance_remaining:
                self.pos = target_pos
                self._change_target()
            else:
                move_vector = direction_vector.normalize() * self.speed
                self.pos += move_vector

    def _change_target(self):
        
        num_stations = len(self.line.stations)

        if self.target_station_index == num_stations - 1:
            self.direction = -1
        
        elif self.target_station_index == 0:
            self.direction = 1
        
        self.target_station_index += self.direction
