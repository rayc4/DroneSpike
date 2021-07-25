import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "DroneSpike"

GRAVITY = 1500
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

PLAYER_FRICTION = 1.0
WALL_FRICTION = 1.0

WALL_ELASTICITY = 0.5

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
        self.background = None

        # Each sprite goes into a list
        self.player_list = None
        self.net_list = None
        self.ball_list = None

        self.p1_sprite = None
        self.p2_sprite = None

        self.physics_engine = arcade.PymunkPhysicsEngine
    def setup(self):
        ''' Set up the game here. Call this function to restart the game.'''
        self.background = arcade.load_texture("background.png")
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.net_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        self.p1_sprite = arcade.Sprite("droneCA.png", 0.05)
        self.p1_sprite.center_x = 64
        self.p1_sprite.center_y = 50
        self.player_list.append(self.p1_sprite)
        self.p2_sprite = arcade.Sprite("droneCN.png", 0.05)
        self.p2_sprite.center_x = 900
        self.p2_sprite.center_y = 50
        self.player_list.append(self.p2_sprite)

        self.ground_sprite = arcade.Sprite("ground.png", 1)
        self.ground_sprite.center_x = 500
        self.ground_sprite.center_y = -500
        self.left_wall_sprite = arcade.Sprite("wall.png", 1)
        self.left_wall_sprite.center_x = -50
        self.left_wall_sprite.center_y = 325
        self.right_wall_sprite = arcade.Sprite("wall.png", 1)
        self.right_wall_sprite.center_x = 1050
        self.right_wall_sprite.center_y = 325
        self.ceiling_sprite = arcade.Sprite("ground.png", 1)
        self.ceiling_sprite.center_x = 500
        self.ceiling_sprite.center_y = 1175

        self.wall_list.append(self.ground_sprite)
        self.wall_list.append(self.left_wall_sprite)
        self.wall_list.append(self.right_wall_sprite)
        self.wall_list.append(self.ceiling_sprite)

        self.ball_sprite = arcade.Sprite("ball.png", 0.1)
        self.ball_sprite.center_x = 100
        self.ball_sprite.center_y = 650
        self.ball_list.append(self.ball_sprite)

        self.net_sprite = arcade.Sprite("net.png", 0.25)
        self.net_sprite.center_x = 500
        self.net_sprite.center_y = 240
        self.net_list.append(self.net_sprite)

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

        self.physics_engine.add_sprite(self.p2_sprite,\
                                       friction=PLAYER_FRICTION, \
                                       mass=PLAYER_FRICTION, \
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF, \
                                       collision_type="player", \
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED, \
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED, \
                                       elasticity=1.0)

        self.physics_engine.add_sprite(self.ground_sprite, \
                                       friction=WALL_FRICTION, \
                                       body_type=arcade.PymunkPhysicsEngine.STATIC, \
                                       collision_type="wall", \
                                       elasticity=WALL_ELASTICITY)

        self.physics_engine.add_sprite(self.left_wall_sprite, \
                                       friction=WALL_FRICTION, \
                                       body_type=arcade.PymunkPhysicsEngine.STATIC, \
                                       collision_type="wall", \
                                       elasticity=WALL_ELASTICITY)

        self.physics_engine.add_sprite(self.right_wall_sprite, \
                                       friction=WALL_FRICTION, \
                                       body_type=arcade.PymunkPhysicsEngine.STATIC, \
                                       collision_type="wall", \
                                       elasticity=WALL_ELASTICITY)

        self.physics_engine.add_sprite(self.ball_sprite,\
                                       friction=0.9, \
                                       mass=BALL_MASS, \
                                       collision_type="ball", \
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED, \
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED, \
                                       elasticity=1.0, \
                                       radius=1)

        self.physics_engine.add_sprite(self.net_sprite, \
                                       friction=WALL_FRICTION, \
                                       body_type=arcade.PymunkPhysicsEngine.STATIC, \
                                       collision_type="net", \
                                       elasticity=0.5)

        self.physics_engine.add_sprite(self.ceiling_sprite, \
                                       friction=WALL_FRICTION, \
                                       body_type=arcade.PymunkPhysicsEngine.STATIC, \
                                       collision_type="wall", \
                                       elasticity=WALL_ELASTICITY)

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

        if key == arcade.key.UP:
            self.keys_pressed['up'] = True
        elif key == arcade.key.LEFT:
            self.keys_pressed['left'] = True
        elif key == arcade.key.RIGHT:
            self.keys_pressed['right'] = True

    def on_key_release(self, key, modifiers):
        ''' Called whenever a key is released. '''
        if key == arcade.key.W:
            self.keys_pressed['w'] = False
        elif key == arcade.key.A:
            self.keys_pressed['a'] = False
        elif key == arcade.key.D:
            self.keys_pressed['d'] = False

        if key == arcade.key.UP:
            self.keys_pressed['up'] = False
        elif key == arcade.key.LEFT:
            self.keys_pressed['left'] = False
        elif key == arcade.key.RIGHT:
            self.keys_pressed['right'] = False

    def on_draw(self):
        ''' Render the screen. '''
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.net_list.draw()
        self.player_list.draw()
        self.wall_list.draw()
        self.ball_list.draw()

    def on_update(self, delta_time):
        ''' Movement and game logic '''
        if self.keys_pressed['a'] and not self.keys_pressed['d']:
            self.physics_engine.apply_force(self.p1_sprite, (-PLAYER_FORCE_ON_GROUND, 0))
            self.physics_engine.set_friction(self.p1_sprite, 0)
        elif self.keys_pressed['d'] and not self.keys_pressed['a']:
            self.physics_engine.apply_force(self.p1_sprite, (PLAYER_FORCE_ON_GROUND, 0))
            self.physics_engine.set_friction(self.p1_sprite, 0)
        if self.keys_pressed['w']:
            self.physics_engine.apply_force(self.p1_sprite, (0, 2500))
        else:
            self.physics_engine.set_friction(self.p1_sprite, PLAYER_FRICTION)

        if self.keys_pressed['left'] and not self.keys_pressed['right']:
            self.physics_engine.apply_force(self.p2_sprite, (-PLAYER_FORCE_ON_GROUND, 0))
            self.physics_engine.set_friction(self.p2_sprite, 0)
        elif self.keys_pressed['right'] and not self.keys_pressed['left']:
            self.physics_engine.apply_force(self.p2_sprite, (PLAYER_FORCE_ON_GROUND, 0))
            self.physics_engine.set_friction(self.p2_sprite, 0)
        if self.keys_pressed['up']:
            self.physics_engine.apply_force(self.p2_sprite, (0, 2500))
        else:
            self.physics_engine.set_friction(self.p2_sprite, PLAYER_FRICTION)

        self.physics_engine.step()


def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
