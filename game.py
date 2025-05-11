import numpy as np 
import pygame
import sys
import math
import random
import time



# Color Definitions
Dark_Magenta = (25, 25, 112)     # Board
Turquoise = (211, 211, 211)       # Empty Slots
Deep_Pink =  (65, 105, 225)      # Player Piece
Lime_Green = (220, 20, 60)     # AI Piece
WHITE = (255, 255, 255)  
GRAY =  (105, 105, 105)    # Obstacle Cell
DARK_GREEN =(0, 0, 0) 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER = 0
AI = 1


EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
OBSTACLE = -1  # Special marker for blocked cells


MOVE_TIME_LIMIT = 5  # seconds


# Board size options
BOARD_OPTIONS = {
    "Small (5x6)": (5, 6, 4),
    "Medium (6x7)": (6, 7, 4),
    "Large (8x10)": (8, 10, 5),
}


pygame.init()
pygame.font.init()
font = pygame.font.SysFont("monospace", 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def splash_screen():
    intro_text = font.render("Welcome to Connect 4!", True, DARK_GREEN)
    screen.fill(WHITE)
    screen.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)

splash_screen()


screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Choose Board Size")


def draw_menu():
    screen.fill(WHITE)
    title = font.render("Select Board Size", True, DARK_GREEN)
    screen.blit(title, (180, 50))


    buttons = []
    for i, option in enumerate(BOARD_OPTIONS.keys()):
        rect = pygame.Rect(150, 120 + i * 80, 300, 50)
        pygame.draw.rect(screen, Dark_Magenta, rect)
        label = font.render(option, True, WHITE)
        screen.blit(label, (rect.x + 20, rect.y + 10))
        buttons.append((rect, option))


    pygame.display.update()
    return buttons


def get_user_board_choice():
    buttons = draw_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, option in buttons:
                    if rect.collidepoint(event.pos):
                        return BOARD_OPTIONS[option]
                    
# ==== Get user board config ====
def get_user_board_config():
    global ROW_COUNT, COLUMN_COUNT, WINNING_LENGTH, SQUARESIZE, RADIUS, width, height, size,screen,myfont,smallfont
    ROW_COUNT, COLUMN_COUNT, WINNING_LENGTH = get_user_board_choice()

    SQUARESIZE = min(100, int(700 / COLUMN_COUNT))
    RADIUS = int(SQUARESIZE / 2 - 5)
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    myfont = pygame.font.SysFont("monospace", 75)
    smallfont = pygame.font.SysFont("monospace", 30)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    # Add obstacles randomly
    num_obstacles = (ROW_COUNT * COLUMN_COUNT) // 8  # ~12.5% of the board blocked
    for _ in range(num_obstacles):
        r, c = random.randint(0, ROW_COUNT-1), random.randint(0, COLUMN_COUNT-1)
        board[r][c] = OBSTACLE
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    for r in range(ROW_COUNT-1, -1, -1):
        if board[r][col] == 0:
            return True
        elif board[r][col] == OBSTACLE:
            continue
    return False


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - WINNING_LENGTH + 1):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(WINNING_LENGTH)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - WINNING_LENGTH + 1):
            if all(board[r+i][c] == piece for i in range(WINNING_LENGTH)):
                return True
    for c in range(COLUMN_COUNT - WINNING_LENGTH + 1):
        for r in range(ROW_COUNT - WINNING_LENGTH + 1):
            if all(board[r+i][c+i] == piece for i in range(WINNING_LENGTH)):
                return True
    for c in range(COLUMN_COUNT - WINNING_LENGTH + 1):
        for r in range(WINNING_LENGTH - 1, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(WINNING_LENGTH)):
                return True
    return False


def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_PIECE): return (None, float("inf"))
            elif winning_move(board, PLAYER_PIECE): return (None, float("-inf"))
            else: return (None, 0)
        return (None, score_position(board, AI_PIECE))


    best_col = random.choice(valid_locations)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta: break
    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta: break
    return best_col, value


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, Dark_Magenta, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, Turquoise, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)


    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                color = Deep_Pink
            elif board[r][c] == AI_PIECE:
                color = Lime_Green
            elif board[r][c] == OBSTACLE:
                color = GRAY
            else:
                color = Turquoise
            pygame.draw.circle(screen, color, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()


def show_timer(start_time):
    elapsed = time.time() - start_time
    remaining = max(0, MOVE_TIME_LIMIT - int(elapsed))
    box_width = 120
    box_height = 40 
    box_x = width - box_width - 10  
    box_y = 10  
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
    timer_label = smallfont.render(f"Time: {remaining}s", 1, (0, 0, 0))
    screen.blit(timer_label, (box_x + (box_width - timer_label.get_width()) // 2, box_y + (box_height - timer_label.get_height()) // 2))
    pygame.display.update()


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 80  # Block opponent's winning chance

    return score


def score_position(board, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6  # Encourage central control

    ## Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    ## Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    ## Score positive diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    ## Score negative diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

#buttons
button_width = 200
button_height = 50
button_color = (0, 200, 0)  # Green color for buttons
button_text_color = (255, 255, 255)  # White text
button_font = pygame.font.SysFont("monospace", 25)

# Function to draw the button
def draw_button(x, y, text, color):
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_surface = button_font.render(text, True, button_text_color)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)

# Function to handle button click events
def handle_button_click(x, y, text, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if x <= pos[0] <= x + button_width and y <= pos[1] <= y + button_height:
            if text == "Restart Game":
                return 'restart'
            elif text == "End Game":
                return 'quit'
    return None

# ==== Game Logic ====


def provide_hint(board):
    valid_locations = get_valid_locations(board)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, PLAYER_PIECE)
        if winning_move(temp_board, PLAYER_PIECE):
            return col  # Suggest this column as a winning move

    # If no winning move found, suggest blocking AI winning move
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, AI_PIECE)
        if winning_move(temp_board, AI_PIECE):
            return col  # Block AI's winning move

    # No immediate winning or losing move, return None
    return None


def draw_hint_line(col, time_remaining):
    # Change the hint line color to dark green only if time remains
    color = DARK_GREEN if time_remaining > 0 else GRAY  # Gray when time is over
    
    # Draw a hint line at the top of the suggested column
    pygame.draw.line(screen, color, 
                     (col * SQUARESIZE + SQUARESIZE / 2, 0), 
                     (col * SQUARESIZE + SQUARESIZE / 2, SQUARESIZE), 
                     5)

def is_board_full(board):
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            return False
    return True

# Game loop modification
board = None
game_over = False
turn = random.randint(PLAYER, AI)
winner=None

# Track game statistics
player_moves = 0
ai_moves = 0
ai_optimal_moves = 0
ai_blocks = 0

start_game_time = time.time()
player_moves = 0
ai_moves = 0
def main_game():
    global board,game_over,turn,winner,player_moves,ai_moves,ai_optimal_moves,ai_blocks,start_game_time,player_moves,ai_moves
    board = create_board()
    game_over = False
    turn = random.randint(PLAYER, AI)
    winner=None

    # Track game statistics
    player_moves = 0
    ai_moves = 0
    ai_optimal_moves = 0
    ai_blocks = 0

    draw_board(board)

    start_game_time = time.time()
    player_moves = 0
    ai_moves = 0
    while not game_over:
        start_time = time.time()
        move_made = False
        while not move_made and not game_over:
            show_timer(start_time)
            time_elapsed = time.time() - start_time
            time_remaining = max(0, MOVE_TIME_LIMIT - int(time_elapsed))

            if time_elapsed > MOVE_TIME_LIMIT:
                turn = (turn + 1) % 2
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if turn == PLAYER:
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                        posx = event.pos[0]
                        pygame.draw.circle(screen, Deep_Pink, (posx, int(SQUARESIZE/2)), RADIUS)
                        pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        posx = event.pos[0]
                        col = int(math.floor(posx / SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, PLAYER_PIECE)

                            if winning_move(board, PLAYER_PIECE):
                                game_over = True
                                winner='Player'
                            elif is_board_full(board):  # <- check for tie
                                game_over = True
                                winner = 'Tie'

                            draw_board(board)
                            player_moves += 1
                            move_made = True
                            turn = (turn + 1) % 2

                # Provide hint to player during their turn
                if turn == PLAYER:
                    hint_col = provide_hint(board)
                    if hint_col is not None:  # If there's a hint column
                        draw_hint_line(hint_col, time_remaining)

            if turn == AI and not move_made:
                pygame.time.delay(500)

                valid_locations = get_valid_locations(board)
                blocking_moves = []
                for col_check in valid_locations:
                    temp_board = board.copy()
                    row_check = get_next_open_row(temp_board, col_check)
                    drop_piece(temp_board, row_check, col_check, PLAYER_PIECE)
                    if winning_move(temp_board, PLAYER_PIECE):
                        blocking_moves.append(col_check)

                col, score = minimax(board, 4, -math.inf, math.inf, True)

                if col in blocking_moves:
                    ai_blocks += 1
                if score == float("inf"):
                    ai_optimal_moves += 1

                if col is not None and is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        game_over = True
                        winner='AI'
                    elif is_board_full(board):
                        game_over = True
                        winner = 'Tie'

                    draw_board(board)
                    ai_moves += 1
                    move_made = True
                    turn = (turn + 1) % 2
            

while game_over==False:
    get_user_board_config()
    main_game()
    time.sleep(5)
    # ==== POST-GAME STATISTICS PANEL ====
    end_game_time = time.time()
    total_duration = int(end_game_time - start_game_time)

    screen.fill(WHITE)
    draw_board(board)

    stats_panel = pygame.Surface((width, height))
    stats_panel.fill(WHITE)

    title_text = myfont.render("Game Over!", True, DARK_GREEN)
    title_rect = title_text.get_rect(center=(width // 2, 50))
    stats_panel.blit(title_text, title_rect)

    stats_list = [
        f"Winner: {winner }",
        f"Player Moves: {player_moves}",
        f"AI Moves: {ai_moves}",
        f"AI Optimal Moves: {ai_optimal_moves}",
        f"AI Blocking Moves: {ai_blocks}",
        f"Game Duration: {total_duration} sec"
    ]
    myfile = open('scores.txt', 'a')
    myfile.write(f'       Board Size:{ROW_COUNT}x{COLUMN_COUNT}\n')
    for idx, stat in enumerate(stats_list):
        stat_text = smallfont.render(stat, True, DARK_GREEN)
        stat_rect = stat_text.get_rect(topleft=(60, 120 + idx * 40))
        stats_panel.blit(stat_text, stat_rect)
        myfile.write(stat + '\n')
    myfile.write('-------------------------------------\n')
    myfile.close()
    screen.blit(stats_panel, (0, 0))

    # Draw the Restart and End Game Buttons
    draw_button(width // 4 - button_width // 2, height - 150, "Restart Game", button_color)
    draw_button(3 * width // 4 - button_width // 2, height - 150, "End Game", button_color)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle button clicks
            result = handle_button_click(width // 4 - button_width // 2, height - 150, "Restart Game", event)
            if result == 'restart':
                waiting = False
                # Restart the game
                board = create_board()
                game_over = False
                turn = random.randint(PLAYER, AI)
                player_moves = 0
                ai_moves = 0
                ai_optimal_moves = 0
                ai_blocks = 0
                start_game_time = time.time()
                draw_board(board)
                break

            result = handle_button_click(3 * width // 4 - button_width // 2, height - 150, "End Game", event)
            if result == 'quit':
                game_over=True
                pygame.quit()
                sys.exit()