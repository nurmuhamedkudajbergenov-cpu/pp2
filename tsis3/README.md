# TSIS 3 — Racer Game

## Setup

```bash
pip install pygame
python main.py
```

## Controls
- **← →** Arrow keys — change lanes
- **ESC** — back to main menu

## Features
- ✅ Lane hazards (slow zones, oil spills, speed bumps)
- ✅ Dynamic road events (nitro strips, moving barriers)
- ✅ Traffic cars with difficulty scaling
- ✅ 3 Power-ups: Nitro, Shield, Repair
- ✅ Score = distance + coins × 10
- ✅ Distance meter with progress bar
- ✅ Leaderboard saved to `leaderboard.json` (Top 10)
- ✅ Username entry before race
- ✅ Main Menu, Game Over, Leaderboard, Settings screens
- ✅ Settings saved to `settings.json` (sound, car color, difficulty)

## File Structure
```
TSIS3/
├── main.py          # Entry point & state machine
├── racer.py         # Game logic (player, traffic, obstacles, power-ups)
├── ui.py            # All screens (menu, game over, leaderboard, settings)
├── game_states.py   # State enum
├── persistence.py   # JSON save/load
├── settings.json    # User preferences
└── leaderboard.json # Top 10 scores
```
