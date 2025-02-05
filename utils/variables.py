import cv2
import random
import time
import sys
import os
from utils.gui import applying_mask

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.normpath(os.path.join(base_path, relative_path))

class FILES(object):
    """
    This class contains all the hardcoded paths.
    """
    laser_left_path = resource_path('images/laser_left.png')
    laser_right_path = resource_path('images/laser_right.png')
    explosion_path = resource_path('images/explosion.png')
    bottle_path = resource_path('images/bottle.png')
    smiley_path = resource_path('images/smiley.png')
    face_cascade_path = resource_path('haarcascade_xml_files/haarcascade_frontalface_default.xml')
    eye_cascade_path = resource_path('haarcascade_xml_files/haarcascade_eye_tree_eyeglasses.xml')


class FLAGS(object):
    """
    This class stores all the flags used.

    EXPLOSION_ON_SCREEN : Allows detecting if a bottle is broken or not.
    START_TIMER : Allows launching the timer when the game start.
    GAME_COMPLETED : Allows determining if a game is finish or not. Set at TRUE at the end of the game.
    NUMBER_BOTTLE_TOUCHED : Allows determining if 5 bottles was touched or not.
    GAME_STATE : Allows knowing if a game is in progress.
    BOTTLE_TOUCHED : Allows determining if a bottle was touched or not.
    COUNTDOWN : Initialized to 3, it will decrement to 1 with this function
    TIMER_GAME : Launch the time taken for a game
    GAME_TIME : Determine elapsed time of the current game
    TIMER_EXP : Determine the time between the explosion and the appearance of a new bottle
    """
    EXPLOSION_ON_SCREEN = False
    START_TIMER = False
    GAME_COMPLETED = False
    NUMBER_BOTTLE_TOUCHED = 0
    GAME_STATE = False
    BOTTLE_TOUCHED = False
    COUNTDOWN = 4  # Start in 3 + 1 to simplify logic. It shows starting in 3
    TIMER_GAME = 0
    GAME_TIME = 0
    TIMER_EXP = 0
    TIME_START = time.time()
    TIME_END = time.time()


class EYES_COORD(object):
    """
    This class stores all the eyes coordinates.

    right_eye_x: This coordinates is the right eye X coordinate.
    right_eye_y: This coordinates is the right eye Y coordinate.
    left_eye_x: This coordinates is the left eye X coordinate.
    left_eye_y: This coordinates is the left eye Y coordinate.
    """
    right_eye_x = -100
    right_eye_y = -100
    left_eye_x = -100
    left_eye_y = -100


class SMILEY(object):
    """
    This class stores all the features related to the smiley image.
    Sources :
    Smiley
    https://www.freepngimg.com/thumb/emoji/64956-emoticon-thumb-double-button-smiley-emoji-signal.png

    smiley_position_x : position X of the smiley.
    smiley_position_y : position Y of the smiley.
    smiley_height : height of the smiley.
    smiley_width : width of the smiley.
    mask_smiley : mask that will also be re-imaged the smiley.
    mask_inv_smiley : inv-mask that will also be re-imaged the smiley.
    smiley_img : smiley png image.
    """
    smiley_position_x = 10
    smiley_position_y = 130
    smiley_height = 190
    smiley_width = 190
    mask_smiley = None
    mask_inv_smiley = None
    smiley_img = cv2.imread(FILES.smiley_path)
    mask_smiley, mask_inv_smiley, smiley_img = applying_mask(smiley_img)


class BOTTLE(object):
    """
    This class store all the features related to the bottle image.
    Sources :
    Bottle
    https://cdn.pixabay.com/photo/2013/07/13/13/33/bottle-161077_960_720.png

    x_max : Frame X-axis size.
    bottle_width: Width of the bottle_img.
    bottle_rand_pos: Bottle random position outside the laser area.
    bottle_img: bottle png image.
    mask_bottle, mask_inv_bottle : inv-mask that will also be re-imaged the bottle.
    """
    x_max = 640
    bottle_width = 100
    bottle_rand_pos = random.randint(0, x_max - bottle_width)
    bottle_height = -1000
    bottle_img = cv2.imread(FILES.bottle_path)
    mask_bottle, mask_inv_bottle, bottle_img = applying_mask(bottle_img)


class LASER(object):
    """
    This class store all the features related to the laser images.

    laser_left_img : right laser png image.
    laser_right_img : left laser png image.
    mask_laser_left, mask_inv_laser_left : mask and inv_mask that will also be re-imaged the left laser.
    mask_laser_right, mask_inv_laser_right : mask and inv_mask that will also be re-imaged the left laser.
    laser_width: width of the laser.
    """
    laser_left_img = cv2.imread(FILES.laser_left_path)
    laser_right_img = cv2.imread(FILES.laser_right_path)
    mask_laser_left, mask_inv_laser_left, laser_left_img = applying_mask(laser_left_img)
    mask_laser_right, mask_inv_laser_right, laser_right_img = applying_mask(laser_right_img)
    laser_width = 60
    right_laser_height = -1000
    left_laser_height = -1000


class EXPLOSION(object):
    """
    This class store all the features related to the explosion image.

    explosion_img: explosion png image.
    mask_explosion, mask_inv_explosion : mask and inv-mask that will also be re-imaged the explosion.
    explosion_width : width of the explosion.
    """
    explosion_img = cv2.imread(FILES.explosion_path)
    mask_explosion, mask_inv_explosion, explosion_img = applying_mask(explosion_img)
    explosion_width = 300