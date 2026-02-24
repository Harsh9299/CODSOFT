"""
Flask Web Application for Tic-Tac-Toe AI
Author: AI Assistant
Date: February 19, 2026

RESTful API backend for the Tic-Tac-Toe AI game.
Provides endpoints for game state management and AI moves.
"""

from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import uuid
from typing import Dict, Optional
from tic_tac_toe_ai import TicTacToe, GameStatistics


app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production-2026'
CORS(app)  # Enable CORS for all routes

# Store active game sessions (in production, use Redis or database)
games: Dict[str, TicTacToe] = {}


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/api/game/new', methods=['POST'])
def new_game():
    """
    Create a new game session.
    
    Request body:
    {
        "difficulty": "easy" | "medium" | "hard",
        "player": "X" | "O"
    }
    
    Response:
    {
        "game_id": "unique-game-id",
        "difficulty": "hard",
        "human": "X",
        "ai": "O",
        "current_player": "X",
        "board": [" ", " ", ...],
        "ai_move": 4  // Only if AI goes first
    }
    """
    data = request.json
    difficulty = data.get('difficulty', 'hard')
    player = data.get('player', 'X')
    
    # Validate inputs
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({'error': 'Invalid difficulty'}), 400
    if player not in ['X', 'O']:
        return jsonify({'error': 'Invalid player'}), 400
    
    # Create new game
    game_id = str(uuid.uuid4())
    game = TicTacToe()
    game.difficulty = difficulty
    game.human = player
    game.ai = 'O' if player == 'X' else 'X'
    game.current_player = 'X'
    
    games[game_id] = game
    
    response = {
        'game_id': game_id,
        'difficulty': difficulty,
        'human': game.human,
        'ai': game.ai,
        'current_player': game.current_player,
        'board': game.board
    }
    
    # If AI goes first, make AI move
    if game.current_player == game.ai:
        position = game.get_best_move()
        game.make_move(position, game.ai)
        game.current_player = game.human
        response['ai_move'] = position
        response['board'] = game.board
        response['current_player'] = game.current_player
    
    return jsonify(response)


@app.route('/api/game/<game_id>/move', methods=['POST'])
def make_move(game_id: str):
    """
    Make a move in the game.
    
    Request body:
    {
        "position": 0-8
    }
    
    Response:
    {
        "success": true,
        "board": [" ", "X", ...],
        "current_player": "O",
        "game_over": false,
        "winner": null | "X" | "O" | "TIE",
        "ai_move": 4  // AI's response move
    }
    """
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    data = request.json
    position = data.get('position')
    
    # Validate position
    if position is None or not isinstance(position, int) or position < 0 or position > 8:
        return jsonify({'error': 'Invalid position'}), 400
    
    if not game.is_valid_move(position):
        return jsonify({'error': 'Invalid move'}), 400
    
    # Make human move
    game.make_move(position, game.human)
    game.current_player = game.ai
    
    # Check if game ended
    game_state = game.evaluate_game_state()
    if game_state is not None:
        game.game_over = True
        game.winner = game_state if game_state != 'TIE' else None
        
        # Record statistics
        is_human_winner = (game.winner == game.human)
        game.statistics.record_game(
            game.winner,
            is_human_winner,
            game.current_game_moves,
            game.difficulty
        )
        
        return jsonify({
            'success': True,
            'board': game.board,
            'current_player': game.current_player,
            'game_over': True,
            'winner': game_state
        })
    
    # AI's turn
    ai_position = game.get_best_move()
    game.make_move(ai_position, game.ai)
    game.current_player = game.human
    
    # Check if game ended after AI move
    game_state = game.evaluate_game_state()
    if game_state is not None:
        game.game_over = True
        game.winner = game_state if game_state != 'TIE' else None
        
        # Record statistics
        is_human_winner = (game.winner == game.human)
        game.statistics.record_game(
            game.winner,
            is_human_winner,
            game.current_game_moves,
            game.difficulty
        )
    
    return jsonify({
        'success': True,
        'board': game.board,
        'current_player': game.current_player,
        'game_over': game.game_over,
        'winner': game.winner,
        'ai_move': ai_position
    })


@app.route('/api/game/<game_id>/undo', methods=['POST'])
def undo_move(game_id: str):
    """
    Undo the last move(s).
    
    Response:
    {
        "success": true,
        "board": [" ", " ", ...],
        "current_player": "X"
    }
    """
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    if len(game.move_history) < 2:
        return jsonify({'error': 'No moves to undo'}), 400
    
    success = game.undo_last_move()
    
    if not success:
        return jsonify({'error': 'Cannot undo'}), 400
    
    return jsonify({
        'success': True,
        'board': game.board,
        'current_player': game.human
    })


@app.route('/api/game/<game_id>/state', methods=['GET'])
def get_game_state(game_id: str):
    """
    Get current game state.
    
    Response:
    {
        "board": [" ", "X", ...],
        "current_player": "X",
        "game_over": false,
        "winner": null,
        "difficulty": "hard",
        "move_count": 4
    }
    """
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    return jsonify({
        'board': game.board,
        'current_player': game.current_player,
        'game_over': game.game_over,
        'winner': game.winner,
        'difficulty': game.difficulty,
        'move_count': len(game.move_history)
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get overall game statistics.
    
    Response:
    {
        "total_games": 100,
        "human_wins": 30,
        "ai_wins": 50,
        "draws": 20,
        "win_rate": 30.0,
        "avg_moves": 6.5,
        "difficulty_stats": {...}
    }
    """
    stats_obj = GameStatistics()
    stats = stats_obj.stats
    
    return jsonify({
        'total_games': stats['total_games'],
        'human_wins': stats['human_wins'],
        'ai_wins': stats['ai_wins'],
        'draws': stats['draws'],
        'win_rate': stats_obj.get_win_rate(),
        'avg_moves': stats_obj.get_average_moves(),
        'difficulty_stats': stats['difficulty_stats']
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'active_games': len(games)
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # In production, use a proper WSGI server like Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
