
import streamlit as st
import openai

# スタイルをカスタマイズするCSSを定義
custom_css = """
body {
    background-color: #696969; /* 背景色を設定 */
}

h1 {
    color: #ff9900; /* 見出しのテキスト色を設定 */
}

p {
    color: #708090; /* 本文のテキスト色を設定 */
}
"""

# スタイルを適用する
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)



# ユーザーインターフェースの構築
st.title("AI司法書士くん")
st.write("勝司法書士法人　任意後見チャット")

import streamlit as st
import pandas as pd


# Sidebarの選択肢を定義する
options = ["北海道", "青森県", "岩手県"]
choice = st.sidebar.selectbox("Select an option", options)

# Mainコンテンツの表示を変える
if choice == "Option 1":
    st.write("You selected Option 1")
elif choice == "Option 2":
    st.write("You selected Option 2")
else:
    st.write("You selected Option 3")


    
options = st.multiselect(
    choice = st.sidebar.selectbox("Select an option", options)
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    default=['Yellow', 'Red'] # デフォルトの設定
)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write(uploaded_file)



# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去
    

# 動的なエフェクトを追加するHTML要素
st.markdown("""
    <style>
    @keyframes robot {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>
    <div style="display: flex; justify-content: center;">
        <div style="font-size: 40px; animation: robot 2s infinite; padding-right: 10px;">🤖</div>
        <div style="font-size: 30px;">お気軽に何でもご相談ください！</div>
    </div>
""", unsafe_allow_html=True)


user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
