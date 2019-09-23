import pathlib
import arcade

IMAGE_WIDTH = 820
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 410
SCREEN_TITLE = "Project 1"
SHIP_PATH = pathlib.Path.cwd() / "Resources" / "Ship.png"
BULLET_PATH = pathlib.Path.cwd() / "Resources" / "Bullet.png"
BACKGROUND_PATH = pathlib.Path.cwd() / "Resources" / "Background.png"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        # setup lists for referencing/appending later
        self.bullet_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        # initial ship position and speed
        self.ship_x = 100
        self.ship_y = 205
        self.SHIP_SPEED = 300
        # boolean flags for movement logic in on_update
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        # pathlib to ensure working directory regardless of platform
        self.ship = arcade.Sprite(SHIP_PATH, center_x=300, center_y=50)
        self.background_1 = arcade.Sprite(BACKGROUND_PATH, center_x=IMAGE_WIDTH/2, center_y=SCREEN_HEIGHT/2)
        self.background_2 = arcade.Sprite(BACKGROUND_PATH, center_x=SCREEN_WIDTH + IMAGE_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)

        # set up infinite scrolling background logic
        self.background_1.change_x = -2
        self.background_2.change_x = -2
        self.background_list.append(self.background_1)
        self.background_list.append(self.background_2)

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
        if self.background_1.left == -IMAGE_WIDTH:
            self.background_1.center_x = SCREEN_WIDTH + IMAGE_WIDTH//2
        if self.background_2.left == -IMAGE_WIDTH:
            self.background_2.center_x = SCREEN_WIDTH + IMAGE_WIDTH//2
        #checks if the left edge of the background image is at -820 (image width) aka fully offscreen
        # if so it moves it basically opposite, all the way to the right offscreen
        #while the other pic continues to scroll left
        #repeat
        #so it moves the center of the image all the way over, the rest are all constants for the image width and screen width
        #define way up here

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
            print(self.center_x)
            self.kill()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
