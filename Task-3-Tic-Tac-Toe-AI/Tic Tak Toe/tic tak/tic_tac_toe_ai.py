"""
Production-Ready Tic-Tac-Toe AI with Minimax Algorithm and Alpha-Beta Pruning
Author: AI Assistant
Date: February 19, 2026

This implementation features:
- Object-Oriented Programming design
- Unbeatable AI using Minimax algorithm with Alpha-Beta Pruning
- Depth-based scoring for optimal move selection
- Multiple difficulty levels (Easy/Medium/Hard)
- Move history and undo functionality
- Game statistics tracking
- Clean separation between game logic and AI logic
- User-friendly terminal interface
"""

import sys
import random
import json
from typing import List, Tuple, Optional, Dict
from datetime import datetime
from pathlib import Path


class GameStatistics:
    """
    Track and persist game statistics across sessions.
    
    Stores:
    - Total games played
    - Wins/losses/draws
    - Win rate
    - Average game length
    """
    
    def __init__(self, stats_file: str = "game_stats.json"):
        """Initialize statistics with persistence."""
        self.stats_file = Path(stats_file)
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """Load statistics from file or create new."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'total_games': 0,
            'human_wins': 0,
            'ai_wins': 0,
            'draws': 0,
            'total_moves': 0,
            'difficulty_stats': {
                'easy': {'games': 0, 'wins': 0},
                'medium': {'games': 0, 'wins': 0},
                'hard': {'games': 0, 'wins': 0}
            }
        }
    
    def save_stats(self) -> None:
        """Persist statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save statistics: {e}")
    
    def record_game(self, winner: Optional[str], is_human_winner: bool, 
                   moves: int, difficulty: str) -> None:
        """Record game result."""
        self.stats['total_games'] += 1
        self.stats['total_moves'] += moves
        
        if winner is None:
            self.stats['draws'] += 1
        elif is_human_winner:
            self.stats['human_wins'] += 1
            self.stats['difficulty_stats'][difficulty]['wins'] += 1
        else:
            self.stats['ai_wins'] += 1
        
        self.stats['difficulty_stats'][difficulty]['games'] += 1
        self.save_stats()
    
    def get_win_rate(self) -> float:
        """Calculate human win rate."""
        total = self.stats['total_games']
        if total == 0:
            return 0.0
        return (self.stats['human_wins'] / total) * 100
    
    def get_average_moves(self) -> float:
        """Calculate average game length."""
        total = self.stats['total_games']
        if total == 0:
            return 0.0
        return self.stats['total_moves'] / total
    
    def display_stats(self) -> None:
        """Display formatted statistics."""
        print("\n" + "=" * 50)
        print("📊 GAME STATISTICS")
        print("=" * 50)
        print(f"Total Games Played: {self.stats['total_games']}")
        print(f"Human Wins: {self.stats['human_wins']}")
        print(f"AI Wins: {self.stats['ai_wins']}")
        print(f"Draws: {self.stats['draws']}")
        print(f"Win Rate: {self.get_win_rate():.1f}%")
        print(f"Average Game Length: {self.get_average_moves():.1f} moves")
        
        print("\nDifficulty Breakdown:")
        for diff, data in self.stats['difficulty_stats'].items():
            if data['games'] > 0:
                win_rate = (data['wins'] / data['games']) * 100
                print(f"  {diff.capitalize()}: {data['games']} games, "
                      f"{data['wins']} wins ({win_rate:.1f}%)")
        print("=" * 50)


class TicTacToe:
    """
    Main Tic-Tac-Toe game class handling game logic, AI, and user interface.
    
    This class encapsulates:
    - Game state management (board, current player, game status)
    - AI decision-making using Minimax with Alpha-Beta Pruning
    - User interface and input validation
    """
    
    def __init__(self):
        """Initialize the game with an empty board and default settings."""
        # Board representation: List of 9 cells (0-8), empty cells marked with space
        self.board: List[str] = [' ' for _ in range(9)]
        
        # Player symbols
        self.human: str = ''      # Will be set by user choice (X or O)
        self.ai: str = ''         # Opposite of human choice
        self.current_player: str = 'X'  # X always starts first
        
        # Game status
        self.game_over: bool = False
        self.winner: Optional[str] = None
        
        # Difficulty settings ('easy', 'medium', 'hard')
        self.difficulty: str = 'hard'
        
        # Move history for undo functionality
        self.move_history: List[Tuple[int, str]] = []  # [(position, player), ...]
        
        # Statistics tracking
        self.statistics = GameStatistics()
        self.current_game_moves: int = 0
        
        # Winning combinations (indices on the board)
        self.winning_combinations: List[List[int]] = [
            [0, 1, 2],  # Top row
            [3, 4, 5],  # Middle row
            [6, 7, 8],  # Bottom row
            [0, 3, 6],  # Left column
            [1, 4, 7],  # Middle column
            [2, 5, 8],  # Right column
            [0, 4, 8],  # Diagonal top-left to bottom-right
            [2, 4, 6]   # Diagonal top-right to bottom-left
        ]
    
    # ==================== GAME LOGIC METHODS ====================
    
    def display_board(self) -> None:
        """
        Display the current game board in a clean, formatted manner.
        Shows position numbers for empty cells to guide the user.
        """
        print("\n" + "=" * 40)
        print("          TIC-TAC-TOE GAME")
        print("=" * 40)
        print()
        
        # Display the board with proper formatting
        for i in range(0, 9, 3):
            row = []
            for j in range(i, i + 3):
                if self.board[j] == ' ':
                    # Show position number for empty cells
                    row.append(f" {j+1} ")
                else:
                    # Show player symbol (X or O)
                    row.append(f" {self.board[j]} ")
            print("  " + "|".join(row))
            if i < 6:
                print("  " + "-" * 11)
        
        print("\n" + "=" * 40)
    
    def is_valid_move(self, position: int) -> bool:
        """
        Validate if a move is legal.
        
        Args:
            position: Board position (0-8)
        
        Returns:
            True if the position is empty and within bounds, False otherwise
        """
        return 0 <= position < 9 and self.board[position] == ' '
    
    def make_move(self, position: int, player: str, track_history: bool = True) -> bool:
        """
        Place a player's symbol on the board.
        
        Args:
            position: Board position (0-8)
            player: Player symbol ('X' or 'O')
            track_history: Whether to record this move in history (for undo)
        
        Returns:
            True if move was successful, False otherwise
        """
        if self.is_valid_move(position):
            self.board[position] = player
            if track_history:
                self.move_history.append((position, player))
                self.current_game_moves += 1
            return True
        return False
    
    def undo_move(self, position: int) -> None:
        """
        Remove a symbol from the board (used in minimax simulation).
        
        Args:
            position: Board position to clear (0-8)
        """
        self.board[position] = ' '
    
    def undo_last_move(self) -> bool:
        """
        Undo the last move(s) made (human and AI).
        Allows player to take back their last move.
        
        Returns:
            True if undo was successful, False if no moves to undo
        """
        if len(self.move_history) < 2:  # Need at least 2 moves (human + AI)
            return False
        
        # Undo AI's last move
        ai_position, ai_player = self.move_history.pop()
        self.board[ai_position] = ' '
        
        # Undo human's last move
        human_position, human_player = self.move_history.pop()
        self.board[human_position] = ' '
        
        self.current_game_moves -= 2
        return True
    
    def check_winner(self, player: str) -> bool:
        """
        Check if a specific player has won the game.
        
        Args:
            player: Player symbol to check ('X' or 'O')
        
        Returns:
            True if the player has a winning combination, False otherwise
        
        Time Complexity: O(1) - Fixed number of combinations to check (8)
        """
        for combo in self.winning_combinations:
            if all(self.board[pos] == player for pos in combo):
                return True
        return False
    
    def is_board_full(self) -> bool:
        """
        Check if the board is completely filled.
        
        Returns:
            True if no empty cells remain, False otherwise
        
        Time Complexity: O(1) - Checking 9 cells
        """
        return ' ' not in self.board
    
    def get_empty_cells(self) -> List[int]:
        """
        Get all available positions on the board.
        
        Returns:
            List of indices representing empty cells
        
        Time Complexity: O(n) where n = 9 (board size)
        """
        return [i for i in range(9) if self.board[i] == ' ']
    
    def evaluate_game_state(self) -> Optional[str]:
        """
        Evaluate the current game state.
        
        Returns:
            'X' if X wins, 'O' if O wins, 'TIE' if draw, None if game continues
        """
        if self.check_winner('X'):
            return 'X'
        elif self.check_winner('O'):
            return 'O'
        elif self.is_board_full():
            return 'TIE'
        return None
    
    # ==================== AI LOGIC METHODS ====================
    
    def minimax(self, depth: int, is_maximizing: bool, alpha: float, beta: float) -> int:
        """
        Minimax algorithm with Alpha-Beta Pruning for optimal AI decision-making.
        
        MINIMAX ALGORITHM EXPLANATION:
        -------------------------------
        Minimax is a recursive algorithm used in decision-making and game theory.
        It explores all possible future game states to find the optimal move.
        
        - Maximizing player (AI): Tries to maximize the score
        - Minimizing player (Human): Tries to minimize the score
        
        The algorithm assumes both players play optimally.
        
        ALPHA-BETA PRUNING OPTIMIZATION:
        --------------------------------
        Alpha-Beta pruning eliminates branches that cannot affect the final decision,
        significantly reducing the number of nodes evaluated in the game tree.
        
        - Alpha: Best value that the maximizer can guarantee (starts at -∞)
        - Beta: Best value that the minimizer can guarantee (starts at +∞)
        
        Pruning occurs when:
        - In a max node: if beta <= alpha, prune remaining branches
        - In a min node: if beta <= alpha, prune remaining branches
        
        DEPTH-BASED SCORING:
        -------------------
        We subtract/add depth to prefer winning faster and losing slower:
        - AI win: +10 - depth (prefer winning in fewer moves)
        - Human win: -10 + depth (prefer losing in more moves)
        
        TIME COMPLEXITY:
        ---------------
        Without pruning: O(b^d) where b = branching factor (~9), d = depth
        With Alpha-Beta pruning: O(b^(d/2)) in best case
        In practice, reduces ~50-90% of nodes in Tic-Tac-Toe
        
        Args:
            depth: Current depth in the game tree (0 at leaf nodes)
            is_maximizing: True if AI's turn (maximizing), False if human's turn (minimizing)
            alpha: Best value for maximizer so far
            beta: Best value for minimizer so far
        
        Returns:
            Score of the board state (-10 to +10 adjusted by depth)
        """
        # Base case: Check if game has ended (terminal node)
        game_state = self.evaluate_game_state()
        
        if game_state == self.ai:
            # AI wins: Return positive score minus depth (prefer faster wins)
            return 10 - depth
        elif game_state == self.human:
            # Human wins: Return negative score plus depth (prefer slower losses)
            return -10 + depth
        elif game_state == 'TIE':
            # Draw: Neutral score
            return 0
        
        # Recursive case: Game continues, evaluate all possible moves
        
        if is_maximizing:
            # AI's turn (Maximizing player): Find move that maximizes score
            max_eval = -float('inf')  # Start with worst possible score
            
            for cell in self.get_empty_cells():
                # Simulate making the move
                self.make_move(cell, self.ai)
                
                # Recursively evaluate the resulting position
                eval_score = self.minimax(depth + 1, False, alpha, beta)
                
                # Undo the simulated move
                self.undo_move(cell)
                
                # Update maximum evaluation
                max_eval = max(max_eval, eval_score)
                
                # Alpha-Beta Pruning: Update alpha
                alpha = max(alpha, eval_score)
                
                # Prune: If beta <= alpha, remaining branches won't affect decision
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        
        else:
            # Human's turn (Minimizing player): Find move that minimizes score
            min_eval = float('inf')  # Start with worst possible score
            
            for cell in self.get_empty_cells():
                # Simulate making the move
                self.make_move(cell, self.human)
                
                # Recursively evaluate the resulting position
                eval_score = self.minimax(depth + 1, True, alpha, beta)
                
                # Undo the simulated move
                self.undo_move(cell)
                
                # Update minimum evaluation
                min_eval = min(min_eval, eval_score)
                
                # Alpha-Beta Pruning: Update beta
                beta = min(beta, eval_score)
                
                # Prune: If beta <= alpha, remaining branches won't affect decision
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def get_best_move(self) -> int:
        """
        Find the optimal move for the AI based on difficulty level.
        
        Difficulty levels:
        - Easy: 30% optimal moves, 70% random
        - Medium: 70% optimal moves, 30% random
        - Hard: 100% optimal moves (unbeatable)
        
        Returns:
            Best position (0-8) for the AI to play
        
        Time Complexity: O(b^(d/2)) with pruning for hard mode
        """
        empty_cells = self.get_empty_cells()
        
        # Difficulty-based move selection
        if self.difficulty == 'easy':
            # 30% chance of optimal move, 70% random
            if random.random() < 0.3:
                return self._get_optimal_move()
            return random.choice(empty_cells)
        
        elif self.difficulty == 'medium':
            # 70% chance of optimal move, 30% random
            if random.random() < 0.7:
                return self._get_optimal_move()
            return random.choice(empty_cells)
        
        else:  # hard mode
            # Always play optimally
            return self._get_optimal_move()
    
    def _get_optimal_move(self) -> int:
        """
        Find the optimal move using Minimax with Alpha-Beta Pruning.
        
        Returns:
            Best position (0-8) for the AI to play
        
        Time Complexity: O(b^(d/2)) with pruning, where b = branching factor, d = depth
        """
        best_score = -float('inf')
        best_move = -1
        
        # Initialize alpha and beta for Alpha-Beta Pruning
        alpha = -float('inf')
        beta = float('inf')
        
        # Evaluate each possible move
        for cell in self.get_empty_cells():
            # Simulate making the move (don't track in history)
            self.make_move(cell, self.ai, track_history=False)
            
            # Calculate the score for this move
            # Start with depth 0 and minimizing (opponent's turn next)
            move_score = self.minimax(0, False, alpha, beta)
            
            # Undo the simulated move
            self.undo_move(cell)
            
            # Update best move if this move has a better score
            if move_score > best_score:
                best_score = move_score
                best_move = cell
            
            # Update alpha for pruning in subsequent iterations
            alpha = max(alpha, best_score)
        
        return best_move
    
    # ==================== USER INTERFACE METHODS ====================
    
    def get_difficulty_choice(self) -> str:
        """
        Let the user choose AI difficulty level.
        
        Returns:
            Difficulty level ('easy', 'medium', or 'hard')
        """
        print("\n" + "=" * 40)
        print("         SELECT DIFFICULTY LEVEL")
        print("=" * 40)
        print("1. Easy   - AI makes mistakes (30% optimal)")
        print("2. Medium - Balanced gameplay (70% optimal)")
        print("3. Hard   - Unbeatable AI (100% optimal)")
        print()
        
        while True:
            choice = input("Choose difficulty (1-3): ").strip()
            if choice == '1':
                return 'easy'
            elif choice == '2':
                return 'medium'
            elif choice == '3':
                return 'hard'
            print("Invalid choice! Please enter 1, 2, or 3.")
    
    def get_player_choice(self) -> str:
        """
        Let the user choose their symbol (X or O).
        
        Returns:
            User's chosen symbol ('X' or 'O')
        """
        print("\n" + "=" * 40)
        print("          WELCOME TO TIC-TAC-TOE!")
        print("=" * 40)
        print("\nYou're playing against an AI!")
        print("The AI uses Minimax with Alpha-Beta Pruning.")
        print()
        
        while True:
            choice = input("Choose your symbol (X/O): ").strip().upper()
            if choice in ['X', 'O']:
                return choice
            print("Invalid choice! Please enter X or O.")
    
    def get_human_move(self) -> int:
        """
        Get and validate the human player's move.
        Supports undo command.
        
        Returns:
            Valid board position (0-8) chosen by the human, or -1 for undo
        """
        while True:
            try:
                if len(self.move_history) >= 2:
                    move = input(f"\n{self.human}'s turn. Enter position (1-9) or 'u' to undo: ").strip().lower()
                else:
                    move = input(f"\n{self.human}'s turn. Enter position (1-9): ").strip()
                
                # Check for undo command
                if move == 'u' and len(self.move_history) >= 2:
                    return -1  # Signal to undo
                
                # Validate input is a number
                if not move.isdigit():
                    print("Invalid input! Please enter a number between 1 and 9.")
                    continue
                
                position = int(move) - 1  # Convert to 0-indexed
                
                # Validate move is within bounds
                if position < 0 or position > 8:
                    print("Invalid position! Please enter a number between 1 and 9.")
                    continue
                
                # Validate cell is empty
                if not self.is_valid_move(position):
                    print("That cell is already occupied! Choose another position.")
                    continue
                
                return position
            
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 9.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Exiting...")
                sys.exit(0)
    
    def display_game_result(self) -> None:
        """Display the final game result with appropriate message."""
        self.display_board()
        print()
        
        difficulty_label = self.difficulty.capitalize()
        
        if self.winner == self.human:
            if self.difficulty == 'hard':
                print("🎉 AMAZING! You won against the UNBEATABLE AI!")
            else:
                print(f"🎉 Congratulations! You won against {difficulty_label} AI!")
        elif self.winner == self.ai:
            print(f"🤖 AI wins! Try again on {difficulty_label} mode!")
        else:
            print("🤝 It's a tie! Well played!")
        
        # Record game statistics
        is_human_winner = (self.winner == self.human)
        self.statistics.record_game(self.winner, is_human_winner, 
                                   self.current_game_moves, self.difficulty)
        print()
    
    def ask_to_play_again(self) -> bool:
        """
        Ask the user if they want to play another game or view stats.
        
        Returns:
            True if user wants to play again, False otherwise
        """
        while True:
            choice = input("Options: (p)lay again, (s)tatistics, (q)uit: ").strip().lower()
            if choice in ['p', 'play']:
                return True
            elif choice in ['s', 'stats', 'statistics']:
                self.statistics.display_stats()
                continue
            elif choice in ['q', 'quit', 'no', 'n']:
                return False
            print("Invalid input! Please enter 'p', 's', or 'q'.")
    
    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.current_game_moves = 0
    
    # ==================== MAIN GAME LOOP ====================
    
    def play(self) -> None:
        """
        Main game loop orchestrating the entire game flow.
        
        This method handles:
        - Difficulty selection
        - Player symbol selection
        - Turn management
        - Move execution (human and AI)
        - Undo functionality
        - Game state checking
        - Statistics tracking
        - End game handling
        - Replay option
        """
        print("\n")
        print("╔" + "═" * 48 + "╗")
        print("║" + " " * 48 + "║")
        print("║" + "    🎮 TIC-TAC-TOE AI - PRO EDITION 🎮    ".center(48) + "║")
        print("║" + " " * 48 + "║")
        print("╚" + "═" * 48 + "╝")
        
        # Initial setup: Choose difficulty and player symbol
        self.difficulty = self.get_difficulty_choice()
        self.human = self.get_player_choice()
        self.ai = 'O' if self.human == 'X' else 'X'
        
        difficulty_label = self.difficulty.capitalize()
        print(f"\nGreat! You are '{self.human}' and AI is '{self.ai}'.")
        print(f"Difficulty: {difficulty_label}")
        print(f"'{self.current_player}' goes first.")
        input("\nPress Enter to start the game...")
        
        # Main game loop - continues until player quits
        while True:
            # Game round loop - continues until game ends
            while not self.game_over:
                # Display current board state
                self.display_board()
                
                # Show move history count
                if len(self.move_history) > 0:
                    print(f"Moves made: {len(self.move_history)}")
                
                # Check if game has ended before accepting input
                game_state = self.evaluate_game_state()
                if game_state is not None:
                    self.game_over = True
                    self.winner = game_state if game_state != 'TIE' else None
                    break
                
                # Execute turn based on current player
                if self.current_player == self.human:
                    # Human's turn
                    position = self.get_human_move()
                    
                    # Handle undo request
                    if position == -1:
                        if self.undo_last_move():
                            print("\n✓ Last move undone!")
                            # Stay on human's turn since we undid both moves
                            continue
                        else:
                            print("\nNo moves to undo!")
                            continue
                    
                    self.make_move(position, self.human)
                    print(f"\nYou placed '{self.human}' at position {position + 1}.")
                else:
                    # AI's turn
                    print(f"\n🤖 AI ({self.difficulty}) is thinking...")
                    position = self.get_best_move()
                    self.make_move(position, self.ai)
                    print(f"AI placed '{self.ai}' at position {position + 1}.")
                    input("\nPress Enter to continue...")
                
                # Switch to next player
                self.current_player = self.ai if self.current_player == self.human else self.human
            
            # Game has ended - display result
            self.display_game_result()
            
            # Ask if player wants to play again
            if self.ask_to_play_again():
                self.reset_game()
                print("\nStarting new game...")
                # Continue to outer loop for another game
            else:
                # Show final statistics before exiting
                self.statistics.display_stats()
                print("\nThanks for playing! Goodbye! 👋")
                break


# ==================== ENTRY POINT ====================

def main():
    """Entry point for the Tic-Tac-Toe game."""
    try:
        game = TicTacToe()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
