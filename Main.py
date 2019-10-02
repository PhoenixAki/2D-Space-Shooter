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
PLAYER_PATH = str(pathlib.Path.cwd() / "Resources" / "Player.png")
ENEMY_PATH = str(pathlib.Path.cwd() / "Resources" / "Enemy1.png")
PLAYER_SHOT_PATH = str(pathlib.Path.cwd() / "Resources" / "PlayerShot.png")
ENEMY_SHOT_PATH = str(pathlib.Path.cwd() / "Resources" / "EnemyShot1.png")
BACKGROUND_PATH = str(pathlib.Path.cwd() / "Resources" / "Background.png")
PLAYER_SHOT_SOUND_PATH = str(pathlib.Path.cwd() / "Resources" / "PlayerShot.wav")
ENEMY_SHOT_SOUND_PATH = str(pathlib.Path.cwd() / "Resources" / "PlayerShot.wav") # placeholder until proper sound picked


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        # sprite lists for enemies, shots, and background
        self.enemy_list = None
        self.player_shot_list = None
        self.enemy_shot_list = None
        self.collisions = None
        self.background_list = arcade.SpriteList()
        # timers and player speed (never changes)
        self.enemy_timer = 0
        self.player_shot_timer = 0
        self.enemy_shot_timer = 0
        self.PLAYER_SPEED = 200
        # flags for player movement logic
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        # pathlib to ensure working directory regardless of platform
        self.player_shot_sound = arcade.Sound(PLAYER_SHOT_SOUND_PATH)
        self.enemy_shot_sound = arcade.Sound(ENEMY_SHOT_SOUND_PATH)
        self.player = arcade.Sprite(PLAYER_PATH)
        # placeholders
        self.enemy_shooting = None
        self.new_enemy = None
        self.shot = None
        self.enemy_rand = 0

        # set up infinite scrolling background logic
        self.background1 = arcade.Sprite(BACKGROUND_PATH, center_x=IMAGE_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.background2 = arcade.Sprite(BACKGROUND_PATH, center_x=SCREEN_WIDTH+IMAGE_WIDTH/2, center_y=SCREEN_HEIGHT/2)
        self.background1.change_x = -3
        self.background2.change_x = -3
        self.background_list.append(self.background1)
        self.background_list.append(self.background2)

    def setup(self):
        # reset variables so player can restart
        self.player_shot_list = arcade.SpriteList()
        self.enemy_shot_list = arcade.SpriteList()
        self.collisions = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player.center_x = 100
        self.player.center_y = SCREEN_HEIGHT / 2
        self.player_shot_timer = 1
        self.enemy_timer = 5
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.player_shot_timer = 1

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        self.player.draw()
        self.enemy_list.draw()
        self.player_shot_list.draw()
        self.enemy_shot_list.draw()

    def on_update(self, delta_time):
        # some code in other functions to save clutter here
        self.move_player(delta_time)
        self.move_background()
        self.check_collisions()

        # update timers and sprite lists
        self.enemy_timer += delta_time
        self.enemy_list.update()
        self.player_shot_timer += delta_time
        self.player_shot_list.update()
        self.enemy_shot_list.update()
        if len(self.enemy_list) > 0:
            self.enemy_shot_timer += delta_time

        # spawning enemies every 5 seconds
        if self.enemy_timer >= 5:
            self.enemy_timer = 0
            self.new_enemy = Enemy(ENEMY_PATH, "Enemy", 1.5, .75)
            self.new_enemy.center_x = 880
            self.new_enemy.center_y = random.randint(27, SCREEN_HEIGHT-27)
            self.enemy_list.append(self.new_enemy)

        # enemies fire every 1.5 seconds
        if self.enemy_shot_timer >= 1.5:
            self.enemy_shot_timer = 0
            self.enemy_shot_sound.play()
            self.enemy_rand = random.randint(0, len(self.enemy_list)-1)
            self.enemy_shooting = self.enemy_list.sprite_list[self.enemy_rand]
            self.shot = Shot(ENEMY_SHOT_PATH, -8.5, 2)
            self.shot.center_x = self.enemy_shooting.center_x - 35
            self.shot.center_y = self.enemy_shooting.center_y
            self.enemy_shot_list.append(self.shot)

    def move_player(self, delta_time):
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

    def move_background(self):
        # side-scrolling background logic
        if self.background1.left <= -820:
            self.background1.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2
        if self.background2.left <= -820:
            self.background2.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2

        self.background_list.update()

    def check_collisions(self):
        for shot in self.player_shot_list:
            self.collisions = shot.collides_with_list(self.enemy_list)
            for enemy in self.collisions:
                if enemy.name == "Enemy":
                    # self.enemy_explosion.play()
                    enemy.kill()
                    shot.kill()

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

        if symbol == arcade.key.SPACE and self.player_shot_timer >= 1:
            self.player_shot_timer = 0
            self.player_shot_sound.play()
            self.shot = Shot(PLAYER_SHOT_PATH, 10, 1)
            self.shot.center_x = self.player.center_x + 76
            self.shot.center_y = self.player.center_y
            self.player_shot_list.append(self.shot)

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
    def __init__(self, filename, speed, change_scale):
        super().__init__(filename, scale=change_scale)
        self.speed = speed

    def update(self):
        self.center_x += self.speed
        if self.right > SCREEN_WIDTH or self.center_x < 0:
            self.kill()


class Enemy(arcade.Sprite):
    def __init__(self, filename, name, speed, sprite_scale):
        super().__init__(filename, scale=sprite_scale)
        self.name = name
        self.speed = speed

    def update(self):
        # enter screen then move up/down, reversing movement when hitting window boundaries
        if self.center_x > 770:
            self.center_x -= 1
        else:
            self.center_y += self.speed
            if self.center_y > SCREEN_HEIGHT - 27 or self.center_y < 27:
                self.speed *= -1


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
