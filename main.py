"""
Platformer Game
"""
import arcade
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Elf Bizniz!"

CHARACTER_SCALING = 0.75
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100


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
        self.background_list = None
        self.key_list = None
        self.enemies_list = None
        self.boss_list = None

        # holder for player sprite
        self.player_sprite = None
        self.physics_engine = None
        self.boss_sprite = None

        # track scrolling
        self.view_bottom = 0
        self.view_left = 0

        # score
        self.score = 0

        # sfx
        self.eugh_sound = arcade.load_sound("sounds/eugh.wav")
        self.shutup_sound_one = arcade.load_sound("sounds/shutup1.wav")
        self.shutup_sound_two = arcade.load_sound("sounds/shutup2.wav")
        self.coin_collect_sfx = arcade.load_sound(":resources:sounds/coin1.wav")

        # sound list
        self.shutup_list = [self.shutup_sound_one, self.shutup_sound_two]

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # score
        self.score = 0

        # track scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()

        # setup player
        image_source = "images/timmy_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # setup bertwam
        self.boss_sprite = arcade.Sprite("images/bertwam_idle.png", CHARACTER_SCALING)
        self.boss_sprite.center_x = 64
        self.boss_sprite.center_y = 128
        self.boss_list.append(self.boss_sprite)

        # load map from file
        map_name = "maps/level_1.tmx"

        # map and layers
        the_map = arcade.read_tmx(map_name)
        platform_layer = "platforms"
        coins_layer = "coins"
        keys_layer = "keys"
        enemies_layer = "enemies"
        self.wall_list = arcade.tilemap.process_layer(map_object=the_map, layer_name=platform_layer,
                                                      scaling=TILE_SCALING, use_spatial_hash=True)

        self.coin_list = arcade.tilemap.process_layer(map_object=the_map, layer_name=coins_layer,
                                                      scaling=TILE_SCALING, use_spatial_hash=True)

        self.key_list = arcade.tilemap.process_layer(map_object=the_map, layer_name=keys_layer,
                                                     scaling=TILE_SCALING, use_spatial_hash=True)

        self.enemies_list = arcade.tilemap.process_layer(map_object=the_map, layer_name=enemies_layer,
                                                         scaling=TILE_SCALING, use_spatial_hash=True)

        # -- Background objects
        self.background_list = arcade.tilemap.process_layer(the_map, "background", TILE_SCALING)

        # environmental stuffs
        if the_map.background_color:
            arcade.set_background_color(the_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        self.background_list.draw()
        self.coin_list.draw()
        self.key_list.draw()
        self.enemies_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        self.boss_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Elf dollahs: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

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
            self.score += 1

        # handle scrolling
        changed = False

        # scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
