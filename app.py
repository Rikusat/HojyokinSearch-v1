import pandas as pd
import streamlit as st
import requests
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Page setup
st.set_page_config(page_title="補助金検索くん", page_icon="🎈", layout="wide")
st.title("補助金検索くん🎈")

# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

# Get a list of unique 地域
unique_地域 = df["地域"].unique()

# Create a selectbox for 地域
selected_地域 = st.selectbox('地域を選択してください', unique_地域)

# Filter the dataframe based on selected 地域
df_filtered = df[df["地域"] == selected_地域]

# 対象事業者の各文字列を取得して一意の値を生成
filter_options = set()
for item in df_filtered["対象事業者"]:
    options = item.split("／")
    filter_options.update(options)

# フィルタリング用の選択ボックスを作成
cols = 4  # 1行に表示するチェックボックスの数
selected_options = []
checkboxes = []
for i, option in enumerate(filter_options):
    if i % cols == 0:
        col = st.beta_columns(cols)
    selected = col[i % cols].checkbox(option, key=option)  # チェックボックスにキーを設定
    checkboxes.append(selected)
    if len(checkboxes) == cols or i == len(filter_options) - 1:
        selected = [option for option, checkbox in zip(filter_options, checkboxes) if checkbox]
        selected_options.extend(selected)
        checkboxes = []

# フィルタリング
df_search = df_filtered[df_filtered["対象事業者"].str.contains("|".join(selected_options))]

# Show the results and balloons
st.write(df_search)
st.balloons()

# Show the cards
N_cards_per_row = 3
cols = st.columns(N_cards_per_row, gap="large")
for n_row, row in df_search.iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
    # draw the card
    with cols[i]:
        st.markdown(f"**{row['補助金名'].strip()}**")
        st.caption(f"{row['申請期間'].strip()}")
        st.markdown(f"{row['詳細'].strip()}")
        st.markdown(f"{row['上限金額・助成額'].strip()}")
        st.markdown(f"**[掲載元]({row['掲載元'].strip()})**")
        st.markdown(f"地域: {row['地域'].strip()}")
        st.markdown(f"実施機関: {row['実施機関'].strip()}")
        st.markdown(f"対象事業者: {row['対象事業者'].strip()}")
        st.markdown(f"公式公募ページ: {row['公式公募ページ'].strip()}")
