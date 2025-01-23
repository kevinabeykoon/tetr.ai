# Tetr.ai Retro Game


Tetr.ai is a game that fuses both modern and retro aspects of gaming. We took the classic game fo Tetris and put a spin on it: Artificial Intelligence! While all the functionalities of normal Tetris is there, like rotating or moving a block using the arrow keys, we allow users to use their camera and hand to make gestures. The program uses uses MediaPipe's artificial intelligence model to tell the program  where all the joints in the user's hand is. The program then uses a set of logic to determine which gesture the user is making: Left, Right, Rotate, or Speed the Block Up, Hint. The hand gestures work exactly how the arrow keys would. We also built a machine learning model for the Hint System, by raising your hand up, the game will give the user two hints: How many rotations and columns/rows needed to shift by to get the best block location.


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
1. You can run tetris.py and hand_gesture_recognition.py simultaneously in terminal/IDE/mix of both.

## Authors:
- Vivian Ma
- Kevin AbeyKoon
- Joanna Joy
- Yifan Qin

## References
1. https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer
2. https://zhuanlan.zhihu.com/p/353922161
3. 
