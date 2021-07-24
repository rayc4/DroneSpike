import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "DroneSpike"

GRAVITY = 1500
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

PLAYER_FRICTION = 1.0
WALL_FRICTION = 1.0

PLAYER_MASS = 2.0
BALL_MASS = 0.001

PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600

PLAYER_FORCE_ON_GROUND = 8000
class GameWindow(arcade.Window):
    ''' Main application class '''
    
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.LIGHT_GOLDENROD_YELLOW)

        # Each sprite goes into a list
        self.p1_list = None
        self.p2_list = None
        self.net_list = None
        self.ball_list = None

        self.p1_sprite = None
        self.p2_sprite = None

        self.physics_engine = arcade.PymunkPhysicsEngine
    def setup(self):
        ''' Set up the game here. Call this function to restart the game.'''
        # Create the Sprite lists
        self.p1_list = arcade.SpriteList()
        self.p2_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.net_list = arcade.SpriteList(use_spatial_hash=True)
        self.ground_list = arcade.SpriteList(use_spatial_hash=True)

        self.p1_sprite = arcade.Sprite("drone_idle.png", 0.4)
        self.p1_sprite.center_x = 64
        self.p1_sprite.center_y = 50
        self.p1_list.append(self.p1_sprite)

        self.ground_sprite = arcade.Sprite("ground.png", 1)
        self.ground_sprite.center_x = 500
        self.ground_sprite.center_y = 10
        self.ground_list.append(self.ground_sprite)

        self.ball_sprite = arcade.Sprite("ball.png", 0.1)
        self.ball_sprite.center_x = 100
        self.ball_sprite.center_y = 650
        self.ball_list.append(self.ball_sprite)

        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING, \
                                                         gravity=(0,-GRAVITY))
        self.physics_engine.add_sprite(self.p1_sprite,\
                                       friction=PLAYER_FRICTION, \
                                       mass=PLAYER_FRICTION, \
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF, \
                                       collision_type="player", \
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED, \
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED, \
                                       elasticity=1.0)

        self.physics_engine.add_sprite(self.ground_sprite,\
                                       friction=WALL_FRICTION, \
                                       body_type=arcade.PymunkPhysicsEngine.STATIC, \
                                       collision_type="wall", \
                                       elasticity=1.0)

        self.physics_engine.add_sprite(self.ball_sprite,\
                                       friction=0.9, \
                                       mass=BALL_MASS, \
                                       collision_type="ball", \
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED, \
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED, \
                                       elasticity=1.0, \
                                       radius=1)
        # WASD for player 1, arrow keys for player 2
        self.keys_pressed = {'w':False, 'a':False, 'd':False, \
                             'up':False, 'left':False, 'right':False}

    def on_key_press(self, key, modifiers):
        ''' Called whenever a key is pressed. '''
        if key == arcade.key.W:
            self.keys_pressed['w'] = True
        elif key == arcade.key.A:
            self.keys_pressed['a'] = True
        elif key == arcade.key.D:
            self.keys_pressed['d'] = True

    def on_key_release(self, key, modifiers):
        ''' Called whenever a key is released. '''
        if key == arcade.key.W:
            self.keys_pressed['w'] = False
        elif key == arcade.key.A:
            self.keys_pressed['a'] = False
        elif key == arcade.key.D:
            self.keys_pressed['d'] = False

    def on_draw(self):
        ''' Render the screen. '''
        arcade.start_render()
        self.p1_list.draw()
        self.ground_list.draw()
        self.ball_list.draw()

    def on_update(self, delta_time):
        ''' Movement and game logic '''
        if self.keys_pressed['a'] and not self.keys_pressed['d']:
            self.physics_engine.apply_force(self.p1_sprite, (-PLAYER_FORCE_ON_GROUND, 0))
            self.physics_engine.set_friction(self.p1_sprite, 0)
        if self.keys_pressed['d'] and not self.keys_pressed['a']:
            self.physics_engine.apply_force(self.p1_sprite, (PLAYER_FORCE_ON_GROUND, 0))
            self.physics_engine.set_friction(self.p1_sprite, 0)
        else:
            self.physics_engine.set_friction(self.p1_sprite, PLAYER_FRICTION)
        self.physics_engine.step()


def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
