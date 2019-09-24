# INSTRUCTIONS
# ------------
# Control the ship using arrow keys or W/A/S/D
# Pressing space fires a shot to the other end of the screen
# Pressing escape exits the game

import pathlib
import arcade

IMAGE_WIDTH = 820
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 410
SCREEN_TITLE = "Project 1"
SHIP_PATH = pathlib.Path.cwd() / "Resources" / "Ship.png"
BULLET_PATH = pathlib.Path.cwd() / "Resources" / "Bullet.png"
BACKGROUND_PATH = pathlib.Path.cwd() / "Resources" / "Background.png"
LASER_PATH = pathlib.Path.cwd() / "Resources" / "Laser.wav"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        # setup done here instead of a setup function to avoid warnings about initialization outside of __init__
        # sprite lists for referencing/appending later
        self.bullet_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        # initial ship position and speed
        self.ship_x = 100
        self.ship_y = SCREEN_HEIGHT / 2
        self.SHIP_SPEED = 200
        # boolean flags for movement logic in on_update
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        # pathlib to ensure working directory regardless of platform
        self.laser_sound = arcade.Sound(LASER_PATH)
        self.ship = arcade.Sprite(SHIP_PATH, center_x=300, center_y=50)
        self.background1 = arcade.Sprite(BACKGROUND_PATH, center_x=IMAGE_WIDTH/2, center_y=SCREEN_HEIGHT/2)
        self.background2 = arcade.Sprite(BACKGROUND_PATH, center_x=SCREEN_WIDTH+IMAGE_WIDTH/2, center_y=SCREEN_HEIGHT/2)

        # set up infinite scrolling background logic
        self.background1.change_x = -3
        self.background2.change_x = -3
        self.background_list.append(self.background1)
        self.background_list.append(self.background2)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        self.ship.draw()
        self.bullet_list.draw()

    def on_update(self, delta_time):
        # check the flags for movement and update accordingly
        if self.right:
            self.ship_x += self.SHIP_SPEED * delta_time
        if self.left:
            self.ship_x -= self.SHIP_SPEED * delta_time
        if self.up:
            self.ship_y += self.SHIP_SPEED * delta_time
        if self.down:
            self.ship_y -= self.SHIP_SPEED * delta_time

        # prevent movement outside of the window boundaries
        if self.ship_x > SCREEN_WIDTH - 38:
            self.ship_x -= self.SHIP_SPEED * delta_time
        if self.ship_x < 38:
            self.ship_x += self.SHIP_SPEED * delta_time
        if self.ship_y > SCREEN_HEIGHT - 17:
            self.ship_y -= self.SHIP_SPEED * delta_time
        if self.ship_y < 17:
            self.ship_y += self.SHIP_SPEED * delta_time

        # update position of ship and any active bullets
        self.ship.set_position(self.ship_x, self.ship_y)
        self.bullet_list.update()

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

        if symbol == arcade.key.SPACE:
            self.laser_sound.play()
            bullet = Bullet(BULLET_PATH)
            bullet.center_x = self.ship.center_x + 76
            bullet.center_y = self.ship.center_y
            self.bullet_list.append(bullet)

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


class Bullet(arcade.Sprite):
    def update(self):
        self.center_x += 4
        if self.center_x > SCREEN_WIDTH:
            self.kill()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
