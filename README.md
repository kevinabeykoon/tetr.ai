# Tetr.ai Game x AI

<a href="https://www.youtube.com/watch?v=yfEJuUH45Xg" target="_blank"><img src="https://github.com/user-attachments/assets/354f9527-7515-4042-befd-8eb36ad5f1af" 
alt="Image of program and the demo link" width="1252" /></a>




Tetr.ai is a game that fuses both modern and retro aspects of gaming. We took the classic game fo Tetris and put a spin on it: Artificial Intelligence! While all the functionalities of normal Tetris is there, like rotating or moving a block using the arrow keys, we allow users to use their camera and hand to make gestures. The program uses uses MediaPipe's artificial intelligence model to tell the program  where all the joints in the user's hand is. The program then uses a set of logic to determine which gesture the user is making: Left, Right, Rotate, or Speed the Block Up, Hint. The hand gestures work exactly how the arrow keys would. We also built a machine learning model for the Hint System, by raising your hand up, the game will give the user two hints: How many rotations and columns/rows needed to shift by to get the best block location.

## Demo
You can click the image above or copy and paste the following link into your browser: [https://www.youtube.com/watch?v=yfEJuUH45Xg](https://www.youtube.com/watch?v=yfEJuUH45Xg)

## Built With
1. Python
2. MediaPipe framework from Google Developers
3. pygame

## Getting Started
### Dependencies
The following libraries must be downloaded within the scope of the project:

For the hand_gesture_recognition file:
* pip install opencv-python
* pip install mediapipe

For the Tetris game:
* pip install pygame
Outsourced files:
* PokemonGb-RAeo.ttf (font)
* tetris_music.mp3 (audio)

### Running the Program
Run tetris.py and hand_gesture_recognition.py simultaneously in terminal/IDE/mix of both.

## Authors:
- Vivian Ma
- Kevin Abeykoon
- Joanna Joy
- Yifan Qin

## References
1. https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer
2. https://zhuanlan.zhihu.com/p/353922161

