# INSTRUCTIONS
# ------------
# Control the ship using arrow keys or W/A/S/D
# Pressing space fires a shot to the other end of the screen
# Pressing escape exits the game

import pathlib
import arcade
import random

IMAGE_WIDTH = 820
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 410
SCREEN_TITLE = "Project 1"
PLAYER_PATH = pathlib.Path.cwd() / "Resources" / "Player.png"
ENEMY_PATH = pathlib.Path.cwd() / "Resources" / "Enemy1.png"
PLAYER_SHOT_PATH = pathlib.Path.cwd() / "Resources" / "PlayerShot.png"
ENEMY_SHOT_PATH = pathlib.Path.cwd() / "Resources" / "EnemyShot1.png"
BACKGROUND_PATH = pathlib.Path.cwd() / "Resources" / "Background.png"
PLAYER_SHOT_SOUND_PATH = pathlib.Path.cwd() / "Resources" / "PlayerShot.wav"
# ENEMY_SHOT_SOUND_PATH = pathlib.Path.cwd() / "Resources" / "EnemyShot1.wav"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        # sprite lists to manage shots and background
        self.enemy_list = None
        self.shot_list = None
        self.background_list = arcade.SpriteList()
        # player speed, never changes
        self.PLAYER_SPEED = 200
        # flags for movement logic in on_update
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        # timers
        self.shot_timer = 0
        self.enemy_timer = 0
        # pathlib to ensure working directory regardless of platform
        self.laser_sound = arcade.Sound(PLAYER_SHOT_SOUND_PATH)
        self.player = arcade.Sprite(PLAYER_PATH)
        self.newEnemy = None
        self.shot = None
        self.background1 = arcade.Sprite(BACKGROUND_PATH, center_x=IMAGE_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.background2 = arcade.Sprite(BACKGROUND_PATH, center_x=SCREEN_WIDTH+IMAGE_WIDTH/2, center_y=SCREEN_HEIGHT/2)

        # set up infinite scrolling background logic
        self.background1.change_x = -3
        self.background_list.append(self.background1)
        self.background2.change_x = -3
        self.background_list.append(self.background2)

    def setup(self):
        # reset variables so player can restart
        self.shot_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player.center_x = 100
        self.player.center_y = SCREEN_HEIGHT / 2
        self.shot_timer = 1
        self.enemy_timer = 5
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.shot_timer = 1

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        self.player.draw()
        self.enemy_list.draw()
        self.shot_list.draw()

    def on_update(self, delta_time):
        # check the flags for movement and update accordingly
        if self.right:
            self.player.center_x += self.PLAYER_SPEED * delta_time
        if self.left:
            self.player.center_x -= self.PLAYER_SPEED * delta_time
        if self.up:
            self.player.center_y += self.PLAYER_SPEED * delta_time
        if self.down:
            self.player.center_y -= self.PLAYER_SPEED * delta_time

        # prevent movement outside of the window boundaries
        if self.player.center_x > SCREEN_WIDTH - 38:
            self.player.center_x -= self.PLAYER_SPEED * delta_time
        if self.player.center_x < 38:
            self.player.center_x += self.PLAYER_SPEED * delta_time
        if self.player.center_y > SCREEN_HEIGHT - 17:
            self.player.center_y -= self.PLAYER_SPEED * delta_time
        if self.player.center_y < 17:
            self.player.center_y += self.PLAYER_SPEED * delta_time

        # update timers and sprite lists
        self.enemy_timer += delta_time
        self.enemy_list.update()
        self.shot_timer += delta_time
        self.shot_list.update()

        # spawning enemies
        if self.enemy_timer >= 5:
            self.enemy_timer = 0
            self.newEnemy = Enemy(ENEMY_PATH, scale=.75)
            self.newEnemy.center_x = 880
            self.newEnemy.center_y = random.randint(27, SCREEN_HEIGHT-27)
            self.enemy_list.append(self.newEnemy)

        # side-scrolling background logic
        if self.background1.left <= -820:
            self.background1.center_x = SCREEN_WIDTH + IMAGE_WIDTH//2
        if self.background2.left <= -820:
            self.background2.center_x = SCREEN_WIDTH + IMAGE_WIDTH//2

        self.background_list.update()

    def on_key_press(self, symbol, modifiers):
        # check for keyboard input on arrows or W/A/S/D
        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.right = True
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.left = True
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.up = True
        if symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.down = True

        if symbol == arcade.key.SPACE and self.shot_timer >= 1:
            self.shot_timer = 0
            self.laser_sound.play()
            self.shot = Shot(PLAYER_SHOT_PATH, 10)
            self.shot.center_x = self.player.center_x + 76
            self.shot.center_y = self.player.center_y
            self.shot_list.append(self.shot)

        if symbol == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, symbol, modifiers):
        # check for keyboard release on arrows or W/A/S/D
        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.right = False
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.left = False
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.up = False
        if symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.down = False


class Shot(arcade.Sprite):
    def __init__(self, filename, x):
        super().__init__(filename)
        self.speed = x

    def update(self):
        self.center_x += self.speed
        if self.center_x > SCREEN_WIDTH or self.center_x < 0:
            self.kill()


class Enemy(arcade.Sprite):
    SPEED = 1.5

    def update(self):
        # enter screen then move up/down, reversing movement when hitting window boundaries
        if self.center_x > 770:
            self.center_x -= 1
        else:
            self.center_y += self.SPEED
            if self.center_y > SCREEN_HEIGHT - 27 or self.center_y < 27:
                self.SPEED *= -1


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
