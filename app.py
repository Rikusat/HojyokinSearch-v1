import pandas as pd
import streamlit as st
import requests

# Google スプレッドシートの設定
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# スプレッドシートからデータフレームを取得
response = requests.get(url)
df = pd.read_csv(pd.compat.StringIO(response.text), dtype=str).fillna("")

# 対象事業者の各文字列を取得して一意の値を生成
filter_options = set()
for item in df["対象事業者"]:
    options = item.split("／")
    filter_options.update(options)

# フィルタリング用の選択ボックスを作成
cols = 4  # 1行に表示するチェックボックスの数
selected_options = []
for i, option in enumerate(filter_options):
    if i % cols == 0:
        col = st.beta_columns(cols)
    selected = col[i % cols].checkbox(option)
    if selected:
        selected_options.append(option)

# フィルタリング
df_search = df[df["対象事業者"].apply(lambda x: all(opt in x.split("／") for opt in selected_options))]

# 結果の表示
st.write(df_search)


# Show the results and balloons
st.write(df_search)
st.balloons()


# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")


# Show the cards
N_cards_per_row = 3
for n_row, row in df_search.iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
        cols = st.columns(N_cards_per_row, gap="large")
    # draw the card
    with cols[i]:
        st.caption(f"{row['地域'].strip()} - {row['対象事業者'].strip()} - {row['補助金名'].strip()}")
        st.markdown(f"**申請期間: {row['申請期間'].strip()}**")
        st.markdown(f"詳細: {row['詳細'].strip()}")
        st.markdown(f"**[リンク]({row['リンク'].strip()})**")
        st.markdown(f"地域: {row['地域'].strip()}")
        st.markdown(f"実施機関: {row['実施機関'].strip()}")
        st.markdown(f"対象事業者: {row['対象事業者'].strip()}")
        st.markdown(f"公式公募ページ: {row['公式公募ページ'].strip()}")
