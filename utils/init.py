import cv2
from utils.gui import Button
from utils.variables import FILES


def load_files():
    """
    This function is to load some files at the beginning of the program
    :return: The output corresponds to the two classifiers used in the game
    """
    face_cascade = cv2.CascadeClassifier(FILES.face_cascade_path)
    eye_cascade = cv2.CascadeClassifier(FILES.eye_cascade_path)

    return face_cascade, eye_cascade


def init_video_capture():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        exit('The Camera is not opened')
    return video_capture


def global_init():
    """
    This function allows to get the different global variables of the game
    :return:
    button: Create button instance
    """
    button = Button('Play', 300, 390, 300, 500)
    return button


def frame_init(frame, button):
    """
    This function allows to set the different local variables of the game
    :param frame: Represent the frame of the camera
    :param button: Initialisation of the PLAY button to launch the game
    :return:
    frame : Represent the frame of the camera
    """
    button.draw(frame)
    return frame


def reset_variables(FLAGS, button):
    """
    This function is to define the time of the game and reset a variable after a game
    :param FLAGS: Flags class containing all parameters needed
    :param button: Play button to launch the game
    :return:
    button.clicked: Set at FALSE to allows to relaunch a game
    FLAGS: Reset the flags to their original state
    """
    button.clicked = False
    FLAGS.COUNTDOWN = 3
    FLAGS.GAME_STATE = False
    FLAGS.START_TIMER = False
    FLAGS.GAME_COMPLETED = True
    FLAGS.NUMBER_BOTTLE_TOUCHED = 0
    return button, FLAGS
