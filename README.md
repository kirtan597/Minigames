# 🎮 Minigames Central

A unified, AI/ML educational gaming platform featuring 8+ games designed for children. Built with Pygame, featuring a professional launcher dashboard, persistent storage, achievements, leaderboards, and beautiful UI.

**Status**: Phase 2.2 - Core games + leaderboards + settings (5/8 games + 3 new games)

---

## 📋 Features

### 🎯 Core Platform
- **8 Games** with smooth 60 FPS gameplay
- **Widescreen Design** (1280x720) optimized for modern displays
- **Professional Launcher** with animated card UI and particle effects
- **Child-Friendly Interface** with vibrant colors and clear navigation

### 🏆 Leaderboard System
- Top 10 scores per game
- Gold/Silver/Bronze medals (🥇🥈🥉)
- Navigate between games easily
- Shows player name and score date
- Auto-updated on game completion

### ⚙️ Settings & Customization
- **6 Vibrant Themes**:
  - Dark (default)
  - Light
  - Neon
  - Retro
  - Pastel
  - Cyberpunk
- **Difficulty Settings**: Easy, Normal, Hard, Nightmare
- **Volume Control**: Mute, Low, Medium, High
- **Persistent Settings** (saves to JSON)

### 📊 Data System
- **High Scores**: Top 100 per game, persistent storage
- **Achievements**: Unlock system for milestones
- **Player Statistics**: Track games played, playtime, wins, streaks
- **Game Sessions**: Record history of recent games
- **Export Functionality**: Analytics-ready data

### 🎮 Games Included

#### Original Games
1. **🐦 Flappy Bird** - Endless flying through obstacles
2. **🐍 Snake** - Classic grid-based movement game
3. **🏓 Pong** - Player vs AI paddle game
4. **👾 Monster Run** - Jump over obstacles and collect coins
5. **👽 Space Invaders** - Wave-based shooting game

#### New Games
6. **🧩 Tetris** - Classic block-falling puzzle (Breakout)
7. **🔢 2048** - Tile merging puzzle game
8. **🧱 Breakout** - Brick-breaking game

---

## 🚀 Getting Started

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/kirtan597/Minigames.git
cd Minigames/pygame-projects
```

2. **Install dependencies**:
```bash
pip install pygame
```

3. **Run the launcher**:
```bash
python game_launcher.py
```

### Controls in Launcher

| Key | Action |
|-----|--------|
| **Click** | Launch a game |
| **L** | Open Leaderboards |
| **S** | Open Settings |
| **ESC** | Quit |

### Controls in Games

**Flappy Bird**
- SPACE: Jump
- ESC: Quit

**Snake**
- Arrow Keys: Move
- ESC: Quit

**Pong**
- Arrow Keys: Move paddle
- ESC: Quit

**Monster Run**
- SPACE: Jump
- ESC: Quit

**Space Invaders**
- Arrow Keys: Move
- SPACE: Shoot
- ESC: Quit

---

## 📁 Project Structure

```
pygame-projects/
├── game_launcher.py          # Main launcher with UI
├── data_manager.py           # Persistent data storage
├── leaderboard_screen.py     # Leaderboard display
├── settings_screen.py        # Settings and themes
├── player_name_input.py      # Player name dialog
│
├── FlappyBird/
│   └── main.py              # Flappy Bird game
├── Snake/
│   └── main.py              # Snake game
├── Pong/
│   └── main.py              # Pong game
├── MonsterRun/
│   └── main.py              # Monster Run game
├── SpaceInvaders/
│   └── main.py              # Space Invaders game
├── Tetris/
│   └── main.py              # Tetris game
├── Game2048/
│   └── main.py              # 2048 game
├── Breakout/
│   └── main.py              # Breakout game
│
├── minigames_data.json       # Persistent storage (auto-created)
├── settings.json             # User settings (auto-created)
└── README.md                 # This file
```

---

## 📊 Data Storage

### minigames_data.json
```json
{
  "high_scores": {
    "flappy_bird": [...],
    "snake": [...],
    ...
  },
  "achievements": {...},
  "player_stats": {...},
  "game_sessions": [...]
}
```

### settings.json
```json
{
  "theme": "dark",
  "difficulty": "Normal",
  "volume": "High"
}
```

---

## 🎯 Development Roadmap

### ✅ Phase 2 (Current)
- [x] 5 original games with scoring
- [x] 3 new games (Tetris, 2048, Breakout)
- [x] Data persistence system
- [x] Leaderboard display
- [x] Settings screen with themes
- [x] Player name input dialog

### 📋 Phase 3 (Planned)
- [ ] Integrated player name system
- [ ] Achievement unlocking
- [ ] Statistics dashboard
- [ ] Sound effects and music
- [ ] Difficulty integration with games

### 🚀 Phase 4 (Planned)
- [ ] 12+ new games
- [ ] Multiplayer support
- [ ] Online leaderboards
- [ ] Badges and rewards system
- [ ] Performance analytics

### 🌟 Phase 5 (Planned)
- [ ] AI/ML tutorials
- [ ] Educational content integration
- [ ] Custom game creation
- [ ] Mobile version
- [ ] Community features

---

## 🛠️ Technical Details

### Requirements
- Python 3.8+
- Pygame 2.0+

### Architecture
- **Modular Design**: Each game is independent
- **Central Data Manager**: Single source of truth for scores
- **Subprocess Isolation**: Games run in separate processes
- **JSON Storage**: Simple, portable data format
- **Event-Driven UI**: Responsive particle animations

### Performance
- **60 FPS** target across all games
- **Minimal Memory Footprint**: <100MB typical
- **Fast Load Times**: <2 seconds to launcher
- **Smooth Animations**: GPU-accelerated rendering

---

## 📝 License

This project is part of the Minigames Central educational platform.

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new games
- Improve existing games
- Enhance the UI
- Add new features
- Report bugs

---

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

## 🎓 Educational Value

Minigames Central is designed to:
- **Teach Game Development Fundamentals**
- **Showcase Physics & Collision Detection**
- **Demonstrate UI/UX Design Principles**
- **Introduce Data Persistence**
- **Explore Achievement Systems**
- **Practice Modular Architecture**

---

## 🔮 Future Vision

Minigames Central aims to become a comprehensive AI/ML educational gaming platform that:
- Makes learning fun and engaging
- Provides insight into game mechanics
- Teaches programming concepts
- Builds community among young developers
- Integrates with educational curricula

---

## 🎮 Latest Updates

**v2.2** (Current)
- Added Leaderboard Screen (L key)
- Added Settings Screen (S key) with 6 themes
- Added Player Name Input Dialog
- Integrated keyboard shortcuts
- Created comprehensive data manager

**v2.1**
- Added Tetris, 2048, Breakout games
- Updated launcher with 8-game support
- Created development roadmap

**v2.0**
- Core platform architecture
- 5 original games implemented
- Data persistence system

---

**Made with ❤️ by Minigames Central Team**
