
import streamlit as st
import openai
import pandas as pd
import uuid
import numpy as np

# ページのレイアウトを設定
st.set_page_config(
    page_title="全国補助金検索アプリ",
    layout="wide", # wideにすると横長なレイアウトに
    initial_sidebar_state="expanded"
)


# ユーザーインターフェースの構築
st.title("補助金検索くん")


    

# Sidebarの選択肢を定義する
options = ["東京","北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
choice = st.sidebar.selectbox("Select an option", options)


# サイドバーにアップロードファイルのウィジェットを表示
st.sidebar.markdown("# ファイルアップロード")
uploaded_file = st.sidebar.file_uploader(
    "AIに読み込ませたいファイルをアップロードしてください", type="txt"
)

 

    

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
        <div style="font-size: 30px;">AIが補助金を検索します</div>
    </div>
""", unsafe_allow_html=True)




options = st.multiselect(
    '補助金の種類を選択してください',
    ['大企業', '中小企業', 'スタートアップ', '個人事業主', '地方自治体', '子ども家庭', '障がい者', '高齢者'],
    default=['中小企業', '個人事業主'] # デフォルトの設定
)




def main1():
    # 東京のランダムな経度・緯度を生成する
    data = {
        'lat': np.random.randn(100) / 100 + 35.68,
        'lon': np.random.randn(100) / 100 + 139.75,
    }
    map_data = pd.DataFrame(data)
    # 地図に散布図を描く
    st.map(map_data)
    
if __name__ == '__main__':
    main1()
    
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
        model="gpt-3.5-turbo-16k",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

    

    


