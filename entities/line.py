import pygame
import random

class Line:
    def __init__(self, stations: list):
        self.stations = stations 
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.width = 4

    def add_station(self, station):
        self.stations.append(station)

    def draw(self, screen):
        if len(self.stations) >= 2:
            
            for i in range(len(self.stations) - 1): 
                station_a = self.stations[i]
                station_b = self.stations[i+1]
                
                pygame.draw.line(
                    screen, 
                    self.color,
                    station_a.pos, 
                    station_b.pos, 
                    self.width
                )
    def update():
        return