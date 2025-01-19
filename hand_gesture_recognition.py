import cv2
import mediapipe as mp
import time


valid_commands = ['up', 'down', 'left', 'right']
file_path='command.txt'

# Initialize MediaPipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# Function to recognize gestures based on landmarks
def recognize_gesture(landmarks):
    if landmarks:
        # Get the y-coordinates of specific landmarks
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
        command_gesture = None

        if (INDEX_FINGER_TIP_X > INDEX_FINGER_MCP_X > WRIST_X
                and INDEX_FINGER_PIP_X > MIDDLE_FINGER_TIP_X
                and INDEX_FINGER_PIP_X > RING_FINGER_TIP_X
                and INDEX_FINGER_PIP_X > PINKY_TIP_X
                and INDEX_FINGER_MCP_Y < MIDDLE_FINGER_MCP_Y
                and INDEX_FINGER_MCP_Y < RING_FINGER_MCP_Y
                and INDEX_FINGER_MCP_Y < PINKY_MCP_Y):
            command_gesture = "left"
            return command_gesture

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
            return command_gesture

        else:
            return "Unidentified"
    return "No Hand Detected"


# Initialize camera
cap = cv2.VideoCapture(1)

# Timestamp for controlling output rate
last_output_time = 0
output_interval = 0.5  # seconds

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
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

                    if gesture == 'exit':
                        print("game finished")
                        break

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
