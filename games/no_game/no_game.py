import pygame
import random
from pygame import mixer
from games import result
import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import asyncio

class HandsTracking:
    def __init__(self):
        self.base_options = python.BaseOptions(
            model_asset_path = "model_hands/hand_landmarker.task"
        )

        self.options = vision.HandLandmarkerOptions(
            base_options = self.base_options,
            num_hands = 2,
            min_hand_detection_confidence = 0.7,
            min_hand_presence_confidence = 0.7,
            running_mode = vision.RunningMode.VIDEO
        )
        
        self.hand_landmarker = vision.HandLandmarker.create_from_options(self.options)

        self.cap = cv2.VideoCapture(0)

        self.frame_timestamp = 0

        self.imshow = "WebCam del Buenestar"
        self.putext = "ola"
        self.misses = 0
        self.score = 0
        self.exercise = 0

    def count_fingers_r(self, l):
        fingers = []

        fingers.append(l[4].x < l[3].x)

        for tip in [8, 12, 16, 20]:
            fingers.append(l[tip].y < l[tip - 1].y)

        return fingers.count(True)

    def count_fingers_l(self, l):
        fingers = []

        fingers.append(l[4].x > l[3].x)

        for tip in [8, 12, 16, 20]:
            fingers.append(l[tip].y < l[tip - 1].y)

        return fingers.count(True)

    def frames(self):
        ret, self.frame = self.cap.read()

        if not ret:
            return

        self.frame = cv2.flip(self.frame, 1)
        rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb_frame)

        self.result = self.hand_landmarker.detect_for_video(mp_image, self.frame_timestamp)

        self.frame_timestamp += 1

    def draw(self):
        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                h, w, c = self.frame.shape

                color = [0, 106, 179]

                for landmark in hand_landmarks:
                    x, y = int(landmark.x * w), int(landmark.y * h)

                    cv2.circle(self.frame, (x, y), 5, (255, 0, color[random.randint(0, 2)]), -1)

                    wrist = hand_landmarks[0]
                    xwrist = int(wrist.x * w)
                    ywrist = int(wrist.y * h)

                    if hand_name == "Left":
                        hand_name = "Derecha"
                        
                        cv2.putText(self.frame, f"Dedos Derecha: {self.count_fingers_r(hand_landmarks)}", (10, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 106), 2)
                    elif hand_name == "Right":
                        hand_name = "Izquierda"
                        cv2.putText(self.frame, f"Dedos Izquierda: {self.count_fingers_l(hand_landmarks)}", (350, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

                    cv2.putText(self.frame, hand_name, (xwrist, ywrist - 20), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (179, 0, 255), 2)

    def next(self):
        self.exercises = [
            self.closeHand_l,
            self.closeHand_r,
            self.closeThumb_r,
            self.closeIndex_r,
            self.closeMidle_r,
            self.closeRing_r,
            self.closePinky_r,
            self.closeThumb_l,
            self.closeIndex_l,
            self.closeMidle_l,
            self.closeRing_l,
            self.closePinky_l,
            self.closeHands,
            ##################
            self.closePinky_r,
            self.closeMidle_l,
            self.closePinky_l,
            self.closeHand_l,
            self.closeMidle_r,
            self.closeIndex_l,
            self.closeThumb_r,
            self.closeThumb_l,
            self.closeHand_r,
            self.closeIndex_l,
            self.closeMidle_l
        ]

        if self.exercise < len(self.exercises):
            self.exercises[self.exercise]()

            return 
        else:
            self.putext = "Completado, presione ESC para salir."

            return

    def closeHand_r(self):
        self.putext = "Suba la mano derecha."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Left":
                    self.putext = "Baje los dedos derechos."

                    if self.count_fingers_r(hand_landmarks) == 0:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeHand_l(self):
        self.putext = "Suba la mano izquierda."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Right":
                    self.putext = "Baje los dedos izquierdos."

                    if self.count_fingers_l(hand_landmarks) == 0:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeThumb_r(self):
        self.putext = "Suba la mano derecha."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Left":
                    self.putext = "Baje el pulgar derecho."

                    if self.count_fingers_r(hand_landmarks) == 4 and hand_landmarks[4].x > hand_landmarks[3].x:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeIndex_r(self):
        self.putext = "Suba la mano derecha."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Left":
                    self.putext = "Baje el índice derecho."

                    if self.count_fingers_r(hand_landmarks) == 4 and hand_landmarks[8].y > hand_landmarks[7].y:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeMidle_r(self):
        self.putext = "Suba la mano derecha."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Left":
                    self.putext = "Baje el medio derecho."

                    if self.count_fingers_r(hand_landmarks) == 4 and hand_landmarks[12].y > hand_landmarks[11].y:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeRing_r(self):
        self.putext = "Suba la mano derecha."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Left":
                    self.putext = "Baje el angular derecho."

                    if self.count_fingers_r(hand_landmarks) == 4 and hand_landmarks[16].y > hand_landmarks[15].y:
                        self.exercise += 1
                        self.score += 10

                        return

    def closePinky_r(self):
        self.putext = "Suba la mano derecha."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Left":
                    self.putext = "Baje el meñique derecho."

                    if self.count_fingers_r(hand_landmarks) == 4 and hand_landmarks[20].y > hand_landmarks[19].y:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeThumb_l(self):
        self.putext = "Suba la mano izquierda."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Right":
                    self.putext = "Baje el pulgar izquierdo."

                    if self.count_fingers_l(hand_landmarks) == 4 and hand_landmarks[4].x < hand_landmarks[3].x:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeIndex_l(self):
        self.putext = "Suba la mano izquierda."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Right":
                    self.putext = "Baje el índice izquierdo."

                    if self.count_fingers_l(hand_landmarks) == 4 and hand_landmarks[8].y > hand_landmarks[7].y:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeMidle_l(self):
        self.putext = "Suba la mano izquierda."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Right":
                    self.putext = "Baje el medio izquierdo."

                    if self.count_fingers_l(hand_landmarks) == 4 and hand_landmarks[12].y > hand_landmarks[11].y:
                        self.exercise += 1
                        self.score += 10

                        return

    def closeRing_l(self):
        self.putext = "Suba la mano izquierda."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Right":
                    self.putext = "Baje el angular izquierdo."

                    if self.count_fingers_l(hand_landmarks) == 4 and hand_landmarks[16].y > hand_landmarks[15].y:
                        self.exercise += 1
                        self.score += 10

                        return

    def closePinky_l(self):
        self.putext = "Suba la mano izquierda."

        if self.result.hand_landmarks:
            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                if hand_name == "Right":
                    self.putext = "Baje el meñique derecho."

                    if self.count_fingers_l(hand_landmarks) == 4 and hand_landmarks[20].y > hand_landmarks[19].y:
                        self.exercise += 1
                        self.score += 10

                        return
                    
    def closeHands(self):
        self.putext = "Suba ambas manos."

        if self.result.hand_landmarks:
            r = False
            l = False

            for hand_landmarks, handedness in zip(self.result.hand_landmarks, self.result.handedness):
                hand_name = handedness[0].category_name

                #if hand_name == "Left":
                self.putext = "Baje todos los dedos."

                if self.count_fingers_r(hand_landmarks) == 0:
                    r = True

                if self.count_fingers_l(hand_landmarks) == 0:
                    l = True

                if r and l:
                    self.exercise += 1
                    self.score += 10

                    return

    def start(self, app, xp, id):
        while True:
            self.frames()

            self.draw()

            self.next()

            cv2.putText(self.frame, self.putext, (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)

            if cv2.waitKey(1) ==  27:
                break

            cv2.imshow(self.imshow, self.frame)

        self.hand_landmarker.close()
        self.cap.release()
        self.misses = len(self.exercises) - self.exercise

        cv2.destroyAllWindows()

        result.results(app, self.misses, self.score, id, xp)