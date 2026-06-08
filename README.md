# Mancala Solver

A sophisticated implementation of the Mancala game with AI players using minimax and alpha-beta pruning algorithms.

## Table of Contents
- [Game Overview](#game-overview)
- [Rules](#rules)
- [Game Rules Used](#game-rules-used)
- [How to Run](#how-to-run)
- [Algorithms](#algorithms)
- [Project Structure](#project-structure)

## Game Overview

Mancala is an ancient family of board games played around the world. In this implementation, we're using the **Kalaha** variant, one of the most popular modern versions. The game is played between two players who move stones around pits on a board, attempting to collect the most stones in their mancala (scoring pit).

### Basic Concept
- Each player has a row of 6 pits with 4 stones each, plus a larger mancala (scoring bin) to the side
- Players take turns picking up all stones from one of their pits and distributing them one by one around the board
- The goal is to collect more stones in your mancala than your opponent

## Rules

### Game Rules Used in This Implementation

1. **Board Setup**: 
   - 6 pits per player, each starting with 4 stones
   - 1 mancala (scoring bin) per player
   - Total: 48 stones on the board

2. **Turn Mechanics**:
   - Players select one of their own pits that contains stones
   - All stones from that pit are picked up and distributed counterclockwise, one stone per pit
   - Stones are placed in the player's own mancala, but never in the opponent's mancala

3. **Capturing (Bonus Feature)**:
   - If the last stone placed in a move lands in an empty pit belonging to the player, that player captures both that stone AND all stones in the opposite pit of the opponent
   - All captured stones go into the player's mancala

4. **Extra Turn**:
   - If the last stone lands in the player's mancala, they get to play again (not implemented in current version)

5. **Game End**:
   - The game ends when all pits on one side of the board are empty
   - Remaining stones on the losing side go to that player's mancala
   - Player with more stones in their mancala wins

## How to Run

### Requirements
- Python 3.6 or higher
- Flask 2.0+ (see requirements.txt)

### Installation
1. Clone or download this repository
2. Navigate to the folder:
   ```bash
   cd MancalaSolver
   ```

### Web Application

First, install Flask dependencies:
```bash
pip install -r requirements.txt
```

Then run the Flask server:
```bash
python app.py
```

Open your browser to: `http://localhost:5000`

The web version features:
- Beautiful responsive design
- Play from any browser
- Share link with others
- Mobile-friendly interface
- Real-time board updates

### Running Benchmark Comparisons
Test different AI algorithms against each other:

```bash
# Alpha-Beta vs Random (100 games)
python alphabetavsrand.py

# Minimax vs Random (100 games)
python minimaxvsrand.py

# Random vs Random (100 games)
python randvsrand.py
```

## Algorithms

### Alpha-Beta Pruning (`alphabeta.py`)
An optimized version of minimax that eliminates unnecessary branches in the game tree, making it much faster. 
- **Performance**: Faster than minimax
- **Results**: Defeats random players ~75-85% of the time
- **Depth**: Configurable search depth (default: 5)

### Minimax (`minimax.py`)
A recursive algorithm that explores the entire game tree to a certain depth, choosing moves that maximize the player's advantage.
- **Performance**: Slower but thorough
- **Results**: Defeats random players ~70-80% of the time
- **Depth**: Configurable search depth (default: 5)

### Game Tree (`game_tree.py`)
Builds a game tree by simulating all possible moves from the current position up to a specified depth.

## Project Structure

```
MancalaSolver/
├── README.md                    # This file - Main documentation
├── requirements.txt             # Python dependencies for web version
├── app.py                       # Flask web server
├── mancala.py                   # Core game logic
├── alphabeta.py                 # Alpha-beta pruning algorithm
├── minimax.py                   # Minimax algorithm
├── game_tree.py                 # Game tree builder
├── alphabetavsrand.py           # Benchmark: AlphaBeta vs Random
├── minimaxvsrand.py             # Benchmark: Minimax vs Random
├── randvsrand.py                # Benchmark: Random vs Random
└── templates/
    └── index.html               # Web app frontend (Flask)
```

## Future Enhancements

- [ ] Extra turn rule (landing in mancala)
- [ ] Difficulty presets for web interface
- [ ] Game statistics and win rates
- [ ] Network multiplayer support
- [ ] Mobile app version

## License

Feel free to use and modify for educational purposes.
