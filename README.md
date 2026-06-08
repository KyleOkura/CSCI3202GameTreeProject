# Mancala Solver

A sophisticated implementation of the Mancala game with AI players using minimax and alpha-beta pruning algorithms.

## Table of Contents
- [Game Overview](#game-overview)
- [Rules](#rules)
- [Game Rules Used](#game-rules-used)
- [How to Run](#how-to-run)
- [GUI Application](#gui-application)
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
- For web version: Flask 2.0+ (see requirements.txt)

### Installation
1. Clone or download this repository
2. Navigate to the folder:
   ```bash
   cd MancalaSolver
   ```

### Option 1: Desktop GUI Application (Recommended for Local Play)
```bash
python gui.py
```
The GUI allows you to play against AI opponents with different difficulty levels.

**Features:**
- Interactive board visualization
- Select algorithm (Minimax or Alpha-Beta)
- Adjustable search depth
- Game log tracking
- Simple one-click gameplay

### Option 2: Web Application (Recommended for Website Deployment)

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

**For Deployment:** See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on hosting this as a live demo on your website (Heroku, PythonAnywhere, your own server, etc.)

### Option 3: Running Benchmark Comparisons
Test different AI algorithms against each other:

```bash
# Alpha-Beta vs Random (100 games)
python alphabetavsrand.py

# Minimax vs Random (100 games)
python minimaxvsrand.py

# Random vs Random (100 games)
python randvsrand.py
```

## GUI Application

The GUI provides an interactive way to play Mancala:

### Features
- **Visual Board Display**: See the current game state clearly with color-coded pits
- **AI Opponents**: Play against intelligent AI using minimax or alpha-beta pruning
- **Difficulty Levels**: Choose search depth (1-8) for AI intelligence
- **Algorithm Selection**: Switch between minimax and alpha-beta algorithms on the fly
- **Move History**: Track all moves made in the game
- **Easy Reset**: Start a new game anytime
- **Real-time Feedback**: Immediate visual updates and game log

### Playing
1. Click on one of your pits (numbered 1-6, highlighted in green) to make a move
2. The AI will automatically respond with its move
3. Watch the stone distribution happen in real-time on the board
4. The game ends automatically when one side is empty
5. Your mancala and opponent's mancala scores are displayed on the sides

## Web Application & Online Demo

Deploy the Mancala Solver as a live web application on your personal website!

### Features
- **Browser-based**: Play from any device with a web browser
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Beautiful UI**: Modern, intuitive interface
- **Real-time Updates**: Smooth board animations
- **Shareable**: Get a URL to share with others
- **Configurable AI**: Adjust algorithm and search depth from the UI

### Running Locally
```bash
pip install -r requirements.txt
python app.py
```
Visit `http://localhost:5000` in your browser.

### Deploying Online

For complete deployment instructions, see **[DEPLOYMENT.md](DEPLOYMENT.md)**

**Quick Summary of Options:**
- **Heroku** (Recommended): Free tier available, easy setup, 30-min sleep on free
- **PythonAnywhere**: Free tier, always running, beginner-friendly
- **DigitalOcean**: $5-12/month, best performance, full control
- **AWS/Azure**: Enterprise-grade, pay-as-you-go

After deployment, you can:
- Embed the game in your website with an `<iframe>`
- Use a custom domain (mancala.yoursite.com)
- Add SSL/HTTPS for security
- Monitor performance and uptime

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
├── DEPLOYMENT.md                # Web deployment guide
├── requirements.txt             # Python dependencies for web version
├── gui.py                       # Desktop GUI application (tkinter)
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

## Deploying as a Live Demo on Your Website

To host this as an interactive demo on your personal website, see the comprehensive **[DEPLOYMENT.md](DEPLOYMENT.md)** guide which includes:

- **Step-by-step instructions** for Heroku, PythonAnywhere, and self-hosted options
- **Cost comparison** of different platforms
- **Security considerations** for production
- **Embedding options** (iframe, subdomain, custom domain)
- **Troubleshooting** common deployment issues
- **Performance optimization** tips

### Quick Start for Deployment

1. **Choose a Platform** (see DEPLOYMENT.md for details):
   - Heroku (Free, easiest setup)
   - PythonAnywhere (Free, always running)
   - Your own server (Full control)

2. **Follow Platform-Specific Guide** in DEPLOYMENT.md

3. **Test** the deployed application

4. **Embed or Share** with your audience

Most platforms can have you live in under 15 minutes!

## Future Enhancements

- [ ] Extra turn rule (landing in mancala)
- [ ] Difficulty selection in GUI
- [ ] Game statistics and win rates
- [ ] Network multiplayer support
- [ ] Mobile app version

## License

Feel free to use and modify for educational purposes.
