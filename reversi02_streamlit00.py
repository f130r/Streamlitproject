import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 定数 ---
EMPTY, BLACK, WHITE = 0, 1, -1
SIZE = 8
dirs = [(dx, dy) for dx in [-1,0,1] for dy in [-1,0,1] if not (dx==0 and dy==0)]

# --- 初期化 ---
if "board" not in st.session_state:
    board = np.zeros((SIZE, SIZE), dtype=int)
    board[3,3], board[4,4] = WHITE, WHITE
    board[3,4], board[4,3] = BLACK, BLACK
    st.session_state.board = board
    st.session_state.turn = BLACK

board = st.session_state.board
turn = st.session_state.turn

# --- ゲームロジック ---
def inside(x,y):
    return 0 <= x < SIZE and 0 <= y < SIZE

def valid_moves(board,color):
    moves=[]
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y,x]!=EMPTY:
                continue
            for dx,dy in dirs:
                nx,ny=x+dx,y+dy
                found=False
                while inside(nx,ny) and board[ny,nx]==-color:
                    found=True
                    nx+=dx
                    ny+=dy
                if found and inside(nx,ny) and board[ny, nx]==color:
                    moves.append((x,y))
                    break
    return moves

def place_stone(board,x,y,color):
    board[y,x] = color
    for dx,dy in dirs:
        nx,ny = x+dx, y+dy
        flips=[]
        while inside(nx,ny) and board[ny,nx]==-color:
            flips.append((nx,ny))
            nx+=dx
            ny+=dy
        if inside(nx,ny) and board[ny,nx]==color:
            for fx,fy in flips:
                board[fy,fx] = color

def ai_move(board,color):
    moves = valid_moves(board,color)
    if not moves:
        return None
    best=None
    max_flips=-1
    for x,y in moves:
        temp=board.copy()
        place_stone(temp,x,y,color)
        flips=np.sum(temp==color)-np.sum(board==color)
        if flips>max_flips:
            max_flips=flips
            best=(x,y)
    return best

# --- 描画 ---
def draw_board(board):
    fig, ax = plt.subplots()
    ax.set_xticks(range(SIZE+1))
    ax.set_yticks(range(SIZE+1))
    ax.grid(True, color='black', linewidth=1)
    ax.set_facecolor('#2e7d32')  # 緑背景

    # 木目盤
    brown_base = np.array([0.55,0.42,0.27])
    for i in range(SIZE):
        for j in range(SIZE):
            variation = ((i+j)%2)*0.05
            color = np.clip(brown_base + variation,0,1)
            ax.add_patch(plt.Rectangle((i,j),1,1,color=color,zorder=0))

    # 石と番号
    for y in range(SIZE):
        for x in range(SIZE):
            idx = (SIZE-1-y)*SIZE + x  # 上下反転して番号と一致
            ax.text(x+0.5,SIZE-y-0.5,str(idx),color='white',ha='center',va='center',zorder=5,fontweight='bold')
            if board[y,x]==BLACK:
                ax.add_patch(plt.Circle((x+0.5,SIZE-y-0.5),0.4,facecolor='black',edgecolor='black',zorder=3))
            elif board[y,x]==WHITE:
                ax.add_patch(plt.Circle((x+0.5,SIZE-y-0.5),0.4,facecolor='white',edgecolor='black',linewidth=1,zorder=4))

    ax.set_xlim(0,SIZE)
    ax.set_ylim(0,SIZE)
    ax.set_aspect('equal')
    ax.set_title("黒：あなた　白：コンピュータ")
    return fig

# --- Streamlit UI ---
st.title("Streamlit オセロ（番号入力版）")

moves = valid_moves(board, turn)
st.write(f"有効手: [{', '.join(str((SIZE-1-y)*SIZE + x) for x,y in moves)}]")  # 有効手を番号で表示

# プレイヤー入力
if turn == BLACK and moves:
    st.subheader("あなたの手番：黒")
    num = st.number_input("置くマス番号 (0-63)", min_value=0, max_value=63, step=1, key="num_input")
    if st.button("石を置く"):
        x, y = divmod(num, SIZE)
        y = SIZE - 1 - y  # 上下反転
        if (x,y) in moves:
            place_stone(board, x, y, BLACK)
            turn = WHITE
            st.session_state.turn = turn
        else:
            st.warning("そこには置けません")

# AIターン
if turn == WHITE:
    move = ai_move(board, WHITE)
    if move:
        x_ai, y_ai = move
        place_stone(board, x_ai, y_ai, WHITE)
    turn = BLACK
    st.session_state.turn = turn

# 描画
fig = draw_board(board)
st.pyplot(fig)

# 終了チェック
black_count = np.sum(board==BLACK)
white_count = np.sum(board==WHITE)
st.write(f"黒: {black_count}  白: {white_count}")
if black_count + white_count == SIZE*SIZE or (not valid_moves(board,BLACK) and not valid_moves(board,WHITE)):
    st.write("ゲーム終了")
