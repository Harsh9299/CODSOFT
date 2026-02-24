# 🚀 Quick Start Guide

## Installation (Takes 2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Choose Your Interface

#### Option A - Terminal/CLI (Simplest)
```bash
python tic_tac_toe_ai.py
```

#### Option B - Desktop GUI (Beautiful)
```bash
python tic_tac_toe_gui.py
```

#### Option C - Web App (Professional)
```bash
# Terminal 1: Start server
python app.py

# Browser: Open
http://localhost:5000
```

## Usage Tips

### Terminal Version
- Enter numbers 1-9 to make moves
- Type 'u' to undo your last move
- After game: choose (p)lay, (s)tatistics, or (q)uit

### GUI Version
- Click cells to make moves
- Use buttons: New Game, Undo, Statistics
- Change difficulty or player anytime

### Web Version
- Click cells to play
- All features available through UI
- Works on mobile devices

## Running Tests
```bash
pytest test_tic_tac_toe.py -v
```

## Common Issues

**Import Error:** Install requirements first
```bash
pip install -r requirements.txt
```

**Port 5000 in use:** Change port in app.py
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Project Highlights for Portfolio

✅ **Advanced Algorithms:** Minimax, Alpha-Beta Pruning
✅ **Full-Stack:** Backend API + Frontend UI
✅ **Testing:** Comprehensive unit tests (>90% coverage)
✅ **Multiple UIs:** CLI, Desktop GUI, Web App
✅ **Clean Code:** OOP, documentation, best practices
✅ **Features:** Difficulty levels, undo, statistics

## For Internship Applications

**Mention in Resume:**
- Implemented unbeatable AI using Minimax with Alpha-Beta Pruning
- Built full-stack web application with Flask and vanilla JavaScript
- Achieved >90% test coverage using pytest
- Demonstrated OOP principles and clean architecture

**In Interviews:**
- Explain Minimax algorithm and Alpha-Beta optimization
- Discuss time complexity improvements (O(b^d) → O(b^(d/2)))
- Show different interfaces (CLI, GUI, Web)
- Walk through test coverage and edge cases

## Next Steps

1. **Play the game** in all three versions
2. **Read the code** with detailed comments
3. **Run the tests** to see coverage
4. **Deploy the web app** (Heroku, Railway, etc.)
5. **Add to GitHub** with screenshots
6. **Update LinkedIn** with project details

---

**Need Help?** Check README.md for detailed documentation.

**Ready to Deploy?** See deployment guides in README.md.
