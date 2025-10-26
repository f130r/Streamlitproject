import numpy as np
import matplotlib.pyplot as plt

EMPTY, BLACK, WHITE = 0, 1, -1
SIZE = 8

board = np.zeros((SIZE, SIZE), dtype=int)
board[3, 3], board[4, 4] = WHITE, WHITE
board[3, 4], board[4, 3] = BLACK, BLACK

turn = BLACK
dirs = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]

def inside(x, y):
    return 0 <= x < SIZE and 0 <= y < SIZE

def valid_moves(board, color):
    moves = []
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y, x] != EMPTY:
                continue
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                found = False
                while inside(nx, ny) and board[ny, nx] == -color:
                    found = True
                    nx += dx
                    ny += dy
                if found and inside(nx, ny) and board[ny, nx] == color:
                    moves.append((x, y))
                    break
    return moves

def place_stone(board, x, y, color):
    board[y, x] = color
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        flips = []
        while inside(nx, ny) and board[ny, nx] == -color:
            flips.append((nx, ny))
            nx += dx
            ny += dy
        if inside(nx, ny) and board[ny, nx] == color:
            for fx, fy in flips:
                board[fy, fx] = color

def ai_move(board, color):
    moves = valid_moves(board, color)
    if not moves:
        return None
    best = None
    max_flips = -1
    for (x, y) in moves:
        temp = board.copy()
        place_stone(temp, x, y, color)
        flips = np.sum(temp == color) - np.sum(board == color)
        if flips > max_flips:
            max_flips = flips
            best = (x, y)
    return best

fig, ax = plt.subplots()

def draw_board():
    ax.clear()
    ax.set_xticks(range(SIZE + 1))
    ax.set_yticks(range(SIZE + 1))
    ax.grid(True, color='black', linewidth=1)

    # 緑背景
    ax.set_facecolor('#2e7d32')

    # 茶系木目風盤面
    brown_base = np.array([0.55, 0.42, 0.27])
    for i in range(SIZE):
        for j in range(SIZE):
            variation = ((i+j)%2) * 0.05
            color = np.clip(brown_base + variation, 0, 1)
            ax.add_patch(plt.Rectangle((i, j), 1, 1, color=color, zorder=0))

    # 黒石
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y, x] == BLACK:
                c = plt.Circle((x + 0.5, SIZE - y - 0.5), 0.4,
                               facecolor='black', edgecolor='black', zorder=3)
                ax.add_patch(c)
    # 白石
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y, x] == WHITE:
                c = plt.Circle((x + 0.5, SIZE - y - 0.5), 0.4,
                               facecolor='white', edgecolor='black', linewidth=1, zorder=4)
                ax.add_patch(c)

    ax.set_xlim(0, SIZE)
    ax.set_ylim(0, SIZE)
    ax.set_aspect('equal')
    ax.set_title("黒：あなた　白：コンピュータ")
    plt.draw()

def onclick(event):
    global turn
    if event.xdata is None or event.ydata is None:
        return
    if turn != BLACK:
        return
    x, y = int(event.xdata), SIZE - int(event.ydata) - 1
    if (x, y) in valid_moves(board, turn):
        place_stone(board, x, y, turn)
        turn *= -1
        draw_board()
        plt.pause(0.5)
        ai_turn()

def ai_turn():
    global turn
    move = ai_move(board, turn)
    if move:
        x, y = move
        place_stone(board, x, y, turn)
        draw_board()
    turn *= -1

draw_board()
fig.canvas.mpl_connect("button_press_event", onclick)
plt.show()
