import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "DroneSpike"

DRONE_SCALING = 1
GRAVITY = 1500
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6
PLAYER_MASS = 2.0
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600

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

        image_source = "drone_idle.png"
        self.p1_sprite = arcade.Sprite(image_source, DRONE_SCALING)
        self.p1_sprite.center_x = 64
        self.p1_sprite.center_y = 128
        self.p1_list.append(self.p1_sprite)

        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING, \
                                                         gravity=(0,-GRAVITY))
        self.physics_engine.add_sprite(self.p1_sprite,\
                                       friction=PLAYER_FRICTION, \
                                       mass=PLAYER_FRICTION, \
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF, \
                                       collision_type="player", \
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED, \
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)
    def on_draw(self):
        ''' Render the screen. '''
        arcade.start_render()
        self.p1_list.draw()

    def on_update(self, delta_time):
        ''' Movement and game logic '''
        self.physics_engine.step()
def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
