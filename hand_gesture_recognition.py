"""
hand_gesture_recognition.py
Summary: This program uses MediaPipe from Google Developers to map a graph
of 21 landmarks (points) on a hand in a live webcam stream. It then
recognizes the gesture and prints the gesture in a text file which is
later used by the Tetris file. It recognizes the gestures through a
series of set comparisons, it determines the gesture to be one of the
following: [right, left, up, down, openfist, closedfist, unidentified].
Please note there are special ways of depicting this gestures; right
down, and up are conveyed through a Thumbs Up in the respective directions.
Left is done by an extended index finger and retracted all other fingers.

Authors: Kevin Abeykoon, Yifan Qin

Citations: The later half of this program and gesture recognition is based off the MediaPipe Documentation
1. https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
2. https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/hands.md

Notes:
In order to run the program, 2 packages must be installed, to do so, run the following lines:
1. pip install opencv-python
2. pip install mediapipe
"""

import cv2 # For camera interaction
import mediapipe as mp # For hand landmark recognition and locating
import time # To slow down the gesture reconition for the related Tetris game

# Initialize MediaPipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

valid_commands = ['up', 'down', 'left', 'right', 'closedfist', 'openpalm']
file_path='command.txt'

# Function to recognize gestures based on landmarks
def recognize_gesture(landmarks):
    command_gesture = None

    if landmarks:
        # Get the x and y coordinates of all landmarks
        WRIST_X = landmarks[0].x
        WRIST_Y = landmarks[0].y
        THUMB_CMC_X = landmarks[1].x
        THUMB_CMC_Y = landmarks[1].y
        THUMB_MCP_X = landmarks[2].x
        THUMB_MCP_Y = landmarks[2].y
        THUMB_IP_X = landmarks[3].x
        THUMB_IP_Y = landmarks[3].y
        THUMB_TIP_X = landmarks[4].x
        THUMB_TIP_Y = landmarks[4].y
        INDEX_FINGER_MCP_X = landmarks[5].x
        INDEX_FINGER_MCP_Y = landmarks[5].y
        INDEX_FINGER_PIP_X = landmarks[6].x
        INDEX_FINGER_PIP_Y = landmarks[6].y
        INDEX_FINGER_DIP_X = landmarks[7].x
        INDEX_FINGER_DIP_Y = landmarks[7].y
        INDEX_FINGER_TIP_X = landmarks[8].x
        INDEX_FINGER_TIP_Y = landmarks[8].y
        MIDDLE_FINGER_MCP_X = landmarks[9].x
        MIDDLE_FINGER_MCP_Y = landmarks[9].y
        MIDDLE_FINGER_PIP_X = landmarks[10].x
        MIDDLE_FINGER_PIP_Y = landmarks[10].y
        MIDDLE_FINGER_DIP_X = landmarks[11].x
        MIDDLE_FINGER_DIP_Y = landmarks[11].y
        MIDDLE_FINGER_TIP_X = landmarks[12].x
        MIDDLE_FINGER_TIP_Y = landmarks[12].y
        RING_FINGER_MCP_X = landmarks[13].x
        RING_FINGER_MCP_Y = landmarks[13].y
        RING_FINGER_PIP_X = landmarks[14].x
        RING_FINGER_PIP_Y = landmarks[14].y
        RING_FINGER_DIP_X = landmarks[15].x
        RING_FINGER_DIP_Y = landmarks[15].y
        RING_FINGER_TIP_X = landmarks[16].x
        RING_FINGER_TIP_Y = landmarks[16].y
        PINKY_MCP_X = landmarks[17].x
        PINKY_MCP_Y = landmarks[17].y
        PINKY_PIP_X = landmarks[18].x
        PINKY_PIP_Y = landmarks[18].y
        PINKY_DIP_X = landmarks[19].x
        PINKY_DIP_Y = landmarks[19].y
        PINKY_TIP_X = landmarks[20].x
        PINKY_TIP_Y = landmarks[20].y



        # Making the comparisons
        # Hand is pointing left
        if (INDEX_FINGER_TIP_X > INDEX_FINGER_MCP_X > WRIST_X
                and INDEX_FINGER_PIP_X > MIDDLE_FINGER_TIP_X
                and INDEX_FINGER_PIP_X > RING_FINGER_TIP_X
                and INDEX_FINGER_PIP_X > PINKY_TIP_X
                and INDEX_FINGER_MCP_Y < MIDDLE_FINGER_MCP_Y
                and INDEX_FINGER_MCP_Y < RING_FINGER_MCP_Y
                and INDEX_FINGER_MCP_Y < PINKY_MCP_Y
                and WRIST_Y < PINKY_MCP_Y
                and THUMB_TIP_Y > INDEX_FINGER_MCP_Y
                and WRIST_Y > INDEX_FINGER_TIP_Y):
            command_gesture = "left"

        # Hand is pointing right
        elif (WRIST_X > THUMB_CMC_X > THUMB_MCP_X > THUMB_IP_X > THUMB_TIP_X
                and PINKY_MCP_X > INDEX_FINGER_MCP_X > THUMB_IP_X

                and WRIST_Y > INDEX_FINGER_MCP_Y
                and WRIST_Y > MIDDLE_FINGER_MCP_Y
                and WRIST_Y > RING_FINGER_MCP_Y
                and WRIST_Y > PINKY_MCP_Y
                and INDEX_FINGER_TIP_Y > INDEX_FINGER_MCP_Y
                and MIDDLE_FINGER_TIP_Y > MIDDLE_FINGER_MCP_Y
                and RING_FINGER_TIP_Y > RING_FINGER_MCP_Y
                and PINKY_TIP_Y > PINKY_MCP_Y):
            command_gesture = "right"

        # Hand is pointing up
        elif (INDEX_FINGER_PIP_X > INDEX_FINGER_TIP_X
              and MIDDLE_FINGER_PIP_X > MIDDLE_FINGER_TIP_X
              and RING_FINGER_PIP_X > RING_FINGER_TIP_X
              and PINKY_PIP_X > PINKY_TIP_X > WRIST_X
              and  (THUMB_TIP_Y < THUMB_IP_Y < THUMB_MCP_Y < THUMB_CMC_Y  < WRIST_Y  <PINKY_TIP_Y)):
            command_gesture = "up"

        # Hand is pointing down
        elif (INDEX_FINGER_PIP_X > INDEX_FINGER_TIP_X
              and MIDDLE_FINGER_PIP_X > MIDDLE_FINGER_TIP_X
              and RING_FINGER_PIP_X > RING_FINGER_TIP_X
              and PINKY_PIP_X > PINKY_TIP_X > WRIST_X
              and  (THUMB_TIP_Y > THUMB_IP_Y > THUMB_MCP_Y > THUMB_CMC_Y  > WRIST_Y  > PINKY_TIP_Y)):
            command_gesture = "down"

        # Hand is a closed fist
        elif (WRIST_Y > THUMB_MCP_Y
              and WRIST_Y > INDEX_FINGER_MCP_Y
              and WRIST_Y > MIDDLE_FINGER_MCP_Y
              and WRIST_Y > RING_FINGER_MCP_Y
              and WRIST_Y > PINKY_MCP_Y
              and THUMB_MCP_Y > INDEX_FINGER_MCP_Y
              and THUMB_MCP_Y > MIDDLE_FINGER_MCP_Y
              and THUMB_MCP_Y > RING_FINGER_MCP_Y
              and THUMB_MCP_Y > PINKY_MCP_Y

             and PINKY_MCP_X > RING_FINGER_MCP_X > MIDDLE_FINGER_MCP_X > INDEX_FINGER_MCP_X
             and THUMB_TIP_X > THUMB_IP_X
             and PINKY_MCP_X > THUMB_CMC_X):
            command_gesture = "closedfist"

        # Hand is an open palm
        elif (PINKY_TIP_Y < PINKY_DIP_Y < PINKY_PIP_Y < PINKY_MCP_Y
              and RING_FINGER_TIP_Y < RING_FINGER_DIP_Y < RING_FINGER_PIP_Y < RING_FINGER_MCP_Y
              and MIDDLE_FINGER_TIP_Y < MIDDLE_FINGER_DIP_Y < MIDDLE_FINGER_PIP_Y < MIDDLE_FINGER_MCP_Y
              and INDEX_FINGER_TIP_Y < INDEX_FINGER_DIP_Y < INDEX_FINGER_PIP_Y < INDEX_FINGER_MCP_Y
              and THUMB_TIP_Y < THUMB_IP_Y < THUMB_MCP_Y < THUMB_CMC_Y < WRIST_Y):
            command_gesture = "openpalm"
        else:
            command_gesture =  "Unidentified"

    return command_gesture


# Controlling output rate
last_output_time = 0
output_interval = 0.5  # seconds

# Most of the code after this line is from the documentation
# Initialize camera
cap = cv2.VideoCapture(1)

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Draw hand landmarks and detect gestures
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # Recognize gesture and control output rate
                current_time = time.time()
                if current_time - last_output_time >= output_interval:
                    gesture = recognize_gesture(hand_landmarks.landmark)

                    if gesture in valid_commands:
                        with open(file_path, 'w') as file:
                            file.write(gesture)
                        print("Command", gesture, "is written in file")
                    else:
                        print("⚠️ invalid command")


                    last_output_time = current_time

        # Display the frame
        cv2.imshow('Hand Gesture Recognition', frame)

        # Break on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
