A galaxy game where you have to avoid crashes with asteroids.

1. To start the game:
- open new terminal
- install requirements - run command in terminal:
  - for Windows: pip freeze > requirements.txt
  - for iOS or Linux: pip3 freeze > requirements.txt
- run main.py file
  - for Windows: python main.py
  - for iOS or Linux: python3 main.py
    
2. Game Instructions:

Toolbar:
  - Left top corner - Remaining lives
  - Middle top - Time
  - Right top corner - Destroyed missiles

Receiving points:
  - 1 points for each destroyed missile in the first 1 minute of the game;
  - 5 points for each destroyed missile between 2nd and 4th minute of the game;
  - 25 points for each destroyed missile after the start of the 5th minute of the game;

- Avoid hitting missiles with either moving the spaceship with left, right, up, down keys or with shooting lasers with spacebar key. If 15 missiles destroyed in combo (without loosing live) - spaceship will start shooting 2 lasers at the same time.

- After every 60 seconds (1 minute) you receive a bonus live.

- You can pause/unpause the game with clicking on "P" key or ESCAPE key.

- End of the game is when you loose all your lives.

- Total points are calculated of all points from destroyed missiles + time seconds played.

- At the end you will be asked if you want to play again or close the system.