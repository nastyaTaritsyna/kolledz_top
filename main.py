import arcade
import random

import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

# размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# заголовок экрана
SCREEN_TITLE = 'Космический шутер'

# масштаб игрока
SPRITE_SCALING_PLAYER = 0.1
# масштаб выстрела
SPRITE_SCALING_LASER = 0.3
# масштаб врага
SPRITE_SCALING_ENEMY = 0.5

class Enemy(arcade.Sprite):
   def __init__(self):
       super().__init__(':resources:images/space_shooter/playerShip3_orange.png', SPRITE_SCALING_ENEMY, angle=180)
       self.change_y = 1

   def update(self):
       self.center_y -= self.change_y

class Laser(arcade.Sprite):
   def __init__(self):
       super().__init__(':resources:images/space_shooter/laserBlue01.png', SPRITE_SCALING_LASER, angle=90)
       self.change_y = 2

   def update(self):
       self.center_y += self.change_y
       if self.bottom >= SCREEN_HEIGHT:
           self.kill()


class Player(arcade.Sprite):
   def __init__(self):
       super().__init__('space-shuttle.png', SPRITE_SCALING_PLAYER)
       self.center_x = SCREEN_WIDTH // 2
       self.center_y = 30


class Game(arcade.Window):
   def __init__(self):
       super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

       self.set_mouse_visible(False)

       # добавляем фон
       self.background_texture = arcade.load_texture(':resources:images/backgrounds/stars.png')

       # переменная для игрока
       self.player_sprite = None

       # переменные для выстрела
       self.laser_sprite = None
       self.laser_sprite_list = None

       # переменная для звука
       self.sound = None
       self.music = None

       # переменная для врагов
       self.enemy_sprite = None
       self.enemy_sprite_list = None

       self.status = True

   def setup(self):
       self.laser_sprite_list = arcade.SpriteList()
       self.enemy_sprite_list = arcade.SpriteList()

       for i in range(1, 31):
           self.enemy_sprite = Enemy()
           self.enemy_sprite.center_x = random.randint(0, SCREEN_WIDTH)
           self.enemy_sprite.center_y = SCREEN_HEIGHT + i * 50
           self.enemy_sprite_list.append(self.enemy_sprite)

   def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
       pass

   def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
       pass

   def on_update(self, delta_time: float):
       if self.status:
           self.laser_sprite_list.update()
           self.enemy_sprite_list.update()
           for laser in self.laser_sprite_list:
               shot_list = arcade.check_for_collision_with_list(laser, self.enemy_sprite_list)
               if shot_list:
                   laser.kill()
                   for enemy in shot_list:
                       enemy.kill()

       if not self.enemy_sprite_list:
           self.status = False
           arcade.pause(1)
           arcade.close_window()

   def on_draw(self):
       self.clear()
       # отрисовываем фон
       arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                     self.background_texture)

       # отрисовываем лазер
       self.laser_sprite_list.draw()

       # отрисовываем врагов
       self.enemy_sprite_list.draw()


if __name__ == '__main__':
   game = Game()
   game.setup()
   arcade.run()

