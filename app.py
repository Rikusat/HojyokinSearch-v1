
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

import streamlit as st

# Sidebarの選択肢を定義する
options = ["Option 1", "Option 2", "Option 3"]
choice = st.sidebar.selectbox("Select an option", options)

# Mainコンテンツの表示を変える
if choice == "Option 1":
    st.write("You selected Option 1")
elif choice == "Option 2":
    st.write("You selected Option 2")
else:
    st.write("You selected Option 3")


import io
import MeCab
import pandas as pd
import streamlit as st
from collections import Counter
from wordcloud import WordCloud

# ページのレイアウトを設定
st.set_page_config(
    page_title="テキスト可視化",
    layout="wide", # wideにすると横長なレイアウトに
    initial_sidebar_state="expanded"
)

# タイトルの設定
st.title("テキスト可視化")

# サイドバーにアップロードファイルのウィジェットを表示
st.sidebar.markdown("# ファイルアップロード")
uploaded_file = st.sidebar.file_uploader(
    "テキストファイルをアップロードしてください", type="txt"
)

# ワードクラウド、出現頻度表の各処理をサイドバーに表示
st.sidebar.markdown("# 可視化のオプション")
if uploaded_file is not None:
    # 処理の選択
    option = st.sidebar.selectbox(
        "処理の種類を選択してください", ["ワードクラウド", "出現頻度表"]
    )
    # ワードクラウドの表示
    if option == "ワードクラウド":
        pos_options = ["名詞", "形容詞", "動詞", "副詞", "助詞", "助動詞", "接続詞", "感動詞", "連体詞", "記号", "未知語"]
        # マルチセレクトボックス
        selected_pos = st.sidebar.multiselect("品詞選択", pos_options, default=["名詞"])
        if st.sidebar.button("生成"):
            st.markdown("## ワードクラウド")
            with st.spinner("Generating..."):
                io_string = io.StringIO(uploaded_file.getvalue().decode("shift-jis"))
                text = io_string.read()
                tagger = MeCab.Tagger()
                node = tagger.parseToNode(text)
                words = []
                while node:
                    if node.surface.strip() != "":
                        word_type = node.feature.split(",")[0]
                        if word_type in selected_pos: # 対象外の品詞はスキップ
                            words.append(node.surface)
                    node = node.next
                word_count = Counter(words)
                wc = WordCloud(
                    width=800,
                    height=800,
                    background_color="white",
                    font_path="./ipaexg00401/ipaexg.ttf", # Fontを指定
                )
                # ワードクラウドを作成
                wc.generate_from_frequencies(word_count)
                # ワードクラウドを表示
                st.image(wc.to_array())
    
    # 出現頻度表の表示
    elif option == "出現頻度表":
        pos_options = ["名詞", "形容詞", "動詞", "副詞", "助詞", "助動詞", "接続詞", "感動詞", "連体詞", "記号", "未知語"]
        # マルチセレクトボックス
        selected_pos = st.sidebar.multiselect("品詞選択", pos_options, default=pos_options)
        if st.sidebar.button("生成"):
            st.markdown("## 出現頻度表")
            with st.spinner("Generating..."):
                io_string = io.StringIO(uploaded_file.getvalue().decode("shift-jis"))
                text = io_string.read()
                tagger = MeCab.Tagger()
                node = tagger.parseToNode(text)

                # 品詞ごとに出現単語と出現回数をカウント
                pos_word_count_dict = {}
                while node:
                    pos = node.feature.split(",")[0]
                    if pos in selected_pos:
                        if pos not in pos_word_count_dict:
                            pos_word_count_dict[pos] = {}
                        if node.surface.strip() != "":
                            word = node.surface
                            if word not in pos_word_count_dict[pos]:
                                pos_word_count_dict[pos][word] = 1
                            else:
                                pos_word_count_dict[pos][word] += 1
                    node = node.next

                # カウント結果を表にまとめる
                pos_dfs = []
                for pos in selected_pos:
                    if pos in pos_word_count_dict:
                        df = pd.DataFrame.from_dict(pos_word_count_dict[pos], orient="index", columns=["出現回数"])
                        df.index.name = "出現単語"
                        df = df.sort_values("出現回数", ascending=False)
                        pos_dfs.append((pos, df))

                # 表を表示
                for pos, df in pos_dfs:
                    st.write(f"【{pos}】")
                    st.dataframe(df, 400, 400)
else:
    # テキスト未アップロード時の処理
    st.write("テキストファイルをアップロードしてください。")



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
