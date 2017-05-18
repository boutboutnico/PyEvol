import pygame
import pymunk
import numpy as np

import parameters
from scene_base import SceneBase
from camera import Camera
import color
from border import Border
from food import Food


collision_types = {"creature": 1, "food": 2, }
categories = {"border": 0x01, "creature": 0x02, "food": 0x04, }


class WorldScene(SceneBase): # needed ?

    FOOD_COUNT = 20
    COLOR_BACKGROUND = color.LIGHT_GREEN

    def __init__(self, simu_model):
        # Model
        self.simu_model = simu_model
        self.rect = simu_model.rect
        self.space = simu_model.space

        # Drawing
        self.surface = pygame.surface.Surface(self.rect.size)
        self.surface = self.surface.convert()
        self.camera = Camera(self.rect)
        self.mouse_click_pos = None

        self.border = Border(self.rect, self.space)

        # World Objects
        self.creatures = simu_model.creatures

        self.creature_selected = None
        self.best = None

        self.foods = list()
        self.add_foods(WorldScene.FOOD_COUNT)

        handler_creature_food = self.space.add_collision_handler(
            collision_types["creature"],
            collision_types["food"])

        handler_creature_food.pre_solve = self.creature_eat_food
        handler_creature_food.data['creatures'] = self.creatures
        handler_creature_food.data['foods'] = self.foods

    def __del__(self):
        for f in self.foods:
            self.space.remove(f.shape, f.body)

        if self.best:
            self.best.is_best = False

        if self.creature_selected:
            self.creature_selected.is_selected = False

    @staticmethod
    def creature_eat_food(arbiter, space, data):
        creature_shape = arbiter.shapes[0]
        food_shape = arbiter.shapes[1]

        c = next((c for c in data['creatures'] if c.shape == creature_shape), None)
        f = next((f for f in data['foods'] if f.shape == food_shape), None)

        if c and f:
            c.eat(f)

            if not f.calories > 0:
                space.remove(food_shape, food_shape.body)
                data['foods'].remove(f)
        else:
            # pass
            print("creature_eat_food error {} {}".format(c, f))
        return False #Workaround to emulate food.shape.sensor=True

    def add_foods(self, n):
        for i in range(0, n):
            pos = (np.random.randint(0, self.rect.width), np.random.randint(0, self.rect.height))
            self.foods.append(Food(pos, self.space))

    def process_input(self, events, key_pressed):

        self.camera.process_input(events)

        if self.creature_selected:
            self.creature_selected.process_inputs(events, key_pressed)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.creature_selected:
                        if not self.creature_selected.is_human_controlled:
                            self.creature_selected.is_human_controlled = True
                        else:
                            self.creature_selected.is_human_controlled = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_click_pos = pygame.mouse.get_pos()

    def compute(self):

        if self.mouse_click_pos:
            creature_clicked = [c for c in self.creatures if c.rect.collidepoint(self.mouse_click_pos)]
            self.mouse_click_pos = None

            if creature_clicked:
                if not self.creature_selected:
                    self.creature_selected = creature_clicked[-1]
                    self.creature_selected.is_selected = True
                else:
                    self.creature_selected.is_selected = False
                    self.creature_selected = creature_clicked[-1]
                    self.creature_selected.is_selected = True
            else:
                if self.creature_selected:
                    self.creature_selected.is_selected = False
                    self.creature_selected = None

        # Creatures
        for creature in self.creatures:
            creature.compute(self.foods)

        _max = 0
        for creature in self.creatures:
            if creature.food > _max:
                _max = creature.food
                if self.best:
                    self.best.is_best = False
                self.best = creature
                self.best.is_best = True

        # Delete depleted foods
        # self.foods = [f for f in self.foods if f.calories > 0]

        # A add missing foods
        self.add_foods(WorldScene.FOOD_COUNT - len(self.foods))

        self.simu_model.space.step(1.0 / parameters.FPS)
        # self.simu_model.space.step(1 / self.simu_model.clock.get_fps())

    def render(self, surface):

        # Background
        self.surface.fill(WorldScene.COLOR_BACKGROUND)
        # self.surface.blit(self.grass, (0, 0))

        # Food
        for food in self.foods:
            food.render(self.surface)

        # Wall
        self.border.render(self.surface)

        # Creatures
        if self.creature_selected:
            self.creature_selected.render(self.surface)

        for creature in self.creatures:
            creature.render(self.surface)

        # Blit to surface
        surface.fill(color.WHITE)
        surface.blit(pygame.transform.scale(self.surface, self.camera.area.size), self.camera.area.topleft)
