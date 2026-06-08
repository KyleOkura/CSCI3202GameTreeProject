"""
Flask app for Mancala Solver - Web deployment version
To run: python app.py
Then visit: http://localhost:5000
"""

from flask import Flask, render_template, jsonify, request, session
import json
from mancala import Mancala
from alphabeta import alphabeta
from minimax import minimax
import uuid

app = Flask(__name__)
app.secret_key = 'mancala_solver_secret_key_change_in_production'

# Store game sessions
games = {}


def create_game(algorithm='alphabeta', depth=5):
    """Create a new game session"""
    game_id = str(uuid.uuid4())
    games[game_id] = {
        'game': Mancala(pits_per_player=6, stones_per_pit=4),
        'algorithm': algorithm,
        'depth': depth,
        'moves_log': [],
        'game_over': False
    }
    return game_id


def serialize_game(game_obj):
    """Convert game object to JSON serializable format"""
    return {
        'board': game_obj.board,
        'current_player': game_obj.current_player,
        'p1_mancala': game_obj.board[game_obj.p1_mancala_index],
        'p2_mancala': game_obj.board[game_obj.p2_mancala_index],
        'valid_moves': game_obj.possible_moves() if not game_obj.winning_eval() else [],
        'game_over': game_obj.winning_eval()
    }


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Create a new game"""
    data = request.get_json()
    algorithm = data.get('algorithm', 'alphabeta')
    depth = data.get('depth', 5)
    
    game_id = create_game(algorithm, depth)
    game_data = games[game_id]
    
    return jsonify({
        'game_id': game_id,
        'game': serialize_game(game_data['game']),
        'message': 'New game created. You are Player 1.'
    })


@app.route('/api/game/<game_id>', methods=['GET'])
def get_game(game_id):
    """Get current game state"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game_data = games[game_id]
    response = {
        'game': serialize_game(game_data['game']),
        'moves_log': game_data['moves_log'],
        'algorithm': game_data['algorithm'],
        'depth': game_data['depth']
    }
    
    opponent_name = 'Random' if game_data['algorithm'] == 'random' else 'AI'

    # Check for winner
    if game_data['game'].winning_eval():
        p1_score = game_data['game'].board[game_data['game'].p1_mancala_index]
        p2_score = game_data['game'].board[game_data['game'].p2_mancala_index]
        
        if p1_score > p2_score:
            response['winner'] = 'player1'
            response['message'] = f'You won {p1_score} to {p2_score}!'
        elif p2_score > p1_score:
            response['winner'] = 'player2'
            response['message'] = f'{opponent_name} won {p2_score} to {p1_score}. Try again!'
        else:
            response['winner'] = 'tie'
            response['message'] = f"It's a tie {p1_score} to {p2_score}!"
        
        game_data['game_over'] = True
    
    return jsonify(response)


@app.route('/api/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    """Make a move in the game"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.get_json()
    pit = data.get('pit')
    
    game_data = games[game_id]
    game_obj = game_data['game']
    
    # Validate move
    if not game_obj.valid_move(pit):
        return jsonify({'error': f'Invalid move: pit {pit} is empty or invalid'}), 400
    
    if game_obj.winning_eval():
        return jsonify({'error': 'Game is already over'}), 400
    
    if game_obj.current_player != 1:
        return jsonify({'error': 'Not your turn'}), 400
    
    # Make player move
    game_obj.play(pit)
    game_data['moves_log'].append({
        'player': 'User',
        'pit': pit,
        'board': list(game_obj.board),
        'current_player': game_obj.current_player
    })
    
    # Check for game over
    if game_obj.winning_eval():
        return jsonify({
            'game': serialize_game(game_obj),
            'moves_log': game_data['moves_log'],
            'message': 'Game over! Your turn ended the game.',
            'ai_move': None
        })
    
    # AI makes a move
    if game_obj.current_player == 2:
        try:
            opponent_name = 'Random' if game_data['algorithm'] == 'random' else 'AI'

            if game_data['algorithm'] == 'alphabeta':
                ai_move = alphabeta(game_obj, game_data['depth'], player=2)
            elif game_data['algorithm'] == 'minimax':
                ai_move = minimax(game_obj, game_data['depth'], player=2)
            else:  # random
                ai_move = game_obj.random_move_generator()
            
            ai_move = int(ai_move)
            game_obj.play(ai_move)
            
            game_data['moves_log'].append({
                'player': opponent_name,
                'pit': ai_move,
                'board': list(game_obj.board),
                'current_player': game_obj.current_player
            })
            
            ai_response = {
                'game': serialize_game(game_obj),
                'moves_log': game_data['moves_log'],
                'ai_move': ai_move,
                'message': f'{opponent_name} played pit {ai_move}'
            }
            
            # Check for game over after AI move
            if game_obj.winning_eval():
                ai_response['message'] += '. Game over!'
            
            return jsonify(ai_response)
        
        except Exception as e:
            return jsonify({'error': f'AI error: {str(e)}'}), 500
    
    return jsonify({
        'game': serialize_game(game_obj),
        'moves_log': game_data['moves_log'],
        'ai_move': None,
        'message': 'Move made successfully'
    })


@app.route('/api/game/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    """Reset the game"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game_data = games[game_id]
    algorithm = game_data['algorithm']
    depth = game_data['depth']
    
    game_data['game'] = Mancala(pits_per_player=6, stones_per_pit=4)
    game_data['moves_log'] = []
    game_data['game_over'] = False
    
    return jsonify({
        'game': serialize_game(game_data['game']),
        'message': 'Game reset. Make your first move!'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
