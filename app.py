import base64
import json
import requests
import streamlit as st
import pandas as pd
import pyperclip
import streamlit.components.v1 as components

# データフレームの例として空のデータフレームを作成
df = pd.DataFrame(columns=["地域", "対象事業者", "補助金名", "申請期間", "上限金額・助成額", "補助率", "目的", "対象経費", "リンク"])

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


# Custom text input widget that prevents form submission on Enter key press
class NoSubmitTextInput:
    def __init__(self, initial_value="", key=None):
        self._key = key
        self._current_value = initial_value
        self._assigned_placeholder = False

    def __call__(self, label, value="", **kwargs):
        value = self._current_value if value == "" else value
        input_id = st.get_session_id() + "-" + self._key if self._key else None
        components.html(
            """
            <input
                id="%s"
                type="text"
                value="%s"
                placeholder="%s"
                data-bypass="true"
                data-key="%s"
            >
            """
            % (input_id, value, label, self._key),
            scrolling=False,
        )
        result = st._get_widget_value(input_id, "no_submit_text_input", self._key)
        self._current_value = result["value"]
        self._assigned_placeholder = result["assigned_placeholder"]
        return result["value"]

# Function to copy text to clipboard
def copy_to_clipboard(text):
    pyperclip.copy(text)

# サイドバーにテキストボックスを表示
email_input = st.sidebar.text_input("メールアドレスを入力してください", key="email_input")

# Display the form and input fields
with st.sidebar.form("katsu-form"):
    message_input = NoSubmitTextInput(initial_value=f"{email_input} {selected_地域} の {selected_対象事業者} の {len(df_search)} 個のリストを取得しました", key="message_input")
    st.write("申請を行う場合、以下のメッセージを送信してください:")
    st.write(message_input("メッセージを入力してください"))

    # Display the copy button
    if st.button("コピー"):
        copy_to_clipboard(message_input._current_value)
        st.success("メッセージがクリップボードにコピーされました。")

# 送信ボタンの処理は変更なし
if st.sidebar.button("送信"):
    # テンプレートの作成
    info_to_ask = f"The selected region is {selected_地域} and the selected business is {selected_対象事業者}. There are {len(df_search)} items in the filtered list."
    message_template = "ユーザーからのメッセージ: {}\n\n{}"

    # テンプレートにメッセージを組み込んで送信
    message = message_template.format(message_input._current_value, info_to_ask)
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
