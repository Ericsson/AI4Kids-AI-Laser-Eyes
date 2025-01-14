import numpy as np
import cv2
import mediapipe as mp


def eyes_detection(EYES_COORD, face_cascade, eye_cascade, frame):
    """
    This function allows to detect the eyes and get the coordinates of each eyes at the output
    :param EYES_COORD: Eyes coordinated class store all the features related to the eyes coordinates
    :param face_cascade: This haar_cascade classifier is used to detect faces
    :param eye_cascade: This haar_cascade classifier is used to detect eyes
    :param frame: Frame is the output of the camera
    :return:
    EYES_COORD : Return coordinates of each eye (left+right)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.3,
                                          minNeighbors=4,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_FIND_BIGGEST_OBJECT | cv2.CASCADE_DO_ROUGH_SEARCH)

    EYES_COORD.right_eye_x = -100
    EYES_COORD.left_eye_x = -100
    EYES_COORD.right_eye_y = -100
    EYES_COORD.left_eye_y = -100

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(gray[y:(y + h), x:(x + w)],
                                            scaleFactor=1.05,
                                            minNeighbors=3,
                                            minSize=(10, 10),
                                            flags=cv2.CASCADE_FIND_BIGGEST_OBJECT | cv2.CASCADE_DO_ROUGH_SEARCH)

        index = 0
        eye_2 = [None, None, None, None]
        eye_1 = [None, None, None, None]
        height = np.size(roi_gray, 1)

        # The following code remove un-precise detection of the eyes (detection of mouth as an eye)
        for (ex, ey, ew, eh) in eyes:
            if ey > height / 2:
                pass
            if index == 0:
                eye_1 = [ex, ey, ew, eh]

            elif index == 1:
                eye_2 = [ex, ey, ew, eh]
            index = index + 1

        if (eye_1[0] is not None) and (eye_2[0] is not None):  # Validate detection
            # Attributing right and left eye
            if eye_1[0] < eye_2[0]:
                left_eye = eye_1
                right_eye = eye_2
            else:
                left_eye = eye_2
                right_eye = eye_1

            # Define center coordinates for each eye
            right_eye_center = (
                int(right_eye[0] + (right_eye[2] / 2)),
                int(right_eye[1] + (right_eye[3] / 2)))

            left_eye_center = (
                int(left_eye[0] + (left_eye[2] / 2)),
                int(left_eye[1] + (left_eye[3] / 2)))

            left_x = left_eye_center[0]
            left_y = left_eye_center[1]

            right_x = right_eye_center[0]
            right_y = right_eye_center[1]

            EYES_COORD.right_eye_x = x + right_x
            EYES_COORD.right_eye_y = right_y + ey + y - 100

            EYES_COORD.left_eye_x = x + left_x
            EYES_COORD.left_eye_y = left_y + ey + y - 100

    return EYES_COORD


# Adding media pipe detection
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

def getLandmarks(image):
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = face_mesh.process(image)
    landmarks = results.multi_face_landmarks[0].landmark
    return landmarks, results

# Crop the right eye region
def mp_getRightEye(image, landmarks):
    eye_top = int(landmarks[263].y * image.shape[0])
    eye_left = int(landmarks[362].x * image.shape[1])
    eye_bottom = int(landmarks[374].y * image.shape[0])
    eye_right = int(landmarks[263].x * image.shape[1])
    #right_eye = [int(eye_top+eye_bottom/2), int(eye_left+eye_right/2)]
    right_eye = [int(eye_top)-40, int(eye_left)+10]
    #right_eye = [int(eye_bottom), int(eye_right)]
    return right_eye

def mp_getLeftEye(image, landmarks):
    eye_top = int(landmarks[159].y * image.shape[0])
    eye_left = int(landmarks[33].x * image.shape[1])
    eye_bottom = int(landmarks[145].y * image.shape[0])
    eye_right = int(landmarks[133].x * image.shape[1])
    #left_eye = [int(eye_top+eye_bottom/2), int(eye_left+eye_right/2)]
    left_eye = [int(eye_top)-35, int(eye_left)+10]
    #left_eye = [int(eye_bottom), int(eye_right)]
    return left_eye


def eyes_detection_media_pipe(EYES_COORD, frame):
    """
        This function allows to detect the eyes and get the coordinates of each eyes at the output
        :param EYES_COORD: Eyes coordinated class store all the features related to the eyes coordinates
        :param frame: Frame is the output of the camera
        :return:
        EYES_COORD : Return coordinates of each eye (left+right)
        """
    # img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    EYES_COORD.right_eye_x = -100
    EYES_COORD.left_eye_x = -100
    EYES_COORD.right_eye_y = -100
    EYES_COORD.left_eye_y = -100

    try:
        mp_landmarks, mp_results = getLandmarks(image=frame)
        EYES_COORD.right_eye_y, EYES_COORD.right_eye_x = mp_getRightEye(image=frame, landmarks=mp_landmarks)
        EYES_COORD.left_eye_y, EYES_COORD.left_eye_x = mp_getLeftEye(image=frame, landmarks=mp_landmarks)
    except:
        pass

    frame.setflags(write=1)
    return EYES_COORD