import cv2
import random
import time
from utils.language import USED_LANGUAGE


class Button(object):
    """
    This class defines the PLAY button used to start a game
    """

    def __init__(self, text, x, y, width, height, command=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.left = x
        self.top = y
        self.right = x + width - 1
        self.bottom = y + height - 1

        self.hover = False
        self.clicked = False
        self.command = command

    def handle_event(self, event, x, y, flags, param):
        self.hover = (self.left <= x <= self.right and
                      self.top <= y <= self.bottom)

        if self.hover and flags == 1:
            self.clicked = True

    def draw(self, frame):
        button_x = 250
        button_y = 440
        button_delta_x = 150
        button_delta_y = 50

        if not self.hover:
            cv2.putText(img=frame,
                        text=USED_LANGUAGE.play_string,
                        org=(button_x + 10, button_y - 15),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 127),
                        thickness=2)

            cv2.rectangle(img=frame,
                          pt1=(button_x, button_y),
                          pt2=(button_x + button_delta_x, button_y - button_delta_y),
                          color=(255, 255, 127),
                          thickness=2)
        else:
            cv2.putText(img=frame,
                        text=USED_LANGUAGE.play_string,
                        org=(button_x + 10, button_y - 15),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(0, 255, 0),
                        thickness=2)

            cv2.rectangle(img=frame,
                          pt1=(button_x, button_y),
                          pt2=(button_x + button_delta_x, button_y - button_delta_y),
                          color=(0, 255, 0),
                          thickness=2)


def applying_mask(img):
    """
    This function allows to create the mask of each image used during the game.
    The output gives the mask of the image, its inverse mask also which will be inserted in the game.

    :param img: This is the image to which the mask is applied
    :return:
    mask: Creation of a new single-layer image uses for masking
    mask_inv: The initial mask will define the area for the image, and the inverse mask will be for the region
              around the image
    img: The image in 3-channel BGR format
    """
    # Create the mask for the object
    objectGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(objectGray, 10, 255, cv2.THRESH_BINARY)

    # Create the inverted mask for the object
    mask_inv = cv2.bitwise_not(mask)
    img = img[:, :, 0:3]

    return mask, mask_inv, img


def resizing(image, width, height, orig_mask, orig_mask_inv, roi_image):
    """
    This function allows you to resize the images (foreground) so that they fit in the frame (background)
    :param image: Image that will be resized to match the desired size in the game
    :param width: width of the resizing image
    :param height: height of the resizing image
    :param orig_mask: mask that will also be re-imaged
    :param orig_mask_inv: inv-mask that will also be re-imaged
    :param roi_image: region of interest where the image will be inserted
    :return:
    dst: Represents the addition of the background and the foreground. Adding the image with the right dimensions
         in the desired area of interest
    """
    img = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    mask = cv2.resize(orig_mask, (width, height), interpolation=cv2.INTER_AREA)
    mask_inv = cv2.resize(orig_mask_inv, (width, height), interpolation=cv2.INTER_AREA)
    mask_inv = cv2.resize(mask_inv, (roi_image.shape[1], roi_image.shape[0]))

    # roi_bg contains the original image only where the image is not in the region that is the size of the image.
    roi_bg = cv2.bitwise_and(roi_image, roi_image, mask=mask_inv)

    # roi_fg contains the image of the image only where the image is
    roi_fg = cv2.bitwise_and(img, img, mask=mask)

    # join the roi_bg and roi_fg
    dst = cv2.add(roi_bg, roi_fg)

    return dst


def display_score(frame, SMILEY, FLAGS):
    """
    This function is used to display the different elements that are displayed at the end of a game. 
    The end message to the player, his score (time) and the smiley
    :param frame: Represent the frame of the camera
    :param FLAGS: Flags class containing all parameters needed
    :param SMILEY: Smiley class containing all parameters needed
    :return:
    Display all end of game elements (score, smiley and end of game message)
    """

    cv2.putText(frame, 'You win! Your time: {:.1f} s'.format(FLAGS.GAME_TIME), (130, 100), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 255, 255), 2)
    roi_smiley = frame[SMILEY.smiley_position_y:SMILEY.smiley_position_y + SMILEY.smiley_height,
                 SMILEY.smiley_position_x:SMILEY.smiley_position_x + SMILEY.smiley_width]
    dst_smiley = resizing(SMILEY.smiley_img, SMILEY.smiley_width, SMILEY.smiley_height,
                          SMILEY.mask_smiley, SMILEY.mask_inv_smiley, roi_smiley)
    frame[SMILEY.smiley_position_y:SMILEY.smiley_position_y + SMILEY.smiley_height,
    SMILEY.smiley_position_x:SMILEY.smiley_position_x + SMILEY.smiley_width] = dst_smiley

    return frame


def display_countdown(FLAGS, frame):
    """
    This function allows to display the countdown when the PLAY button is clicked
    :param FLAGS: Flags class containing all parameters needed
    :param frame: Represent the frame of the camera

    :return:
    Display the countdown on the frame (from 3 to 1) before the game starts
    """
    FLAGS.TIME_END = time.time()
    if FLAGS.TIME_START == None or (FLAGS.TIME_END - FLAGS.TIME_START) > 1:
        FLAGS.TIME_START = time.time()
        FLAGS.COUNTDOWN -= 1

    cv2.putText(frame, str(FLAGS.COUNTDOWN), (270, 320), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 8)
    return frame, FLAGS


def draw_explosion(frame, BOTTLE, EXPLOSION):
    """
    This function allows to draw the explosion
    :param frame: Represent the frame of the camera
    :param BOTTLE: Bottle class containing all parameters needed
    :param EXPLOSION: Explosion class containing all parameters needed
    :return:
    EXPLOSION_ON_SCREEN flag status
    """
    frame_y_max = frame.shape[0]
    EXPLOSION_ON_SCREEN = True

    # Display explosion
    roi_explosion = frame[frame_y_max - BOTTLE.bottle_height:frame_y_max,
                    BOTTLE.bottle_rand_pos:BOTTLE.bottle_rand_pos + BOTTLE.bottle_width]

    dst_exp = resizing(EXPLOSION.explosion_img,
                       BOTTLE.bottle_width,
                       BOTTLE.bottle_height,
                       EXPLOSION.mask_explosion,
                       EXPLOSION.mask_inv_explosion,
                       roi_explosion)

    frame[frame_y_max - BOTTLE.bottle_height:frame_y_max,
    BOTTLE.bottle_rand_pos:BOTTLE.bottle_rand_pos + BOTTLE.bottle_width] = dst_exp
    return EXPLOSION_ON_SCREEN


def draw_laser(frame, EYES_COORD, LASER):
    """
    This function allows to draw the lasers
    :param frame: Represent the frame of the camera
    :param EYES_COORD : Eyes coordinates class containing all parameters needed
    :param LASER : Laser class containing all parameters needed
    :return:
    Frame with lasers added
    """
    try:
        LASER.right_laser_height = frame.shape[0] - EYES_COORD.right_eye_y
        LASER.left_laser_height = frame.shape[0] - EYES_COORD.left_eye_y
        LASER.laser_width = 60

        if EYES_COORD.right_eye_y > 0 and EYES_COORD.right_eye_x > 0 and EYES_COORD.left_eye_x > 0 and \
                EYES_COORD.left_eye_y > 0 and LASER.right_laser_height > 0 and LASER.left_laser_height > 0 and \
                LASER.laser_width > 0:

            roi_right = frame[EYES_COORD.right_eye_y: EYES_COORD.right_eye_y + LASER.right_laser_height,
                        EYES_COORD.right_eye_x - int(LASER.laser_width / 2): EYES_COORD.right_eye_x +
                                                                             int(LASER.laser_width / 2)]
            dst_right = resizing(LASER.laser_right_img,
                                 LASER.laser_width,
                                 LASER.right_laser_height,
                                 LASER.mask_laser_right,
                                 LASER.mask_inv_laser_right,
                                 roi_right)

            frame[EYES_COORD.right_eye_y: EYES_COORD.right_eye_y + LASER.right_laser_height,
            EYES_COORD.right_eye_x - int(LASER.laser_width / 2): EYES_COORD.right_eye_x +
                                                                 int(LASER.laser_width / 2)] = dst_right

            roi_left = frame[EYES_COORD.left_eye_y: EYES_COORD.left_eye_y + LASER.left_laser_height,
                       EYES_COORD.left_eye_x - int(LASER.laser_width / 2): EYES_COORD.left_eye_x +
                                                                           int(LASER.laser_width / 2)]
            dst_left = resizing(LASER.laser_left_img,
                                LASER.laser_width,
                                LASER.left_laser_height,
                                LASER.mask_laser_left,
                                LASER.mask_inv_laser_left,
                                roi_left)

            frame[EYES_COORD.left_eye_y: EYES_COORD.left_eye_y + LASER.left_laser_height,
            EYES_COORD.left_eye_x - int(LASER.laser_width / 2): EYES_COORD.left_eye_x +
                                                                int(LASER.laser_width / 2)] = dst_left
    except Exception as exc:
        print('Error caught:')
        print(exc)

    return frame


def draw_bottle(FLAGS, frame, BOTTLE):
    """
    This function allows to draw a bottle
    :param FLAGS: Flags class containing all parameters needed
    :param frame: Represent the frame of the camera
    :param BOTTLE: Bottle class containing all parameters needed
    :return:
    Frame with bottle added
    """

    frame_y_max = frame.shape[0]
    if not FLAGS.EXPLOSION_ON_SCREEN:
        BOTTLE.bottle_height = int(frame.shape[0] / 3)

        roi_bottle = frame[frame_y_max - BOTTLE.bottle_height:frame_y_max,
                     BOTTLE.bottle_rand_pos:BOTTLE.bottle_rand_pos + BOTTLE.bottle_width]

        dst_bottle = resizing(BOTTLE.bottle_img,
                              BOTTLE.bottle_width,
                              BOTTLE.bottle_height,
                              BOTTLE.mask_bottle,
                              BOTTLE.mask_inv_bottle,
                              roi_bottle)

        frame[frame_y_max - BOTTLE.bottle_height:frame_y_max,
        BOTTLE.bottle_rand_pos:BOTTLE.bottle_rand_pos + BOTTLE.bottle_width] = dst_bottle

    return frame


def bottle_was_touched(EYES_COORD, LASER, FLAGS, BOTTLE):
    """
    This function allows to determine the position of the bottle compare to the lasers position
    :param: Eyes coordinates class containing all parameters needed
    :param: Laser class containing all parameters needed
    :param: Flags class containing all parameters needed
    :param: Bottle class containing all parameters needed
    :return:
    FLAGS : BOTTLE_RAND_POSITION : Allows determining if a bottle is inside or outside the laser area
    """
    FLAGS.BOTTLE_TOUCHED = False
    if (
            BOTTLE.bottle_rand_pos < EYES_COORD.right_eye_x + LASER.laser_width < BOTTLE.bottle_rand_pos + BOTTLE.bottle_width) or (
            BOTTLE.bottle_rand_pos < EYES_COORD.right_eye_x < BOTTLE.bottle_rand_pos + BOTTLE.bottle_width) or (
            BOTTLE.bottle_rand_pos < EYES_COORD.left_eye_x + LASER.laser_width < BOTTLE.bottle_rand_pos + BOTTLE.bottle_width) or (
            BOTTLE.bottle_rand_pos < EYES_COORD.left_eye_x < BOTTLE.bottle_rand_pos + BOTTLE.bottle_width) or FLAGS.EXPLOSION_ON_SCREEN == True:
        FLAGS.BOTTLE_TOUCHED = True
    return FLAGS


def new_bottle_position(BOTTLE, EYES_COORD, LASER):
    """
    This function allows to create a new random bottle position inside the frame but outside the lasers' area
    :param BOTTLE: Bottle class containing all parameters needed
    :param EYES_COORD : Eyes coordinates class containing all parameters needed
    :param LASER : Laser class containing all parameters needed
    :return:
    BOTTLE : returning the new position of the bottle
    """
    margin_px = 5
    BOTTLE.bottle_rand_pos = random.randint(margin_px, BOTTLE.x_max - BOTTLE.bottle_width - margin_px)
    marge_left = EYES_COORD.left_eye_x - 4 * margin_px
    marge_right = EYES_COORD.right_eye_x + LASER.laser_width + 4 * margin_px

    a = random.randint(0, 1)
    if a == 0 and BOTTLE.bottle_width < marge_left:
        BOTTLE.bottle_rand_pos = random.randint(0, EYES_COORD.left_eye_x - BOTTLE.bottle_width)
    elif a == 0 and BOTTLE.bottle_width > marge_left:
        BOTTLE.bottle_rand_pos = random.randint(EYES_COORD.right_eye_x, BOTTLE.x_max - BOTTLE.bottle_width)
    if a == 1 and BOTTLE.bottle_width < (BOTTLE.x_max - marge_right):
        BOTTLE.bottle_rand_pos = random.randint(EYES_COORD.right_eye_x + LASER.laser_width,
                                                BOTTLE.x_max - BOTTLE.bottle_width)
    elif a == 1 and BOTTLE.bottle_width > (BOTTLE.x_max - marge_right):
        BOTTLE.bottle_rand_pos = random.randint(0, EYES_COORD.left_eye_x - BOTTLE.bottle_width)

    return BOTTLE
