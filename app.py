
import streamlit as st
import openai

# ページのレイアウトを設定
st.set_page_config(
    page_title="テキスト可視化",
    layout="wide", # wideにすると横長なレイアウトに
    initial_sidebar_state="expanded"
)


# ユーザーインターフェースの構築
st.title("補助金検索くん")


import streamlit as st
import pandas as pd


options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    default=['Yellow', 'Red'] # デフォルトの設定
)
    

# Sidebarの選択肢を定義する
options = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
choice = st.sidebar.selectbox("Select an option", options)


# サイドバーにアップロードファイルのウィジェットを表示
st.sidebar.markdown("# ファイルアップロード")
uploaded_file = st.sidebar.file_uploader(
    "AIに読み込ませたいファイルをアップロードしてください", type="txt"
)





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
