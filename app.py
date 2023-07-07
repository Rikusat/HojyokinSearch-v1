import pandas as pd
import streamlit as st
import requests
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# Page setup
st.set_page_config(page_title="補助金検索くん", page_icon="🎈", layout="wide")
st.title("補助金検索くん🎈")

# Add additional text above the title
st.markdown("**補助金を効率的に検索するツールです**")

# Correct the formation of the URL
sheet_id = "1NGjKJrVZUtcm9V1yiQjDaR4qbr5pqkHfSsZPWqqvA9Y"
sheet_name = "神奈川DB"
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
    checkbox_key = f"checkbox_{option}"  # チェックボックスのキー
    selected = col[i % cols].checkbox(option, key=checkbox_key, value=(option in selected_options))
    if selected:
        selected_options.append(option)
    checkboxes.append(selected)

# 選択されたオプションを表示
selected_options = list(set(selected_options))  # 重複を削除
st.write("選択されたオプション:", selected_options)

# フィルタリング
df_search = df_filtered[df_filtered["対象事業者"].str.contains("|".join(selected_options))]

# Show the results and balloons
st.write(df_search)
st.balloons()

# Prepare the initial question
info_to_ask = f" {selected_地域} の補助金リストの中から〇〇市へ出ている補助金を挙げてください "

# Get user's input
user_input = st.text_input("あなたの質問を入力してください", value=info_to_ask)

if st.button("送信"):
    # Filter the dataframe using the user's input
    df_search = df[(df["地域"] == selected_地域)]

    # Check if the dataframe is empty
    if df_search.empty:
        st.write("No matching data found.")
    else:
        # If not, use the data to generate a message for GPT-3
        message = f"I found {len(df_search)} matches for the 地域 '{user_input}'. Here's the first one: {df_search.iloc[0].to_dict()}"

        # Add AI instruction prompt
        instruction_prompt = "AIに対して追加の指示を入力してください。"
        message_with_prompt = f"{instruction_prompt}\n{message}"

        # Use OpenAI API
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=message_with_prompt,
            max_tokens=50,
            temperature=0.5
        )

        # Show OpenAI's response
        st.write(response.choices[0].text)




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
