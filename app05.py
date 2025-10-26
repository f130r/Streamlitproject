import streamlit as st
import pandas as pd
import os

CSV_FILE = "shopping.csv"

# データ読み込み
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["商品名", "数量", "購入済み"])

st.title("🛒 お買い物リストアプリ")

# 商品追加フォーム
st.subheader("📝 商品を追加")
col1, col2 = st.columns([3, 1])
with col1:
    item = st.text_input("商品名")
with col2:
    quantity = st.number_input("数量", min_value=1, value=1)

if st.button("追加"):
    if item:
        new_item = pd.DataFrame([{
            "商品名": item, "数量": quantity, "購入済み": False
        }])
        df = pd.concat([df, new_item], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success(f"{item} を追加しました！")
        st.rerun()  # 画面を再読み込み
