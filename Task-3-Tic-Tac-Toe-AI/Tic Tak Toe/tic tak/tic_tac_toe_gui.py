"""
Tic-Tac-Toe GUI Application using Tkinter
Author: AI Assistant
Date: February 19, 2026

Beautiful GUI interface for the Tic-Tac-Toe AI game with:
- Modern, responsive design
- Visual feedback for moves
- Difficulty selection
- Statistics display
- Undo functionality
- Smooth animations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List
import sys
# Import the game logic from the main file
sys.path.append('.')
from tic_tac_toe_ai import TicTacToe, GameStatistics


class TicTacToeGUI:
    """GUI Application for Tic-Tac-Toe game using Tkinter."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Tic-Tac-Toe AI - Pro Edition")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Color scheme
        self.bg_color = "#1e1e2e"
        self.button_bg = "#2d2d44"
        self.button_hover = "#3d3d54"
        self.x_color = "#ff6b6b"
        self.o_color = "#4ecdc4"
        self.text_color = "#ffffff"
        self.accent_color = "#a8dadc"
        
        self.root.configure(bg=self.bg_color)
        
        # Game instance
        self.game = TicTacToe()
        self.buttons: List[tk.Button] = []
        self.game_started = False
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the complete user interface."""
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🎮 TIC-TAC-TOE AI 🎮",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Powered by Minimax & Alpha-Beta Pruning",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle_label.pack()
        
        # Info frame
        self.info_frame = tk.Frame(self.root, bg=self.bg_color)
        self.info_frame.pack(pady=10)
        
        self.info_label = tk.Label(
            self.info_frame,
            text="Select difficulty to start",
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.info_label.pack()
        
        self.status_label = tk.Label(
            self.info_frame,
            text="",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.status_label.pack()
        
        # Difficulty selection
        diff_frame = tk.Frame(self.root, bg=self.bg_color)
        diff_frame.pack(pady=10)
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).grid(row=0, column=0, padx=5)
        
        self.difficulty_var = tk.StringVar(value="hard")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        
        for i, (label, value) in enumerate(difficulties):
            rb = tk.Radiobutton(
                diff_frame,
                text=label,
                variable=self.difficulty_var,
                value=value,
                font=("Arial", 11),
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor=self.button_bg,
                activebackground=self.bg_color,
                activeforeground=self.accent_color,
                command=self.on_difficulty_change
            )
            rb.grid(row=0, column=i+1, padx=5)
        
        # Player selection
        player_frame = tk.Frame(self.root, bg=self.bg_color)
        player_frame.pack(pady=10)
        
        tk.Label(
            player_frame,
            text="You are:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).grid(row=0, column=0, padx=5)
        
        self.player_var = tk.StringVar(value="X")
        for i, symbol in enumerate(["X", "O"]):
            color = self.x_color if symbol == "X" else self.o_color
            rb = tk.Radiobutton(
                player_frame,
                text=symbol,
                variable=self.player_var,
                value=symbol,
                font=("Arial", 14, "bold"),
                bg=self.bg_color,
                fg=color,
                selectcolor=self.button_bg,
                activebackground=self.bg_color,
                activeforeground=color,
                command=self.start_new_game
            )
            rb.grid(row=0, column=i+1, padx=10)
        
        # Game board
        self.board_frame = tk.Frame(self.root, bg=self.bg_color)
        self.board_frame.pack(pady=20)
        
        self.create_board()
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=10)
        
        button_style = {
            "font": ("Arial", 11, "bold"),
            "bg": self.button_bg,
            "fg": self.text_color,
            "activebackground": self.button_hover,
            "activeforeground": self.text_color,
            "bd": 0,
            "padx": 15,
            "pady": 8,
            "cursor": "hand2"
        }
        
        self.new_game_btn = tk.Button(
            control_frame,
            text="🔄 New Game",
            command=self.start_new_game,
            **button_style
        )
        self.new_game_btn.grid(row=0, column=0, padx=5)
        
        self.undo_btn = tk.Button(
            control_frame,
            text="↩ Undo",
            command=self.undo_move,
            state=tk.DISABLED,
            **button_style
        )
        self.undo_btn.grid(row=0, column=1, padx=5)
        
        self.stats_btn = tk.Button(
            control_frame,
            text="📊 Statistics",
            command=self.show_statistics,
            **button_style
        )
        self.stats_btn.grid(row=0, column=2, padx=5)
        
        # Start initial game
        self.start_new_game()
    
    def create_board(self):
        """Create the 3x3 game board."""
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Arial", 32, "bold"),
                width=4,
                height=2,
                bg=self.button_bg,
                fg=self.text_color,
                activebackground=self.button_hover,
                bd=2,
                relief=tk.RAISED,
                cursor="hand2",
                command=lambda pos=i: self.on_cell_click(pos)
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(btn)
    
    def on_difficulty_change(self):
        """Handle difficulty change."""
        if self.game_started:
            response = messagebox.askyesno(
                "New Game",
                "Changing difficulty will start a new game. Continue?"
            )
            if response:
                self.start_new_game()
    
    def start_new_game(self):
        """Start a new game with current settings."""
        # Reset game state
        self.game = TicTacToe()
        self.game.difficulty = self.difficulty_var.get()
        self.game.human = self.player_var.get()
        self.game.ai = 'O' if self.game.human == 'X' else 'X'
        self.game.current_player = 'X'
        
        # Clear board
        for i, btn in enumerate(self.buttons):
            btn.config(
                text="",
                state=tk.NORMAL,
                bg=self.button_bg,
                relief=tk.RAISED
            )
            self.game.board[i] = ' '
        
        self.game_started = True
        self.undo_btn.config(state=tk.DISABLED)
        
        # Update info
        diff_label = self.game.difficulty.capitalize()
        self.info_label.config(
            text=f"Playing as {self.game.human} vs AI ({diff_label})"
        )
        
        # If AI goes first
        if self.game.current_player == self.game.ai:
            self.status_label.config(text="AI is thinking...")
            self.root.after(500, self.make_ai_move)
        else:
            self.status_label.config(text="Your turn!")
    
    def on_cell_click(self, position: int):
        """Handle cell click event."""
        if not self.game_started or self.game.game_over:
            return
        
        if self.game.current_player != self.game.human:
            return
        
        if not self.game.is_valid_move(position):
            return
        
        # Make human move
        self.make_move(position, self.game.human)
        
        # Check if game ended
        if self.check_game_over():
            return
        
        # AI's turn
        self.status_label.config(text="AI is thinking...")
        self.disable_board()
        self.root.after(500, self.make_ai_move)
    
    def make_move(self, position: int, player: str):
        """Make a move on the board."""
        self.game.make_move(position, player)
        
        # Update button
        color = self.x_color if player == 'X' else self.o_color
        self.buttons[position].config(
            text=player,
            fg=color,
            state=tk.DISABLED,
            relief=tk.SUNKEN
        )
        
        # Update undo button
        if len(self.game.move_history) >= 2:
            self.undo_btn.config(state=tk.NORMAL)
    
    def make_ai_move(self):
        """Make AI move."""
        if self.game.game_over:
            return
        
        position = self.game.get_best_move()
        self.make_move(position, self.game.ai)
        
        self.enable_board()
        
        if not self.check_game_over():
            self.status_label.config(text="Your turn!")
    
    def check_game_over(self) -> bool:
        """Check if game is over and handle end game."""
        game_state = self.game.evaluate_game_state()
        
        if game_state is None:
            return False
        
        self.game.game_over = True
        self.game.winner = game_state if game_state != 'TIE' else None
        self.disable_board()
        
        # Highlight winning combination
        if game_state != 'TIE':
            self.highlight_winner(game_state)
        
        # Record statistics
        is_human_winner = (self.game.winner == self.game.human)
        self.game.statistics.record_game(
            self.game.winner,
            is_human_winner,
            self.game.current_game_moves,
            self.game.difficulty
        )
        
        # Show result
        self.root.after(500, lambda: self.show_result(game_state))
        return True
    
    def highlight_winner(self, winner: str):
        """Highlight the winning combination."""
        for combo in self.game.winning_combinations:
            if all(self.game.board[pos] == winner for pos in combo):
                for pos in combo:
                    self.buttons[pos].config(bg="#28a745")
                break
    
    def show_result(self, game_state: str):
        """Show game result dialog."""
        if game_state == 'TIE':
            title = "It's a Tie!"
            message = "Well played! 🤝"
        elif game_state == self.game.human:
            title = "You Won!"
            if self.game.difficulty == 'hard':
                message = "🎉 AMAZING! You beat the unbeatable AI!"
            else:
                message = f"🎉 Congratulations! You won against {self.game.difficulty.capitalize()} AI!"
        else:
            title = "AI Won!"
            message = f"🤖 Better luck next time! Try again on {self.game.difficulty.capitalize()} mode."
        
        self.status_label.config(text=title)
        
        response = messagebox.askyesnocancel(
            title,
            f"{message}\n\nPlay again?",
            icon=messagebox.INFO
        )
        
        if response is True:
            self.start_new_game()
        elif response is None:
            self.show_statistics()
    
    def undo_move(self):
        """Undo the last move."""
        if len(self.game.move_history) < 2:
            messagebox.showwarning("Undo", "No moves to undo!")
            return
        
        # Undo AI move
        ai_pos, _ = self.game.move_history.pop()
        self.game.board[ai_pos] = ' '
        self.buttons[ai_pos].config(
            text="",
            state=tk.NORMAL,
            bg=self.button_bg,
            relief=tk.RAISED
        )
        
        # Undo human move
        human_pos, _ = self.game.move_history.pop()
        self.game.board[human_pos] = ' '
        self.buttons[human_pos].config(
            text="",
            state=tk.NORMAL,
            bg=self.button_bg,
            relief=tk.RAISED
        )
        
        self.game.current_game_moves -= 2
        
        # Disable undo if no more moves
        if len(self.game.move_history) < 2:
            self.undo_btn.config(state=tk.DISABLED)
        
        self.status_label.config(text="Move undone! Your turn.")
    
    def show_statistics(self):
        """Show game statistics in a dialog."""
        stats = self.game.statistics.stats
        
        stats_text = f"""
📊 GAME STATISTICS

Total Games: {stats['total_games']}
Your Wins: {stats['human_wins']}
AI Wins: {stats['ai_wins']}
Draws: {stats['draws']}
Win Rate: {self.game.statistics.get_win_rate():.1f}%
Avg Game Length: {self.game.statistics.get_average_moves():.1f} moves

DIFFICULTY BREAKDOWN:
"""
        for diff, data in stats['difficulty_stats'].items():
            if data['games'] > 0:
                win_rate = (data['wins'] / data['games']) * 100
                stats_text += f"\n{diff.capitalize()}: {data['games']} games, "
                stats_text += f"{data['wins']} wins ({win_rate:.1f}%)"
        
        messagebox.showinfo("Game Statistics", stats_text)
    
    def disable_board(self):
        """Disable all board buttons."""
        for btn in self.buttons:
            if btn['text'] == '':
                btn.config(state=tk.DISABLED)
    
    def enable_board(self):
        """Enable empty board buttons."""
        for btn in self.buttons:
            if btn['text'] == '':
                btn.config(state=tk.NORMAL)


def main():
    """Entry point for GUI application."""
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
