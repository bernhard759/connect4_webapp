# Connect Four AI Game

This project is a web-based implementation of the classic Connect Four game, featuring an AI opponent powered by the Minimax algorithm. The project consists of a Flask-based backend that handles the game logic and AI, and a Svelte-powered frontend that provides a responsive and interactive user interface.

## Features

- **Connect Four Game**: A fully functional Connect Four game with an intuitive drag-and-drop interface.
- **AI Opponent**: An AI opponent that uses the Minimax algorithm with a simple heuristic to play against the user.
- **Svelte Frontend**: A modern, responsive frontend built with Svelte and Sveltestrap for a clean user experience.
- **Flask Backend**: A Flask server exposing RESTful endpoints for game state management and AI decision-making.

### Backend

- **Flask Server (`app.py`)**: This file contains the main Flask application, defining routes for initializing the game, handling player moves, making AI moves, and checking the game status (win/draw).
- **Game Logic (`game_logic.py`)**: Implements the core game mechanics, including move validation, win condition checks, and board evaluation.
- **Minimax AI (`minimax_ai.py`)**: Contains the Minimax algorithm implementation that the AI uses to decide its moves.
- **Configuration (`config.py`)**: Holds constants such as player IDs and the scoring matrix that influences the AI's decisions.

### Frontend

- **Svelte Application (`App.svelte`, `Game.svelte`)**: Provides the user interface for playing the game. Includes drag-and-drop functionality for placing tokens and dynamic updates based on the game state.
- **Sveltestrap Components**: Utilizes Bootstrap-styled components for layout and controls, ensuring a clean and responsive design.
- **Custom Styles (`gamestyle.css`)**: Custom CSS to style the game board, tokens, and other UI elements.

## Installation

### Prerequisites

- **Python 3**: Ensure Python 3 is installed on your system.
- **Node.js and npm**: Required for building and running the Svelte frontend.

### Backend Setup

1. **Clone the repository**:

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Install the dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   - Visit `http://localhost:5000` to interact with the game.

## Usage

- **Start a New Game**: Click the "Reset Game" button to start a new game.
- **Play Your Move**: Drag a token and drop it into a column on the board.
- **AI Move**: The AI will automatically make its move after yours.
- **Win/Draw Detection**: The game will notify you if there is a winner or if the game ends in a draw.