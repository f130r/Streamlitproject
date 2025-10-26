import streamlit as st
import pandas as pd
import os

CSV_FILE = "data.csv"

# データ読み込み
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["名前", "年齢"])

st.title("📝 データ登録アプリ")

# 入力フォーム
name = st.text_input("名前")
age = st.number_input("年齢", min_value=0, max_value=120)

if st.button("登録"):
    new_data = pd.DataFrame([{"名前": name, "年齢": age}])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success("登録しました！")

st.dataframe(df)