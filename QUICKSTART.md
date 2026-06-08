# Quick Start Guide - Mancala Solver

Get up and running with the Mancala Solver in 2 minutes!

## 🎮 Play Desktop Version (Easiest)

No extra setup needed - just Python!

```bash
python gui.py
```

That's it! A window will open with the Mancala board. Click on your pits (numbered 1-6) to play.

## 🌐 Play Web Version (For Website Hosting)

Want to play in your browser or embed it on your website?

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python app.py
```

### Step 3: Open Browser
Visit: `http://localhost:5000`

## 📊 Run Benchmarks (Check AI Performance)

See how the AI algorithms perform against each other:

```bash
# See how often Alpha-Beta wins against Random
python alphabetavsrand.py

# See how often Minimax wins against Random  
python minimaxvsrand.py

# See Random vs Random (baseline)
python randvsrand.py
```

## 📖 For More Info

- **Gameplay Rules**: See README.md - Rules section
- **Complete Setup**: See README.md
- **Website Deployment**: See DEPLOYMENT.md

## 🎮 GUI Controls

| Action | How |
|--------|-----|
| Make a move | Click a pit (1-6) |
| Change difficulty | Use the Algorithm and Depth dropdowns |
| Start new game | Click "New Game" button |
| View score | Watch the score display at the top |

## 🐛 Troubleshooting

**"Module not found" error?**
```bash
pip install -r requirements.txt
```

**Port already in use?**
```bash
python app.py --port 8000
```

**GUI window won't open?**
Make sure you have tkinter installed:
```bash
# Windows: Usually included with Python
# Mac: brew install python-tk@3.11
# Linux: sudo apt-get install python3-tk
```

## 🚀 Next Steps

1. **Play a few games** to understand how it works
2. **Try different difficulties** (1-8 search depth)
3. **Compare algorithms** (Minimax vs Alpha-Beta)
4. **Read the rules** if you're new to Mancala
5. **Deploy online** (see DEPLOYMENT.md) to share with others

Enjoy! 🎉
