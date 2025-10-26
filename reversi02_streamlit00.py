import streamlit as st
import numpy as np
import random

# --- ゲームロジック ---
def init_board():
    board = np.zeros((8,8), dtype=int)
    board[3,3] = board[4,4] = 1
    board[3,4] = board[4,3] = -1
    return board

DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def valid_moves(board, player):
    moves = []
    for x in range(8):
        for y in range(8):
            if board[x,y] != 0:
                continue
            for dx,dy in DIRECTIONS:
                nx,ny = x+dx,y+dy
                found_opponent = False
                while 0<=nx<8 and 0<=ny<8:
                    if board[nx,ny] == -player:
                        found_opponent = True
                    elif board[nx,ny] == player and found_opponent:
                        moves.append((x,y))
                        break
                    else:
                        break
                    nx += dx
                    ny += dy
    return list(set(moves))

def place_stone(board, x, y, player):
    board[x,y] = player
    for dx,dy in DIRECTIONS:
        nx,ny = x+dx, y+dy
        stones_to_flip = []
        while 0<=nx<8 and 0<=ny<8:
            if board[nx,ny] == -player:
                stones_to_flip.append((nx,ny))
            elif board[nx,ny] == player:
                for fx,fy in stones_to_flip:
                    board[fx,fy] = player
                break
            else:
                break
            nx += dx
            ny += dy
    return board

def ai_move(board):
    moves = valid_moves(board, -1)
    if moves:
        return random.choice(moves)
    return None

def score(board):
    black = np.sum(board==1)
    white = np.sum(board==-1)
    return black, white

# --- HTML盤面描画（600px固定版） ---
def render_board_html(board, moves=None, total_size=600):
    html = f'<div style="width:{total_size}px; margin:auto;">'
    html += '<table style="border-collapse: collapse; width:100%;">'
    cell_size = total_size // 8

    for x in range(8):
        html += '<tr>'
        for y in range(8):
            cell_value = board[x,y]
            style = f'width:{cell_size}px; height:{cell_size}px; text-align:center; vertical-align:middle; border:2px solid black; background-color:green; position:relative;'
            if moves and (x,y) in moves:
                style += ' outline:3px solid red;'
            content = ''
            if cell_value == 1:
                content = f'<div style="width:{int(cell_size*0.65)}px; height:{int(cell_size*0.65)}px; border-radius:50%; background:black; margin:auto; position:relative; top:17.5%;"></div>'
            elif cell_value == -1:
                content = f'<div style="width:{int(cell_size*0.65)}px; height:{int(cell_size*0.65)}px; border-radius:50%; background:white; border:1px solid black; margin:auto; position:relative; top:17.5%;"></div>'
            else:
                index = x*8+y
                content = f'<div style="position:absolute; top:25%; left:25%; font-weight:bold; color:white;">{index}</div>'
            html += f'<td style="{style}">{content}</td>'
        html += '</tr>'
    html += '</table></div>'
    return html

# --- Streamlit UI ---
st.title("オセロゲーム ver2.0")

if "board" not in st.session_state:
    st.session_state.board = init_board()

board = st.session_state.board
player = 1
moves = valid_moves(board, player)

# 盤面描画
st.markdown(render_board_html(board, moves, total_size=600), unsafe_allow_html=True)

# 注意書き（中央・白文字）
st.markdown(
    '<div style="text-align:center; color:white; font-weight:bold; font-size:16px;">黒の石を置くマス番号を入力して石を置くボタンは2回クリックしてください</div>',
    unsafe_allow_html=True
)

# マス番号入力
cell_number = st.number_input("置きたいマス番号(0-63)", min_value=0, max_value=63, value=0)
if st.button("石を置く"):
    x, y = divmod(cell_number, 8)
    if (x,y) in moves:
        board = place_stone(board, x, y, player)
        ai = ai_move(board)
        if ai:
            board = place_stone(board, ai[0], ai[1], -player)
    else:
        st.warning("そこには置けません。")
    st.session_state.board = board

# スコア表示
black, white = score(board)
st.markdown(f"<div style='text-align:center;font-size:20px;'>プレイヤー(黒): {black} / AI(白): {white}</div>", unsafe_allow_html=True)

# 勝敗判定
if not valid_moves(board,1) and not valid_moves(board,-1):
    if black > white:
        st.success("プレイヤーの勝ち！")
    elif white > black:
        st.success("AIの勝ち！")
    else:
        st.info("引き分け！")

# リセット
if st.button("リセット"):
    st.session_state.board = init_board()
