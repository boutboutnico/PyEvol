import pygame

from scene_base import SceneBase
from color import *


class InfoScene(SceneBase):

    def __init__(self, world):
        self.font = pygame.font.SysFont("monospace", 15)
        self.world = world

    def process_input(self, events, key_pressed):
        pass

    def compute(self):
        pass

    def render(self, surface):
        surface.fill(LIGHT_BLUE)

        zoom_label = self.font.render("Zoom: {:2.2f}".format(self.world.zoom), 1, BLACK)
        surface.blit(zoom_label, (10, 10))

        zoom_label = self.font.render("Power: {:2.2f}/{:2.2f}".format(self.world.creatures[0].left_power, self.world.creatures[0].right_power), 1, BLACK)
        surface.blit(zoom_label, (10, 30))

        zoom_label = self.font.render("Inputs: {}".format(self.world.creatures[0].nn.inputs), 1, BLACK)
        surface.blit(zoom_label, (10, 50))

        zoom_label = self.font.render("Outputs: {}".format(self.world.creatures[0].nn.outputs), 1, BLACK)
        surface.blit(zoom_label, (10, 70))

    def terminate(self):
        pass
