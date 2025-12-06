import pygame
import random

class Line:
    def __init__(self, nodes: list[pygame.math.Vector2], stations_objects: list):
        self.nodes = nodes
        self.stations = stations_objects
        
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.width = 4

    def add_station(self, node):
        self.nodes.append(node)

    def draw(self, screen):
        if len(self.nodes) >= 2:
            
            for i in range(len(self.nodes) - 1): 
                station_a = self.nodes[i]
                station_b = self.nodes[i+1]

                pygame.draw.line(
                    screen, 
                    self.color,
                    station_a, 
                    station_b, 
                    self.width
                )
    def update():
        return