from flask import Flask, request, jsonify
from gamecode.minmax import MinimaxAI
from gamecode.game_logic import ConnectFourGame

# App
app = Flask(__name__)

# Initialize global game state
game = None
ai = MinimaxAI()

# Welcome
@app.route("/", methods=["GET"])
def hello():
    return "Welcome to the game backend"

# Game init
@app.route('/init_game', methods=['POST'])
def init_game():
    global game
    game = ConnectFourGame()
    return jsonify(game.board)

# Player move
@app.route('/player_move', methods=['POST'])
def player_move():
    global game
    data = request.get_json()
    column = data['column']
    if game.make_move(column, player=1):
        return jsonify(game.board)
    else:
        return jsonify({"error": "Invalid move"}), 400

# AI move
@app.route('/ai_move', methods=['POST'])
def ai_move():
    global game
    ai_column, move_scores = ai.find_best_move(game.board)
    game.make_move(ai_column, player=2)
    return jsonify({
        "board": game.board,
        "scores": move_scores
    })

# Check winner
@app.route('/check_game_status_winner', methods=['GET'])
def check_game_status_winner():
    global game
    return jsonify(status=game.check_win())


# Check draw
@app.route('/check_game_status_draw', methods=['GET'])
def check_game_status_draw():
    global game
    return jsonify(status=game.check_draw())

# Run
if __name__ == '__main__':
    app.run(debug=True) # Port 5000