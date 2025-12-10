import pygame

from core.constants import WHITE, SHAPE_TYPE

class Train:

    def __init__(self, line):
        self.line = line

        self.nodes = line.nodes[:]
        self.stations = line.stations[:]
        
        self.pos = line.nodes[0].copy() 
        
        self.target_index = 1
        self.speed = 1
        self.passengers = {shape: [] for shape in SHAPE_TYPE} 
        self.capacity = 5

    def draw (self, screen):
        pygame.draw.circle(screen, self.line.color, (int(self.pos.x), int(self.pos.y)), 5)

        
        font = pygame.font.Font(None, 18)
        y_offset = -30
        
        passenger_counts = {shape: len(queue) for shape, queue in self.passengers.items()}
        
        for shape, count in passenger_counts.items():
            if count > 0:
                text = font.render(f"{shape[0].upper()}: {count}", True, WHITE)
                
                screen.blit(text, (self.pos.x + 8, self.pos.y + y_offset))
                y_offset += 15
        
    def update(self):
        target_pos = self.nodes[self.target_index].copy()
        
        direction_vector = target_pos - self.pos
        distance_remaining = direction_vector.length()

        points = 0

        if distance_remaining > 0: 
            
            if self.speed >= distance_remaining:
                self.pos = target_pos
                
                actual_station = self._get_actual_station(target_pos) 

                self._change_target()
                
                if actual_station:
                    points = self._handle_station_stop(actual_station) 
                
            else:
                move_vector = direction_vector.normalize() * self.speed
                self.pos += move_vector
        
        return points

    def _get_actual_station(self, position):
        for station in self.stations: 
            if station.pos == position:
                return station
        return None 

    def _handle_station_stop(self, station):
        station_target_type = station.shape_type

        passenger_unboard = len(self.passengers[station_target_type])
        self.passengers[station_target_type] = []

        priority_shapes, futures_stations = self._get_boarding_priority()

        stale_passengers = self._get_stale_passengers(futures_stations)

        for stale_passenger in stale_passengers:
            self.passengers[stale_passenger.shape_type].remove(stale_passenger)
            
        current_count = sum(len(queue) for queue in self.passengers.values())
        space_available = self.capacity - current_count
        
        if space_available > 0:
            
            boarding_candidates = station.get_boarding_candidates(priority_shapes)
            
            passengers_to_board = []
            
            for p in boarding_candidates:
                if space_available <= 0:
                    break
                
                is_on_route = any(p.shape_type == fs.shape_type for fs in futures_stations)
                
                if is_on_route:
                    passengers_to_board.append(p)
                    space_available -= 1
                
            for p in passengers_to_board:
                self.passengers[p.shape_type].append(p)
                station.remove_passenger(p) 

        return passenger_unboard
    
    def _change_target(self):

        if self.target_index == len(self.line.nodes) - 1:
            self.nodes.reverse()
            self.stations.reverse()
            self.target_index = 0
        
        self.target_index += 1

    def _get_boarding_priority(self):
        
        stations = self.stations
        num_stations = len(stations)
        
        boarding_priority_shape = []
        future_stations = []
        
        current_station_index = -1
        current_pos = self.pos 
        
        for i, station in enumerate(stations):
            if station.pos == current_pos:
                current_station_index = i
                break
        
        if current_station_index == -1:
            print("Erreur: Index de station actuel non trouvé.")
            return [], []
        
        range_stations = range(current_station_index + 1, num_stations)
            
        for i in range_stations:
            station = stations[i] 
            future_stations.append(station)  
            if station.shape_type not in boarding_priority_shape:
                boarding_priority_shape.append(station.shape_type)
        
        print(boarding_priority_shape)
        return boarding_priority_shape,  future_stations
    
    def _get_stale_passengers(self, futures_stations):

        accessible_shape = {fs.shape_type for fs in futures_stations}

        stale_passengers = []

        for passenger_list in self.passengers.values():
            for p in passenger_list:

                if p.shape_type not in accessible_shape:
                    stale_passengers.append(p)
        return stale_passengers