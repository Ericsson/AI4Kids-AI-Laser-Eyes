import cv2
import time
from utils.gui import display_score, display_countdown, draw_explosion, new_bottle_position, draw_laser, draw_bottle, \
    bottle_was_touched
from utils.init import frame_init, init_video_capture, global_init, load_files, reset_variables
from utils.detect import eyes_detection, eyes_detection_media_pipe
from utils.variables import FLAGS, EYES_COORD, SMILEY, BOTTLE, LASER, EXPLOSION
from utils.language import USED_LANGUAGE, FRENCH_LANGUAGE, ENGLISH_LANGUAGE, change_language

# Language selection
change_language(USED_LANGUAGE, ENGLISH_LANGUAGE)

# Loading images and classifiers
face_cascade, eye_cascade = load_files()

# Play game setting
button = global_init()

# Init video capture
video_capture = init_video_capture()

# Create windows and set is to be full screen
cv2.namedWindow(USED_LANGUAGE.laser_eyes_string, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(USED_LANGUAGE.laser_eyes_string, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#
# cv2.namedWindow(USED_LANGUAGE.laser_eyes_string, cv2.WND_PROP_AUTOSIZE)
# cv2.setWindowProperty(USED_LANGUAGE.laser_eyes_string, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_FULLSCREEN)


while True:
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)

    if button.clicked == False:
        frame = frame_init(frame, button)
        if FLAGS.GAME_COMPLETED:
            # Draw the score at the end of a game
            frame = display_score(frame, SMILEY, FLAGS)
        cv2.setMouseCallback(USED_LANGUAGE.laser_eyes_string, button.handle_event)

    if button.clicked == True:  # Once 'Play' button is clicked, a countdown begins. Then the game starts
        FLAGS.GAME_COMPLETED = False
        if FLAGS.COUNTDOWN > 0:
            # Display countdown
            frame, FLAGS = display_countdown(FLAGS, frame)

            if FLAGS.COUNTDOWN == 0:
                FLAGS.TIMER_GAME = time.time()  # Allows determining the time during a game
                FLAGS.GAME_STATE = True

        if FLAGS.NUMBER_BOTTLE_TOUCHED < 5 and FLAGS.GAME_STATE == True:
            # Detection of each eye and get the coordinates of each eyes
            # EYES_COORD = eyes_detection(EYES_COORD, face_cascade, eye_cascade, frame)
            EYES_COORD = eyes_detection_media_pipe(EYES_COORD, frame)

            # Draw the lasers with the coordinates of each eyes
            frame = draw_laser(frame, EYES_COORD, LASER)

            # Draw the bottle in a random position
            frame = draw_bottle(FLAGS, frame, BOTTLE)

            # Bottle was touched ?
            FLAGS = bottle_was_touched(EYES_COORD, LASER, FLAGS, BOTTLE)

            if FLAGS.BOTTLE_TOUCHED == True:
                # Display explosion
                FLAGS.EXPLOSION_ON_SCREEN = draw_explosion(frame, BOTTLE, EXPLOSION)
                if FLAGS.EXPLOSION_ON_SCREEN == True and FLAGS.START_TIMER == False:
                    FLAGS.START_TIMER = True
                    FLAGS.TIMER_EXP = time.time()
                    FLAGS.NUMBER_BOTTLE_TOUCHED += 1
                if time.time() - FLAGS.TIMER_EXP > 2:
                    BOTTLE = new_bottle_position(BOTTLE, EYES_COORD, LASER)
                    FLAGS.EXPLOSION_ON_SCREEN = False
                    FLAGS.START_TIMER = False

        elif FLAGS.NUMBER_BOTTLE_TOUCHED == 5 and FLAGS.GAME_STATE == True:
            FLAGS.GAME_TIME = time.time() - FLAGS.TIMER_GAME
            button, FLAGS = reset_variables(FLAGS, button)
        # Display on screen how many bottles were touched
        cv2.putText(frame, USED_LANGUAGE.bottle_touched_string.format(FLAGS.NUMBER_BOTTLE_TOUCHED), (150, 50), cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 255, 255), 2)
        if FLAGS.GAME_STATE == True:
            # Display on screen how much time took to touch 5 bottles
            cv2.putText(frame, USED_LANGUAGE.timer_string.format(time.time() - FLAGS.TIMER_GAME), (150, 100),
                        cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 2)

    cv2.imshow(USED_LANGUAGE.laser_eyes_string, frame)
    if cv2.waitKey(30) != -1:
        break
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
