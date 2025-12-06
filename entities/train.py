import pygame

from core.constants import WHITE, SHAPE_TYPE

class Train:

    def __init__(self, line):
        self.line = line
        
        self.pos = line.nodes[0].copy() 
        
        self.target_index = 1
        self.speed = 1
        self.passengers = {shape: [] for shape in SHAPE_TYPE} 
        self.capacity = 5
        self.direction = 1

    def draw (self, screen):
        pygame.draw.circle(screen, self.line.color, (int(self.pos.x), int(self.pos.y)), 5)

        font = pygame.font.Font(None, 20)
        y_offset = -15
        
        total_passengers = sum(len(queue) for queue in self.passengers.values())
        text = font.render(str(total_passengers), True, WHITE)
        screen.blit(text, (self.pos.x + 8, self.pos.y + y_offset))
        
    def update(self):
        target_pos = self.line.nodes[self.target_index].copy()
        
        direction_vector = target_pos - self.pos
        distance_remaining = direction_vector.length()

        if distance_remaining > 0: 
            
            if self.speed >= distance_remaining:
                self.pos = target_pos
                
                actual_station = self._get_actual_station(target_pos) 
                
                if actual_station:
                    self._handle_station_stop(actual_station) 

                self._change_target()
                
            else:
                move_vector = direction_vector.normalize() * self.speed
                self.pos += move_vector

    def _get_actual_station(self, position):
        for station in self.line.stations: 
            if station.pos == position:
                return station
        return None 

    def _handle_station_stop(self, station):
        station_target_type = station.shape_type

        self.passengers[station_target_type] = []
            
        current_count = sum(len(queue) for queue in self.passengers.values())
        space_available = self.capacity - current_count
        
        if space_available > 0:
            new_passengers = station.board_passengers(space_available, self._get_boarding_priority())
            
            for p in new_passengers:
                self.passengers[p.shape_type].append(p)
    
    def _change_target(self):
        
        num_positions = len(self.line.nodes)

        if self.target_index == num_positions - 1:
            self.direction = -1
        
        elif self.target_index == 0:
            self.direction = 1
        
        self.target_index += self.direction

    def _get_boarding_priority(self):
        
        stations = self.line.stations
        num_stations = len(stations)
        
        boarding_priority_shape = []

        current_station_index = 0
        current_pos = self.line.nodes[self.target_index]
        for i, station in enumerate(stations):
            if station.pos == current_pos:
                current_station_index = i
                break
        
        if self.direction == 1:
            range_stations = range(current_station_index + 1, num_stations, 1)
        else:
            range_stations = range(current_station_index - 1, -1, -1)
            
        for i in range_stations:
            station = stations[i]
            if station.shape_type not in boarding_priority_shape:
                boarding_priority_shape.append(station.shape_type)
        
        return boarding_priority_shape