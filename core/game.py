import pygame
import random

from .constants import *
from entities.station import Station
from entities.line import Line
from entities.train import Train
from entities.passenger import Passenger

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        
        self.stations = []
        self.lines = []
        self.trains = []

        self.drawing_line = False
        self.current_line_stations = []

        self.last_passenger_spawn_time = pygame.time.get_ticks()
        self.last_money_time = pygame.time.get_ticks()
        self.last_train_time = pygame.time.get_ticks()
        self.SPAWN_INTERVAL = 2000
        self.MONEY_INTERVAL = 10000
        self.TRAIN_INTERVAL = 30000

        self.money = 5

        self._initialize_map()

    def _initialize_map(self):
        
        self.stations.append(Station(3, 3, random.choice(SHAPE_TYPE)))
        self.stations.append(Station(7, 4, random.choice(SHAPE_TYPE)))
        self.stations.append(Station(10, 12, random.choice(SHAPE_TYPE)))
        self.stations.append(Station(9, 11, random.choice(SHAPE_TYPE)))

        for _ in range(5):
            self.stations[0].add_passenger(Passenger(random.choice(SHAPE_TYPE))) 

        initial_positions = [self.stations[0].pos, self.stations[1].pos, self.stations[3].pos]
        
        initial_stations_objects = [self.stations[0], self.stations[1], self.stations[3]] 
        
        self.lines.append(Line(initial_positions, initial_stations_objects))
        
        self.trains.append(Train(self.lines[0]))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.last_passenger_spawn_time + self.SPAWN_INTERVAL:
            random.choice(self.stations).add_passenger(Passenger(random.choice(SHAPE_TYPE)))
            self.last_passenger_spawn_time = current_time

        if current_time > self.last_money_time + self.MONEY_INTERVAL:
            self.money += 1
            self.last_money_time = current_time

            if current_time > self.last_train_time + self.TRAIN_INTERVAL:
                if self.lines:
                    self.trains.append(Train(random.choice(self.lines)))
                    self.last_train_time = current_time
                    print("New Train")
        
        for station in self.stations:
            station.update()

        for train in self.trains:
            self.money += train.update()  

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.money > COST_NEW_LINE:

                    if self.drawing_line and self.current_line_stations:
                        
                        last_point_pos = self.current_line_stations[-1]
                        
                        is_closing_on_station = False
                        
                        stations_on_new_line = [] 
                        
                        for point_pos in self.current_line_stations:
                            for station in self.stations:
                                if station.pos == point_pos:
                                    stations_on_new_line.append(station)
                                    
                                    if point_pos == last_point_pos:
                                        is_closing_on_station = True
                                        
                                    break
                        
                        
                        if is_closing_on_station:
                            if len(self.current_line_stations) >= 2:
                                
                                positions_list = self.current_line_stations 
                                
                                stations_list = stations_on_new_line
                                
                                self.lines.append(Line(positions_list, stations_list))
                                self.trains.append(Train(self.lines[-1]))
                                self.money -= COST_NEW_LINE
                                
                            else:
                                print("Ligne annulée : Pas assez de segments.")
                                
                            self.current_line_stations = []
                            self.drawing_line = False

                            return
                else:
                    print("Not enough money")

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.math.Vector2(event.pos)
                cliked_station = None

                for station in self.stations:
                    if mouse_pos.distance_to(station.pos) < station.radius:
                        cliked_station = station
                        break
                
                if event.button == 3:
                    
                    if cliked_station:
                        if not self.drawing_line:
                            self.current_line_stations = [cliked_station.pos]
                            self.drawing_line = True

                        elif self.drawing_line:
                            
                            if cliked_station.pos != self.current_line_stations[-1]:
                                
                                self.current_line_stations.append(cliked_station.pos)
                            
                    else:
                        if self.drawing_line:
                            if self.drawing_line:
                            
                                grid_x = int(mouse_pos.x // GRID_SIZE)
                                grid_y = int(mouse_pos.y // GRID_SIZE)
                                
                                center_x = grid_x * GRID_SIZE + GRID_SIZE // 2
                                center_y = grid_y * GRID_SIZE + GRID_SIZE // 2
                                
                                new_pos = pygame.math.Vector2(center_x, center_y)

                                if new_pos != self.current_line_stations[-1]:
                                    self.current_line_stations.append(new_pos)

                elif event.button == 1:
                    if not self.drawing_line and cliked_station:
                        cliked_station.add_passenger(Passenger(random.choice(SHAPE_TYPE)))
                    elif self.drawing_line:
                        #click gauche annule le dessin
                        self.drawing_line = False
                        self.current_line_stations = []
            
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        money_font = pygame.font.Font(None, 18)
        money_text = money_font.render(f"money : {self.money}", True, WHITE)
        self.screen.blit(money_text, (15, 15))


        
        for x in range(0, SCREEN_WIDTH + 1, GRID_SIZE):
            start_pos = (x, 0)
            end_pos = (x, SCREEN_HEIGHT)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, 1)

        for y in range(0, SCREEN_HEIGHT + 1, GRID_SIZE):
            start_pos = (0, y)
            end_pos = (SCREEN_WIDTH, y)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, 1)

        for line in self.lines:
            line.draw(self.screen)

        if self.drawing_line and len(self.current_line_stations) > 0:
            
            for i in range(len(self.current_line_stations) - 1):
                start_pos = self.current_line_stations[i]
                end_pos = self.current_line_stations[i + 1]
                pygame.draw.line(self.screen, WHITE, start_pos, end_pos, 4)

            last_fixed_pos = self.current_line_stations[-1]
            current_mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.screen, WHITE, last_fixed_pos, current_mouse_pos, 4)

        for station in self.stations:
            station.draw(self.screen)

        for train in self.trains:
            train.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)