"""
My version of the RealPython Arcade Game example from
https://realpython.com/top-python-game-engines/
"""

import arcade
from random import randint
from pathlib import Path

WIDTH = 800
HEIGHT = 600
TITLE = "Arcade Sample Game"
ASSETS_PATH = Path.cwd() / "assets"
COIN_COUNT = 10 #game ends with this number of coins on screen
COIN_VALUE = 10

class ArcadeGame(arcade.Window):
    """ The Arcade Game class """

    def __init__(self, width, height, title):
        """ Create the main game window """
        
        super().__init__(width, height, title)
        self.coin_countdown = 2.5
        self.coin_interval = 0.1
        self.wolf_pace = 1
        self.score = 0
        self.coins = arcade.SpriteList()
        self.set_mouse_visible(False)
        self.game_over = False
        self.wolf_appeared = False

    def reset(self):
        self.coin_countdown = 2.5
        self.wolf_pace = 1
        self.score = 0
        self.coins = arcade.SpriteList()
        self.game_over = False
        self.wolf_appeared = False
        arcade.schedule(
            function_pointer=self.add_coin, interval=self.coin_countdown
        )
        arcade.schedule(
            function_pointer = self.move_wolf, interval=0.2
        )
    
    def setup(self):
        """ Get the game ready to play """
        arcade.set_background_color(color=arcade.color.BROWN)
        sprite_image = ASSETS_PATH / "images" / "alien_green_stand.png"
        self.player = arcade.Sprite(
            filename=sprite_image, center_x=WIDTH // 2, center_y=HEIGHT // 2,
            scale = 0.5,
        )
        arcade.schedule(
            function_pointer=self.add_coin, interval=self.coin_countdown
        )
        self.coin_pickup_sound = arcade.load_sound(
            ASSETS_PATH / "sounds" / "coin_pickup.wav"
        )
        arcade.schedule(
            function_pointer = self.move_wolf, interval=0.2
        )


    def add_coin(self, dt: float):
        coin_image = ASSETS_PATH / "images" / "coin_gold.png"
        if not self.game_over:
            new_coin = arcade.Sprite(
                filename=coin_image,
                center_x=randint(20, WIDTH - 20),
                center_y=randint(20, HEIGHT - 20),
                scale = 0.5
            )
            self.coins.append(new_coin)
            
            if len(self.coins) < 3:
                self.coin_countdown -= self.coin_interval
                if self.coin_countdown < 0.1:
                    self.coin_countdown = 0.3
                arcade.unschedule(function_pointer=self.add_coin)
                arcade.schedule(
                    function_pointer=self.add_coin, interval=self.coin_countdown
                )

    def move_wolf(self, dt:float):
        wolf_image = ASSETS_PATH / "images" / "howl.png"
        if self.wolf_appeared:
            delta_x = self.wolf.center_x - self.player.center_x
            delta_y = self.wolf.center_y - self.player.center_y
            if delta_x < 0:
                self.wolf.center_x = self.wolf.center_x + self.wolf_pace
            elif delta_x > 0:
                self.wolf.center_x = self.wolf.center_x - self.wolf_pace
            if delta_y < 0:
                self.wolf.center_y = self.wolf.center_y + self.wolf_pace
            elif delta_x > 0:
                self.wolf.center_y = self.wolf.center_y - self.wolf_pace
            self.wolf_pace += 0.1
        elif self.coin_countdown < 1.5 and not self.wolf_appeared:
            self.wolf = arcade.Sprite(
                filename=wolf_image, center_x=WIDTH // 2, center_y=HEIGHT // 2, scale = 1,
            )
            self.wolf_appeared = True
        arcade.unschedule(function_pointer=self.move_wolf)
        arcade.schedule(
            function_pointer=self.move_wolf, interval=0.2
        )
            

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if not self.game_over:
            self.player.center_x = arcade.clamp(x, 0, WIDTH)
            self.player.center_y = arcade.clamp(y, 0, HEIGHT)

    def on_mouse_press(self, x, y, button, modifiers):
        self.reset()

    def on_update(self, delta_time: float):
        coins_hit = arcade.check_for_collision_with_list(
            sprite=self.player, sprite_list=self.coins
            )
        for coin in coins_hit:
            self.score += COIN_VALUE
            arcade.play_sound(self.coin_pickup_sound)
            coin.remove_from_sprite_lists()
        """
        if len(self.coins) > COIN_COUNT:
            arcade.unschedule(function_pointer=self.add_coin)
            self.game_over = True
        """
        if self.wolf_appeared:
            if self.wolf.collides_with_sprite(other=self.player):
                arcade.unschedule(function_pointer=self.move_wolf)
                self.game_over = True

    def on_draw(self):
        status = f"Score: {self.score}"
        if self.game_over:
            status = f"GAME OVER - Score: {self.score}"
        arcade.start_render()
        self.coins.draw()
        self.player.draw()
        if self.wolf_appeared:
            self.wolf.draw()
        arcade.draw_text(
            text=status,
            start_x=50,
            start_y=50,
            font_size=32,
            color=arcade.color.BLACK
        )

def main():
    arcade_game = ArcadeGame(WIDTH, HEIGHT, TITLE)
    arcade_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
    
