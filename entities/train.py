import pygame

from core.constants import WHITE, SHAPE_TYPE

class Train:

    def __init__(self, line):
        self.line = line
        self.pos = line.stations[0].pos.copy()
        self.target_station_index = 1
        self.speed = 1
        self.passengers = {shape: [] for shape in SHAPE_TYPE} 
        self.capacity = 5
        self.direction = 1

    def draw (self, screen):
        pygame.draw.circle(screen, self.line.color, self.pos, 5)

        passenger_counts = {shape: len(queue) for shape, queue in self.passengers.items()}

        font = pygame.font.Font(None, 24)
        
        y_offset = -10
        for shape, count in passenger_counts.items():
            text = font.render(f"{shape[0]}: {count}", True, WHITE) # Ex: C: 2
            screen.blit(text, (self.pos.x + 5, self.pos.y + y_offset))
            y_offset -= 15
        
    def update(self):
        target_station = self.line.stations[self.target_station_index]
        target_pos = target_station.pos.copy()
        
        direction_vector = target_pos - self.pos
        distance_remaining = direction_vector.length()

        if distance_remaining > 0: 
            
            if self.speed >= distance_remaining:
                self.pos = target_pos
                station_target_type = target_station.shape_type

                for shape in SHAPE_TYPE:
                    if shape == station_target_type:
                        self.passengers[shape] = []
                    else:
                        pass 

                current_count = sum(len(queue) for queue in self.passengers.values())
                space_available = self.capacity - current_count

                if space_available > 0:
                    new_passengers = target_station.board_passengers(space_available)
                    
                    for p in new_passengers:
                        if p.shape_type in self.passengers:
                            self.passengers[p.shape_type].append(p)
                        else:
                            print(f"Erreur: Passager de type {p.shape_type} inconnu") 

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
