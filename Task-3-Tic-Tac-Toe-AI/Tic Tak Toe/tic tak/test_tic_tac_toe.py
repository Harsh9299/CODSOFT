"""
Unit Tests for Tic-Tac-Toe AI Game
Author: AI Assistant
Date: February 19, 2026

Comprehensive test suite covering:
- Game logic
- AI algorithms
- Move validation
- Statistics tracking
- Win detection
- Difficulty levels

Run with: pytest test_tic_tac_toe.py -v
"""

import pytest
import json
import os
from pathlib import Path
from tic_tac_toe_ai import TicTacToe, GameStatistics


class TestGameLogic:
    """Test basic game logic and mechanics."""
    
    def test_initialization(self):
        """Test game initializes with correct default state."""
        game = TicTacToe()
        assert len(game.board) == 9
        assert all(cell == ' ' for cell in game.board)
        assert game.current_player == 'X'
        assert game.game_over == False
        assert game.winner is None
    
    def test_valid_move(self):
        """Test making a valid move."""
        game = TicTacToe()
        game.human = 'X'
        result = game.make_move(0, 'X')
        assert result == True
        assert game.board[0] == 'X'
        assert len(game.move_history) == 1
    
    def test_invalid_move_occupied_cell(self):
        """Test that occupied cells cannot be overwritten."""
        game = TicTacToe()
        game.make_move(0, 'X')
        result = game.make_move(0, 'O')
        assert result == False
        assert game.board[0] == 'X'
    
    def test_invalid_move_out_of_bounds(self):
        """Test that out of bounds moves are rejected."""
        game = TicTacToe()
        assert game.is_valid_move(-1) == False
        assert game.is_valid_move(9) == False
        assert game.is_valid_move(100) == False
    
    def test_undo_move(self):
        """Test undo functionality."""
        game = TicTacToe()
        game.human = 'X'
        game.ai = 'O'
        
        game.make_move(0, 'X')
        game.make_move(1, 'O')
        
        success = game.undo_last_move()
        assert success == True
        assert game.board[0] == ' '
        assert game.board[1] == ' '
        assert len(game.move_history) == 0
    
    def test_undo_insufficient_moves(self):
        """Test undo with insufficient moves."""
        game = TicTacToe()
        game.make_move(0, 'X', track_history=True)
        success = game.undo_last_move()
        assert success == False  # Need at least 2 moves


class TestWinDetection:
    """Test win condition detection."""
    
    def test_horizontal_win_top(self):
        """Test detection of top row win."""
        game = TicTacToe()
        game.board = ['X', 'X', 'X',
                      ' ', 'O', ' ',
                      'O', ' ', ' ']
        assert game.check_winner('X') == True
        assert game.check_winner('O') == False
    
    def test_horizontal_win_middle(self):
        """Test detection of middle row win."""
        game = TicTacToe()
        game.board = ['O', ' ', 'X',
                      'X', 'X', 'X',
                      'O', ' ', ' ']
        assert game.check_winner('X') == True
    
    def test_vertical_win(self):
        """Test detection of column win."""
        game = TicTacToe()
        game.board = ['O', 'X', ' ',
                      'O', ' ', 'X',
                      'O', 'X', ' ']
        assert game.check_winner('O') == True
    
    def test_diagonal_win_main(self):
        """Test detection of main diagonal win."""
        game = TicTacToe()
        game.board = ['X', 'O', 'O',
                      ' ', 'X', ' ',
                      'O', ' ', 'X']
        assert game.check_winner('X') == True
    
    def test_diagonal_win_anti(self):
        """Test detection of anti-diagonal win."""
        game = TicTacToe()
        game.board = ['O', ' ', 'X',
                      ' ', 'X', 'O',
                      'X', 'O', ' ']
        assert game.check_winner('X') == True
    
    def test_no_winner(self):
        """Test when no winner exists."""
        game = TicTacToe()
        game.board = ['X', 'O', 'X',
                      'X', 'O', 'O',
                      'O', 'X', ' ']
        assert game.check_winner('X') == False
        assert game.check_winner('O') == False
    
    def test_tie_game(self):
        """Test tie game detection."""
        game = TicTacToe()
        game.board = ['X', 'O', 'X',
                      'X', 'O', 'O',
                      'O', 'X', 'X']
        assert game.is_board_full() == True
        assert game.evaluate_game_state() == 'TIE'


class TestAILogic:
    """Test AI decision making and algorithms."""
    
    def test_ai_blocks_winning_move(self):
        """Test that AI blocks opponent's winning move."""
        game = TicTacToe()
        game.human = 'X'
        game.ai = 'O'
        game.difficulty = 'hard'
        
        # X about to win in row
        game.board = ['X', 'X', ' ',
                      'O', ' ', ' ',
                      ' ', ' ', ' ']
        
        best_move = game.get_best_move()
        assert best_move == 2  # AI should block at position 2
    
    def test_ai_takes_winning_move(self):
        """Test that AI takes winning move when available."""
        game = TicTacToe()
        game.human = 'X'
        game.ai = 'O'
        game.difficulty = 'hard'
        
        # O about to win
        game.board = ['O', 'O', ' ',
                      'X', 'X', ' ',
                      ' ', ' ', ' ']
        
        best_move = game.get_best_move()
        assert best_move == 2  # AI should win at position 2
    
    def test_ai_center_strategy(self):
        """Test that AI prefers center when available."""
        game = TicTacToe()
        game.human = 'X'
        game.ai = 'O'
        game.difficulty = 'hard'
        
        # Empty board except one corner
        game.board = ['X', ' ', ' ',
                      ' ', ' ', ' ',
                      ' ', ' ', ' ']
        
        best_move = game.get_best_move()
        assert best_move == 4  # Center is optimal
    
    def test_difficulty_easy_randomness(self):
        """Test that easy AI makes some random moves."""
        game = TicTacToe()
        game.human = 'X'
        game.ai = 'O'
        game.difficulty = 'easy'
        
        game.board = ['X', ' ', ' ',
                      ' ', ' ', ' ',
                      ' ', ' ', ' ']
        
        moves = set()
        # Run multiple times to check for randomness
        for _ in range(10):
            game_copy = TicTacToe()
            game_copy.board = game.board.copy()
            game_copy.ai = 'O'
            game_copy.difficulty = 'easy'
            moves.add(game_copy.get_best_move())
        
        # Easy mode should produce varied moves
        assert len(moves) > 1
    
    def test_minimax_depth_scoring(self):
        """Test that AI prefers faster wins."""
        game = TicTacToe()
        game.human = 'X'
        game.ai = 'O'
        game.difficulty = 'hard'
        
        # O can win immediately at 2 or in future
        game.board = ['O', 'O', ' ',
                      'X', ' ', ' ',
                      'X', ' ', ' ']
        
        best_move = game.get_best_move()
        assert best_move == 2  # Should take immediate win


class TestGameStatistics:
    """Test statistics tracking and persistence."""
    
    @pytest.fixture
    def temp_stats_file(self, tmp_path):
        """Create temporary stats file."""
        stats_file = tmp_path / "test_stats.json"
        return str(stats_file)
    
    def test_statistics_initialization(self, temp_stats_file):
        """Test statistics initialization."""
        stats = GameStatistics(temp_stats_file)
        assert stats.stats['total_games'] == 0
        assert stats.stats['human_wins'] == 0
        assert stats.stats['ai_wins'] == 0
        assert stats.stats['draws'] == 0
    
    def test_record_human_win(self, temp_stats_file):
        """Test recording a human win."""
        stats = GameStatistics(temp_stats_file)
        stats.record_game('X', True, 5, 'hard')
        
        assert stats.stats['total_games'] == 1
        assert stats.stats['human_wins'] == 1
        assert stats.stats['ai_wins'] == 0
        assert stats.stats['total_moves'] == 5
    
    def test_record_ai_win(self, temp_stats_file):
        """Test recording an AI win."""
        stats = GameStatistics(temp_stats_file)
        stats.record_game('O', False, 7, 'medium')
        
        assert stats.stats['total_games'] == 1
        assert stats.stats['ai_wins'] == 1
        assert stats.stats['human_wins'] == 0
    
    def test_record_draw(self, temp_stats_file):
        """Test recording a draw."""
        stats = GameStatistics(temp_stats_file)
        stats.record_game(None, False, 9, 'easy')
        
        assert stats.stats['total_games'] == 1
        assert stats.stats['draws'] == 1
    
    def test_win_rate_calculation(self, temp_stats_file):
        """Test win rate calculation."""
        stats = GameStatistics(temp_stats_file)
        stats.record_game('X', True, 5, 'hard')
        stats.record_game('O', False, 7, 'hard')
        stats.record_game('X', True, 6, 'medium')
        
        win_rate = stats.get_win_rate()
        assert win_rate == pytest.approx(66.666, rel=0.01)
    
    def test_average_moves_calculation(self, temp_stats_file):
        """Test average moves calculation."""
        stats = GameStatistics(temp_stats_file)
        stats.record_game('X', True, 5, 'hard')
        stats.record_game('O', False, 7, 'hard')
        stats.record_game(None, False, 9, 'easy')
        
        avg_moves = stats.get_average_moves()
        assert avg_moves == 7.0  # (5 + 7 + 9) / 3
    
    def test_statistics_persistence(self, temp_stats_file):
        """Test that statistics persist across sessions."""
        stats1 = GameStatistics(temp_stats_file)
        stats1.record_game('X', True, 5, 'hard')
        stats1.save_stats()
        
        # Create new instance (simulating new session)
        stats2 = GameStatistics(temp_stats_file)
        assert stats2.stats['total_games'] == 1
        assert stats2.stats['human_wins'] == 1


class TestDifficultyLevels:
    """Test different difficulty levels."""
    
    def test_hard_mode_unbeatable(self):
        """Test that hard mode AI cannot lose from start."""
        game = TicTacToe()
        game.human = 'X'
        game.ai = 'O'
        game.difficulty = 'hard'
        game.current_player = 'X'
        
        # Simulate a full game with AI playing optimally
        # Human plays corners, AI should not lose
        human_moves = [0, 2, 6]  # Corners
        move_idx = 0
        
        while not game.game_over and move_idx < len(human_moves):
            # Human move
            if game.current_player == game.human:
                pos = human_moves[move_idx]
                if game.is_valid_move(pos):
                    game.make_move(pos, game.human, track_history=False)
                    move_idx += 1
                else:
                    # Try next empty cell
                    for i in range(9):
                        if game.is_valid_move(i):
                            game.make_move(i, game.human, track_history=False)
                            break
            else:
                # AI move
                pos = game.get_best_move()
                game.make_move(pos, game.ai, track_history=False)
            
            # Check game state
            state = game.evaluate_game_state()
            if state:
                game.game_over = True
                game.winner = state if state != 'TIE' else None
                break
            
            # Switch player
            game.current_player = game.ai if game.current_player == game.human else game.human
        
        # AI should never lose
        assert game.winner != game.human
    
    def test_difficulty_assignment(self):
        """Test difficulty levels are correctly assigned."""
        game = TicTacToe()
        
        game.difficulty = 'easy'
        assert game.difficulty == 'easy'
        
        game.difficulty = 'medium'
        assert game.difficulty == 'medium'
        
        game.difficulty = 'hard'
        assert game.difficulty == 'hard'


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_cells_calculation(self):
        """Test getting empty cells."""
        game = TicTacToe()
        game.board = ['X', ' ', 'O',
                      ' ', 'X', ' ',
                      'O', ' ', ' ']
        
        empty = game.get_empty_cells()
        assert empty == [1, 3, 5, 7, 8]
    
    def test_full_board_detection(self):
        """Test full board detection."""
        game = TicTacToe()
        assert game.is_board_full() == False
        
        game.board = ['X'] * 9
        assert game.is_board_full() == True
    
    def test_move_history_tracking(self):
        """Test that move history is correctly tracked."""
        game = TicTacToe()
        game.make_move(0, 'X', track_history=True)
        game.make_move(1, 'O', track_history=True)
        game.make_move(2, 'X', track_history=True)
        
        assert len(game.move_history) == 3
        assert game.move_history[0] == (0, 'X')
        assert game.move_history[1] == (1, 'O')
        assert game.move_history[2] == (2, 'X')
    
    def test_reset_game(self):
        """Test game reset functionality."""
        game = TicTacToe()
        game.make_move(0, 'X')
        game.make_move(1, 'O')
        game.game_over = True
        game.winner = 'X'
        
        game.reset_game()
        
        assert all(cell == ' ' for cell in game.board)
        assert game.game_over == False
        assert game.winner is None
        assert len(game.move_history) == 0
        assert game.current_game_moves == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
