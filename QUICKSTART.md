# 🚀 Quick Start Guide

## Installation (30 seconds)

```bash
# 1. Clone the repository
git clone https://github.com/kirtan597/Minigames.git
cd Minigames/pygame-projects

# 2. Install Pygame
pip install pygame

# 3. Run the game launcher
python game_launcher.py
```

## First Run

1. **Launcher opens** with 8 game cards
2. **Click any game card** to play that game
3. **ESC** returns to launcher
4. **Your score is saved automatically**

## Keyboard Shortcuts in Launcher

```
L    → Open Leaderboards
S    → Open Settings  
ESC  → Quit Launcher
```

## Play a Game

Click any game card to launch. Each game has different controls:

### 🐦 Flappy Bird
- SPACE: Jump
- ESC: Exit to launcher

### 🐍 Snake
- Arrow Keys: Move
- ESC: Exit to launcher

### 🏓 Pong
- Arrow Keys: Control paddle
- ESC: Exit to launcher

### 👾 Monster Run
- SPACE: Jump
- ESC: Exit to launcher

### 👽 Space Invaders
- Arrow Keys: Move
- SPACE: Shoot
- ESC: Exit to launcher

### 🧩 Tetris
- Arrow Keys: Move/Rotate
- SPACE: Drop
- P: Pause
- ESC: Exit to launcher

### 🔢 2048
- Arrow Keys: Slide tiles
- N: New game
- ESC: Exit to launcher

### 🧱 Breakout
- Arrow Keys: Move paddle
- SPACE: Launch ball
- ESC: Exit to launcher

## View Leaderboards

Press **L** in the launcher to see top scores for all games.

- Use **LEFT/RIGHT arrows** to navigate between games
- **ESC** to return to launcher
- Shows your best scores automatically

## Customize Settings

Press **S** in the launcher to open Settings.

- **↑/↓**: Select option
- **←/→**: Change value
- **ESC**: Save and exit

### Available Settings
- **Theme**: 6 vibrant color schemes
- **Difficulty**: Easy, Normal, Hard, Nightmare
- **Volume**: Mute, Low, Medium, High

## Where Are My Scores?

Your scores are saved in two files:

- **minigames_data.json** - Game scores and achievements
- **settings.json** - Your preferences

These are auto-created when you play your first game.

## Troubleshooting

### "pygame not found"
```bash
pip install pygame
```

### Game won't launch
- Make sure you're in the right directory
- Check that Python 3.8+ is installed
- Try running: `python game_launcher.py`

### Scores not saving
- Check that the folder is writable
- Delete `minigames_data.json` to reset data
- Restart the launcher

## Next Steps

1. **Try all 8 games** - Each has unique gameplay
2. **Check Leaderboards** - See your progress
3. **Customize Settings** - Pick your favorite theme
4. **Beat your scores** - Climb the leaderboards!

## Tips & Tricks

### 🎯 General
- Higher scores appear on leaderboards
- Settings apply immediately
- All data is saved automatically

### 🎮 Game Tips
- **Flappy Bird**: Tap repeatedly for smooth flying
- **Snake**: Plan ahead to avoid walls
- **Pong**: Aim for the paddle edges for spins
- **Monster Run**: Jump early to avoid obstacles
- **Space Invaders**: Clear the wave for bonus aliens
- **Tetris**: Plan your next pieces
- **2048**: Don't waste corners
- **Breakout**: Use edges to angle shots

---

## What's Next?

Check out the full [README.md](README.md) for:
- Detailed feature list
- Architecture overview
- Development roadmap
- Technical specifications

---

**Enjoy playing Minigames Central! 🎮**

For bugs or suggestions, open an issue on GitHub.
