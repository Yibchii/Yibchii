import os

# Create directories
os.makedirs("tictactoe/states", exist_ok=True)

def get_board_string(board):
    return "".join(board)

def check_winner(b):
    lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for x, y, z in lines:
        if b[x] == b[y] == b[z] and b[x] != 'E':
            return b[x]
    if 'E' not in b:
        return 'T' # Tie
    return None

def minimax(board, is_max):
    score = check_winner(board)
    if score == 'O': return 1
    if score == 'X': return -1
    if score == 'T': return 0
    
    if is_max:
        best = -1000
        for i in range(9):
            if board[i] == 'E':
                board[i] = 'O'
                best = max(best, minimax(board, False))
                board[i] = 'E'
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] == 'E':
                board[i] = 'X'
                best = min(best, minimax(board, True))
                board[i] = 'E'
        return best

def find_best_move(board):
    best_val = -1000
    best_move = -1
    for i in range(9):
        if board[i] == 'E':
            board[i] = 'O'
            move_val = minimax(board, False)
            board[i] = 'E'
            if move_val > best_val:
                best_val = move_val
                best_move = i
    return best_move

def generate_markdown(board, is_root=False):
    content = "<table>\n"
    winner = check_winner(board)
    
    for r in range(3):
        content += "  <tr>\n"
        for c in range(3):
            idx = r * 3 + c
            cell = board[idx]
            if cell == 'X':
                content += "    <td>❌</td>\n"
            elif cell == 'O':
                content += "    <td>⭕</td>\n"
            else:
                if winner:
                    content += "    <td>⬜</td>\n"
                else:
                    next_board = list(board)
                    next_board[idx] = 'X'
                    ai_move = find_best_move(next_board)
                    if ai_move != -1:
                        next_board[ai_move] = 'O'
                    
                    next_state_str = get_board_string(next_board)
                    path_prefix = "tictactoe/states/" if is_root else ""
                    content += f'    <td><a href="{path_prefix}{next_state_str}.md">⬜</a></td>\n'
        content += "  </tr>\n"
    content += "</table>\n\n"
    
    if not is_root:
        content += "[🔄 Reset Game](../../README.md)\n"
    else:
        content += "[🔄 Reset Game](README.md)\n"
        
    return content

# Generate all states
visited = set()
def build_game_tree(board):
    board_str = get_board_string(board)
    if board_str in visited:
        return
    visited.add(board_str)
    
    with open(f"tictactoe/states/{board_str}.md", "w", encoding="utf-8") as f:
        f.write(generate_markdown(board))
        
    if check_winner(board):
        return
        
    for i in range(9):
        if board[i] == 'E':
            next_board = list(board)
            next_board[i] = 'X'
            ai_move = find_best_move(next_board)
            if ai_move != -1:
                next_board[ai_move] = 'O'
            build_game_tree(next_board)

# Create root
start_board = ['E'] * 9
with open("README.md", "w", encoding="utf-8") as f:
    f.write(generate_markdown(start_board, is_root=True))

build_game_tree(start_board)
print("Done! Generated clean board matrices.")
