# ConHex
Game of ConHex in Python with GUI and bot player

About ConHex
---

ConHex is game by Michail Antonow where two players try to create a connected chain of *cells* from one side of the board to the other side. They do this by claiming one empty *position* each turn. If a player first possesses at least half of the *positions* of a *cell*, the *cell* belongs to that player. Cells can't be conquered/taken once owned. More info on the game [on Boardgame Geek](https://boardgamegeek.com/boardgame/10989/conhex) and [on Little Golem](https://docs.littlegolem.net/games/conhex/).

About this project
---

I created a Python application on which you can play ConHex. In the current state, you can play a basic game against yourself. Basic game rules (excluding more advanced features such as swapping are not implemented yet).

Future plans are:

- Provide more info in the GUI about the game: players' name, list of moves, etc.
- Last move indication
- Provide the possibility to load/save/copy-paste games.
- Provide more advanced game statistics, such as a "score" of the players positions.
- Improve the gameplay with swapping options.
- Add and train a bot based on Alpha Zero or Mu Zero deep learning networks.

How to install
---

In its current state, the game is still in alpha-status. Which means that it requires some familiarity with Python to install the game. Basically, it comes down to:

1. Get the source files (`git clone https://github.com/agtoever/ConHex`)
1. Install Python 3.9 including tkinter or better using yum/apt/brew/...
2. Optional (but recommended): create a virtual environment (`python3 -m venv ./ConHex`) and activate it (`cd ./ConHex && source ./bin/activate`)
3. Use pip3 to install PySimpleGUI (`pip3 install PySimpleGUI`)
4. Run the game with: `python3 ./conhex_gui.py`

Feedback, etc.
---

Any feedback is welcome. Please provide it using the [Issues](https://github.com/agtoever/ConHex/issues) section of this GitHub.
