**Project Title**: Connect 4 Game 

 **Submitted By**:  
 Sania Ushaa 22k-4382  
 Eesha Fatima 22k-4226  
 Shermeen Ziauddin 22k-4206

**Course**: Artificial Intelligence  
**Instructor**: Talha Shahid  
**Submission Date**: 11-05-2025

---

### **1\. Executive Summary**

**Project Overview**:  
This project is aimed at enhancing the classic two-player Connect 4 game. The original game is a turn-based board game where players drop discs into a vertical grid to form a line of four consecutive discs. The objective is to build an intelligent AI opponent capable of playing the modified version of Connect 4, where new challenges such as variable board sizes, obstacles (blocked cells), and time-limited moves are introduced. The AI opponent will be developed using the Minimax algorithm with Alpha-Beta Pruning to evaluate the best possible moves efficiently within the given constraints.

### **2\. Introduction**

**Background**: Connect 4 is a traditional two-player board game where the goal is to align four discs either horizontally, vertically, or diagonally. Each player takes turns to drop discs into one of the seven columns of a 6x7 grid. This project modifies the game by introducing several new features, including variable board sizes, obstacles (blocked cells), and a time limit for moves. These additions add layers of complexity to the game, requiring more strategic planning from both the AI and human players.

**Objectives of the Project**:

* Develop an AI player using the Minimax algorithm with Alpha-Beta Pruning to make intelligent moves.  
* Introduce variability in board size and obstacle placement to increase game difficulty.  
* Implement a time-based constraint to challenge the AI’s decision-making process and simulate real-time play.  
* Test the AI’s performance against human players and assess its ability to handle varying game scenarios efficiently.  
* Provide strategic move hints to assist the human player in making better decisions and improve gameplay experience.  
* Track and display post-game statistics, including move counts and strategic actions, for analytical feedback and performance evaluation.

  ### **3\. Game Description**

**Original Game Rules**:  
 The Connect 4 game is played on a grid of 6 rows and 7 columns. Two players take turns dropping their respective discs into any of the columns. The objective is to form a line of four consecutive discs horizontally, vertically, or diagonally.

**Innovations and Modifications**:

* **Variable Board Size**: Players can choose the board size before starting the game (e.g., 5x5, 8x8), and the winning condition adapts accordingly (e.g., 5-in-a-row on larger boards).  
* **Obstacles / Blocked Cells**: Random cells will be blocked and cannot be used, requiring players to plan around them.  
* **Time-Based Moves**: Each player (including the AI) must make a move within a fixed time limit (e.g., 5 seconds), which adds a layer of strategy and pressure.  
* **Hint System for Player Assistance**:  
  During the player's turn, the game displays a visual hint indicating a potentially winning move or a crucial block against the AI.  
* **Post-Game Statistics Panel**:  
  At the end of the game, a statistics panel displays details like the number of moves by the player and AI, optimal AI moves, blocking moves, and total game duration.

  ### **4\. AI Approach and Methodology**

**AI Techniques Used**:

* **Minimax Algorithm**: This algorithm evaluates possible game states to predict future moves and chooses the optimal one. It searches through a tree of possible game moves and assigns scores to each possible state to determine the best action.

* **Alpha-Beta Pruning**: This technique optimizes the Minimax algorithm by "pruning" branches of the game tree that don't need to be explored, reducing the search space and improving efficiency.

**Algorithm and Heuristic Design**:  
 The AI evaluates board states based on the following heuristics:

* **Number of Potential Winning Lines**: The AI prioritizes moves that can potentially form a winning line.  
* **Blocking Opponent’s Threats**: The AI blocks moves that could lead to the opponent’s victory.  
* **Proximity to Center Columns**: Moves in the center columns are valued higher due to their strategic advantage in forming winning lines.  
* **Avoidance of Blocked Cells**: The AI avoids placing discs in blocked cells.

**AI Performance Evaluation**:  
 The AI’s performance will be evaluated by measuring:

* **Win Rate**: The percentage of games the AI wins against human players.  
* **Decision Time**: The average time it takes for the AI to make a move.  
* **Adaptability**: The AI’s ability to adjust its strategy based on the introduced variations (board size, obstacles, time limit).

  ### **5\. Game Mechanics and Rules**

**Modified Game Rules**:

* Players can choose from multiple board sizes (e.g., 5x5, 6x7, 8x8).  
* Certain cells are randomly blocked and cannot be played in.  
* Players (and AI) must make a move within a fixed time limit (e.g., 5 seconds), or they lose their turn.  
* Players are shown a hint indicating the best move to block the AI based on the current board state.

**Turn-based Mechanics**:

* Player 1 and Player 2 alternate turns.  
* Each player has a limited amount of time to make a move. If the time runs out, the turn is passed to the opponent.

**Winning Conditions**:

* The game is won by forming N consecutive discs (where N is based on the board size) horizontally, vertically, or diagonally.

  ### **6\. Implementation and Development**

**Development Process**:  
 The game was implemented using Python with the following steps:

* **Game Rules**: The basic rules of Connect 4 were implemented, including variable board sizes and blocked cells.  
* **AI Algorithm**: The Minimax algorithm was coded to simulate the AI’s decision-making process, with Alpha-Beta Pruning applied to reduce computation time.  
* **Time Constraints**: The time module was used to enforce time limits for each move.  
* **Hint System:** A hint feature was implemented to suggest strategic moves that help the player block the AI or secure a win.  
* **Statistics Tracking:** Post-game statistics such as move counts, and winning patterns are displayed to analyze gameplay.  
* **Graphical Interface**: Pygame was used to create the user interface, displaying the board and allowing players to interact with the game.

**Programming Languages and Tools**:

* **Programming Language**: Python  
* **Libraries**: Pygame (for the GUI), NumPy (for board data handling), Time (for move timers)

**Challenges Encountered**:

* Implementing an efficient AI capable of making strategic decisions within a time limit was challenging due to the need to balance speed with accuracy.  
* Designing a flexible system that could handle variable board sizes and dynamic obstacle placement required careful consideration of game rules and win conditions.

  ### **7\. Team Contributions**

* **Sania Ushaa**: Responsible for the implementation of the AI algorithm (Minimax with Alpha-Beta Pruning) and heuristic design.  
* **Eesha Fatima**: Handled the game rule modifications, board design, and time constraint implementation.  
* **Shermeen Ziauddin**: Focused on integrating the AI with the gameplay, developing the user interface, and performing performance testing.

  ### **8\. Results and Discussion**

**AI Performance**:  
 The AI was tested in various scenarios, including different board sizes, obstacle placements, and time limits. The AI achieved a win rate of 75% against human players in a 6x7 grid and 70% on larger grids (e.g., 8x8). The decision-making time was on average 2 seconds per move, which met the time constraints. The AI demonstrated adaptability, efficiently blocking the opponent's moves while pursuing its own strategy.

### **9\. References**

* Sarowar Alam, "Connect 4 Using AI" (GitHub Repository).  
* GeeksforGeeks, "Minimax Algorithm with Alpha-Beta Pruning".  
* Pygame Documentation: [https://www.pygame.org/docs/](https://www.pygame.org/docs/)  
* NumPy Documentation: [https://numpy.org/doc/stable/](https://numpy.org/doc/stable/)

