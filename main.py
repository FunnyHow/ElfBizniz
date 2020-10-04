"""
Platformer Game
"""
import arcade
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Elf Bizniz!"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
COIN_COUNT = 10


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # sprite lists
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # holder for player sprite
        self.player_sprite = None
        self.physics_engine = None

        self.eugh_sound = arcade.load_sound("sounds/eugh.wav")
        self.shutup_sound_one = arcade.load_sound("sounds/shutup1.wav")
        self.shutup_sound_two = arcade.load_sound("sounds/shutup2.wav")
        self.coin_collect_sfx = arcade.load_sound(":resources:sounds/coin1.wav")

        # sound list
        self.shutup_list = [self.shutup_sound_one, self.shutup_sound_two]

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # setup player
        image_source = "images/timmy_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # walls
        for x in range(0, 1000, 64):
            # wall = arcade.Sprite("images/tiles/green+grass-128x128.png", TILE_SCALING)
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # create coins
        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        self.coin_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key: int, modifiers: int):
        """key handler"""
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.E:
            arcade.play_sound(self.eugh_sound)
        elif key == arcade.key.P:
            arcade.play_sound(random.choice(self.shutup_list))

    def on_key_release(self, key: int, modifiers: int):
        """key handler"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        """movement and game logic"""

        # move player with physics!
        self.physics_engine.update()

        # coin hit check
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # remove collected coins
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.coin_collect_sfx)



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
