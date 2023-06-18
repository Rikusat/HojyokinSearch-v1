# Import libraries
import streamlit as st
import pandas as pd
import openai
import requests
import json
import streamlit.components.v1 as components
import time


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

# Create a selectbox for 地域 in the sidebar
selected_地域 = st.sidebar.selectbox('地域を選択してください', unique_地域)

# Filter the 対象事業者 based on selected 地域
unique_対象事業者 = df[df["地域"] == selected_地域]["対象事業者"].unique()

# Create a selectbox for 対象事業者 in the sidebar
selected_対象事業者 = st.sidebar.selectbox('対象事業者を選択してください', unique_対象事業者)

# Filter the dataframe using selected 地域 and 対象事業者
df_search = df[(df["地域"] == selected_地域) & (df["対象事業者"] == selected_対象事業者)]


# ページにテキストボックスを表示
email_input = st.sidebar.text_input("メールアドレスを入力してください")
message_input = st.sidebar.text_input("申請を行う場合、メールアドレスを入力し送信してください:", value=f" {email_input} {selected_地域} の {selected_対象事業者} の {len(df_search)} 個のリストを取得しました")

if st.sidebar.button("送信"):
    # テンプレートの作成
    info_to_ask = f"The selected region is {selected_地域} and the selected business is {selected_対象事業者}. There are {len(df_search)} items in the filtered list."
    message_template = "ユーザーからのメッセージ: {}\n\n{}"
    
    # テンプレートにメッセージを組み込んで送信
    message = message_template.format(message_input, info_to_ask)
    result = send_message_to_bot('tI6OSbQdwZIbdANCJpO9', 'LDbjERuQV2kJtkDozNIX', message)
    st.write(result)

# Show the results and balloons
st.write(df_search)
st.balloons()


def send_message_to_bot(team_id, bot_id, message):
    # URLを構築
    url = f"https://api.docsbot.ai/teams/{team_id}/bots/{bot_id}/chat"

    # 送信するメッセージをJSON形式に変換
    data = json.dumps({"question": message})  # 'content'ではなく'question'に変更する

    # ヘッダーを定義
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '9d7e3da1547d23fb4a8193c72d036bf6b2cd799999590fc6ae3176ab9c2703d6',  # replace 'your_token' with your actual token
    }

    # POSTリクエストを実行
    response = requests.post(url, headers=headers, data=data)

    # レスポンスをチェック
    if response.status_code == 200:
        return response.json()  # success
    else:
        return response.status_code, response.text  # return error information

result = send_message_to_bot('tI6OSbQdwZIbdANCJpO9', 'LDbjERuQV2kJtkDozNIX', message_input)


# Show the cards
N_cards_per_row = 3
for n_row, row in df_search.reset_index().iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
        cols = st.columns(N_cards_per_row, gap="large")
    # draw the card
    with cols[n_row % N_cards_per_row]:
        st.caption(f"{row['地域'].strip()} - {row['対象事業者'].strip()} - {row['補助金名'].strip()}")
        st.markdown(f"**申請期間: {row['申請期間'].strip()}**")
        st.markdown(f"*上限金額・助成額: {row['上限金額・助成額'].strip()}*")
        st.markdown(f"補助率: {row['補助率'].strip()}")
        st.markdown(f"目的: {row['目的'].strip()}")
        st.markdown(f"対象経費: {row['対象経費'].strip()}")
        st.markdown(f"**[リンク]({row['リンク'].strip()})**")

