## About The Project

The goal of this project is to develop a computer vision game for children. The game must be as simple as possible, utilizing the OpenCV and NumPy libraries. The project aims to introduce machine learning concepts to kids and students through games and interactive learning tutorials.



## Game Demo
![This is the pipeline overview](Documentation/demo.gif)



## Overview

The project is divided into several parts:

1. **Image Processing:**  
   Using the Viola-Jones method with Haar cascade classifiers provided by the OpenCV library, this component detects the player’s face and eyes. It includes image processing, such as converting to grayscale, and implementing detection functions. Additionally, it features a function for detecting head rotation within a range of -40 to 40 degrees.

2. **Human-Machine Interaction (HMI):**  
   Based on the detection process, this part establishes the core gameplay mechanics. It involves integrating different ROIs (Regions of Interest) to insert and manipulate images. Elements such as a laser, bottle, and explosion are added to reflect the player’s interactions during the game.

3. **Game Design:**  
   This involves designing the game environment, creating a graphical user interface (GUI), and implementing buttons for gameplay functionality.


![This is the pipeline overview](Documentation/flow_diagram.svg)



## Program Files 

1. **`main.py`**: Runs the game.  
2. **`gui.py`**: Contains display functions for objects that convey information and represent user actions. Objects change color, size, or visibility based on user interaction.  
3. **`language.py`**: Lists all text displays in both French and English.  
4. **`variables.py`**: Defines all game variables, organized by category.  
5. **`detect.py`**: Features for face and eye detection.  
6. **`init.py`**: Contains initializations required at program startup.



## Classes

- **`FILES`**: Gathers resources like image classifiers and game-related images (laser, bottle, smiley, etc.).  
- **`FLAGS`**: Manages the states of flags used in the game, such as timers, countdowns, and bottle counters.  
- **`EYES_COORD`**: Initializes coordinates for each eye center to ensure the game starts even if eyes are not immediately detected.  
- **`SMILEY`**: Manages the mask, resizing, and coordinates of the smiley displayed at the game’s conclusion.  
- **`BOTTLE`**: Manages the mask, resizing, and coordinates of the bottle.  
- **`LASER`**: Manages the mask, resizing, and coordinates of the two lasers.  
- **`EXPLOSION`**: Manages the mask, resizing, and coordinates of the explosion.



## Functions

- **`display_score`**: Displays the player’s score (time taken during a game).  
- **`display_countdown`**: Shows a countdown when the PLAY button is clicked.  
- **`draw_explosion`**: Displays an explosion when a bottle is hit by a laser.  
- **`new_bottle_position`**: Sets the position of the first or subsequent bottles.  
- **`draw_laser`**: Displays lasers using eye coordinates.  
- **`draw_bottle`**: Displays bottles at positions defined by `new_bottle_position`.  
- **`FRENCH_LANGUAGE` | `ENGLISH_LANGUAGE`**: Sets the game’s language.  
- **`load_files`**: Loads classifiers at the program’s start.  
- **`reset_variables`**: Resets game time and variables after a game.  
- **`eyes_detection`**: Detects eyes and retrieves their coordinates.



## Contributors
- Francisco Perdigon Romero [LinkedIn](https://www.linkedin.com/in/fperdigon/) | [Github](https://github.com/fperdigon)
- Pierre Thibault [LinkedIn](https://www.linkedin.com/in/pierre-thibault-089b60a/)
- Marie Nashed [LinkedIn](https://www.linkedin.com/in/julien-reguigne-0b2aa3129/) | [Github](https://github.com/JulieenR)



## License

This project is licensed under the MIT License.
