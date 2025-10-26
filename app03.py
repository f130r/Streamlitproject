import streamlit as st

st.title("📝 ユーザー入力のテスト")

name = st.text_input("お名前を入力してください")
age = st.number_input("年齢を入力してください", min_value=0, max_value=120)

if st.button("送信"):
    st.write(f"こんにちは、{name}さん！")
    st.write(f"年齢は{age}歳ですね。")