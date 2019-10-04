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
PLAYER_HIT_SOUND_PATH = str(pathlib.Path.cwd() / "Resources" / "PlayerHit.wav")
ENEMY_SHOT_SOUND_PATH = str(pathlib.Path.cwd() / "Resources" / "EnemyShot.wav")
ENEMY_HIT_SOUND_PATH = str(pathlib.Path.cwd() / "Resources" / "EnemyHit.wav")
WIN_SOUND_PATH = str(pathlib.Path.cwd() / "Resources" / "Win.wav")
# LOSE_SOUND_PATH = str(pathlib.Path.cwd() / "Resources" / "Lose.wav")


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
        # state system and scoring
        self.state = None
        self.score = 0
        # flags for player movement logic
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        # initializing sounds and sprites
        self.player_shot_sound = arcade.Sound(PLAYER_SHOT_SOUND_PATH)
        self.player_hit_sound = arcade.Sound(PLAYER_HIT_SOUND_PATH)
        self.enemy_shot_sound = arcade.Sound(ENEMY_SHOT_SOUND_PATH)
        self.enemy_hit_sound = arcade.Sound(ENEMY_HIT_SOUND_PATH)
        self.win_sound = arcade.Sound(WIN_SOUND_PATH)
        # self.lose_sound = arcade.Sound(LOSE_SOUND_PATH)
        self.player = arcade.Sprite(PLAYER_PATH)
        # other temp variables
        self.enemy_shooting = None
        self.new_enemy = None
        self.new_shot = None
        self.enemy_rand = 0
        self.enemy_spawn_time = 0
        self.player_health = 0

        # set up infinite scrolling background logic
        self.background1 = arcade.Sprite(BACKGROUND_PATH, center_x=IMAGE_WIDTH / 2,
                                         center_y=SCREEN_HEIGHT / 2)
        self.background2 = arcade.Sprite(BACKGROUND_PATH, center_x=SCREEN_WIDTH+IMAGE_WIDTH/2,
                                         center_y=SCREEN_HEIGHT/2)
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
        self.score = 0
        self.enemy_timer = 3
        self.player_health = 2
        self.enemy_spawn_time = 4
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.state = "RUNNING"  # reset state to running so movement is allowed
        self.player_shot_timer = 1

    def on_draw(self):
        arcade.start_render()
        if self.state == "RUNNING":
            self.background_list.draw()
            self.player.draw()
            self.enemy_list.draw()
            self.player_shot_list.draw()
            self.enemy_shot_list.draw()
            arcade.draw_text(f"SCORE: {self.score}", 20, 380, arcade.color.YELLOW, 20)
            arcade.draw_text(f"HEALTH: {self.player_health}", 20, 350, arcade.color.YELLOW, 20)
        elif self.state == "WIN":
            arcade.draw_text(f"You win!\nFinal Score: {self.score}", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.color.YELLOW, 30, anchor_x="center")
            arcade.draw_text("Press Q to quit, or R to restart.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-30,
                             arcade.color.YELLOW, 30, anchor_x="center")
        elif self.state == "LOSE":
            arcade.draw_text(f"You lose...\nFinal Score: {self.score}", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.color.YELLOW, 30, anchor_x="center")
            arcade.draw_text("Press Q to quit, or R to restart.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-30,
                             arcade.color.YELLOW, 30, anchor_x="center")

    def on_update(self, delta_time):
        # check state of the game before doing anything else
        if self.state == "RUNNING":
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

            # spawning enemies every x seconds
            if self.enemy_timer >= self.enemy_spawn_time:
                self.enemy_timer = 0
                self.new_enemy = Enemy(ENEMY_PATH, 2, 1, .75)
                self.new_enemy.center_x = 880
                self.new_enemy.center_y = random.randint(27, SCREEN_HEIGHT-27)
                self.enemy_list.append(self.new_enemy)

            # enemies fire every 1.5 seconds
            if self.enemy_shot_timer >= 1:
                self.enemy_shot_timer = 0
                self.enemy_rand = random.randint(0, len(self.enemy_list)-1)
                self.enemy_shooting = self.enemy_list.sprite_list[self.enemy_rand]
                # only fire if enemy is fully on-screen
                if self.enemy_shooting.ready:
                    self.new_shot = Shot(ENEMY_SHOT_PATH, -10, 2)
                    self.new_shot.center_x = self.enemy_shooting.center_x - 35
                    self.new_shot.center_y = self.enemy_shooting.center_y
                    self.enemy_shot_list.append(self.new_shot)
                    self.enemy_shot_sound.play()

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
        # iterate through player shots to check for enemy collisions
        for shot in self.player_shot_list:
            self.collisions = shot.collides_with_list(self.enemy_list)
            if len(self.collisions) > 0:
                # boss enemies have 2 health, otherwise kill right away
                if self.collisions[0].health == 2:
                    self.enemy_hit_sound.play()
                    self.collisions[0].health -= 1
                    shot.kill()
                elif self.collisions[0].health == 1:
                    self.enemy_hit_sound.play()
                    self.collisions[0].kill()
                    shot.kill()
                    self.score += 1
                    if self.score >= 3:
                        self.win_sound.play()
                        self.state = "WIN"
                        self.win()

        # iterate through enemy shots to check for player collision
        for shot in self.enemy_shot_list:
            if shot.collides_with_sprite(self.player):
                if self.player_health == 2:
                    self.player_hit_sound.play()
                    self.player_health -= 1
                    shot.kill()
                elif self.player_health == 1:
                    # self.lose_sound.play()
                    self.state = "LOSE"
                    self.lose()

        # check if player is colliding with enemy ships
        if len(self.player.collides_with_list(self.enemy_list)) > 0:
            # self.lose_sound.play()
            self.state = "LOSE"
            self.lose()

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
            self.new_shot = Shot(PLAYER_SHOT_PATH, 10, 1)
            self.new_shot.center_x = self.player.center_x + 76
            self.new_shot.center_y = self.player.center_y
            self.player_shot_list.append(self.new_shot)

        if symbol == arcade.key.Q and (self.state == "WIN" or self.state == "LOSE"):
            self.close()

        if symbol == arcade.key.R and (self.state == "WIN" or self.state == "LOSE"):
            self.setup()

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

    def lose(self):
        pass

    def win(self):
        pass


class Shot(arcade.Sprite):
    def __init__(self, filename, speed, change_scale):
        super().__init__(filename, scale=change_scale)
        self.speed = speed

    def update(self):
        self.center_x += self.speed
        if self.right > SCREEN_WIDTH - 10 or self.center_x < 10:
            self.kill()


class Enemy(arcade.Sprite):
    def __init__(self, filename, speed, health, sprite_scale):
        super().__init__(filename, scale=sprite_scale)
        self.speed = speed
        self.health = health
        self.ready = False  # used to track if enemy is done with initial fade onto screen

    def update(self):
        # enter screen then move up/down, reversing movement when hitting window boundaries
        if self.center_x > 770:
            self.center_x -= 3
        else:
            if self.ready is False:
                self.ready = True
            self.center_y += self.speed
            if self.center_y > SCREEN_HEIGHT - 27 or self.center_y < 27:
                self.speed *= -1


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
