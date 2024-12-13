# Checkers Reinforcement Learning Project Documentation

## `checkers_env.py`
### Core Methods
- `initialize_board()`: Creates 6x6 board with initial piece positions
- `valid_moves(player)`: Generates legal moves for given player
- `capture_piece(action)`: Removes captured pieces during jumps
- `game_winner(board)`: Determines game outcome
- `step(action, player)`: Executes game state transitions

## `LearningAgent.py` (Q-Learning)
### Key Components
- `choose_action()`: Epsilon-greedy action selection
- `evaluation()`: Reward calculation based on board state
- `q_learning_update()`: Updates Q-table using Q-learning algorithm
- `learning()`: Training method for agent

## `SARSALearningAgent.py`
### Distinct Features
- SARSA learning algorithm implementation
- Similar structure to Q-Learning agent
- On-policy learning approach

## `gui.py`
### Functionality
- Tkinter-based game interface
- Supports human vs computer and computer vs computer modes
- Handles game state visualization and interaction

## `deployment.py`
### Main Functions
- Dependency checking
- Model training initiation
- Game execution management

## `modelpersistance.py`
### Main Functions
- QTable Saving
- QTable Loading
- Listing all saved QTables

## `PerformanceTracker.py`
### Main Functions
- episode Tracking
- performance data saving
- performance data loading

## Key Reinforcement Learning Concepts
- Epsilon-greedy exploration
- Q-table based value estimation
- Reward shaping
- On-policy and off-policy learning