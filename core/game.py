import pygame
import random

from .constants import *
from entities.station import Station
from entities.line import Line
from entities.train import Train

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
        self.SPAWN_INTERVAL = 2000

        self._initialize_map()

    def _initialize_map(self):
        shapes = ['circle', 'square', 'triangle'] 
        
        self.stations.append(Station(100, 100, random.choice(shapes)))
        self.stations.append(Station(300, 500, random.choice(shapes)))
        self.stations.append(Station(500, 250, random.choice(shapes)))
        self.stations.append(Station(700, 200, random.choice(shapes)))

        for _ in range(5):
            self.stations[0].add_passenger(1) 

        initial_stations = [self.stations[0], self.stations[1], self.stations[3]]
        self.lines.append(Line(initial_stations))

        self.trains.append(Train(self.lines[0]))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.last_passenger_spawn_time + self.SPAWN_INTERVAL:
            random.choice(self.stations).add_passenger(1)
            self.last_passenger_spawn_time = current_time

        for train in self.trains:
            train.update()  

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
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
                            self.drawing_line = True
                            self.current_line_stations = [cliked_station]

                        elif self.drawing_line:
                            
                            if cliked_station != self.current_line_stations[-1]:
                                
                                self.current_line_stations.append(cliked_station)

                                self.lines.append(Line(self.current_line_stations))
                                
                                self.current_line_stations = []
                                self.drawing_line = False
                                
                    else:
                        self.drawing_line = False
                        self.current_line_stations = []

                elif event.button == 1:
                    if not self.drawing_line and cliked_station:
                        cliked_station.add_passenger(1)
            
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for line in self.lines:
            line.draw(self.screen)

        if self.drawing_line:
            start_pos = self.current_line_stations[-1].pos
            end_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.screen, WHITE, start_pos, end_pos, 1)

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