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
selected_options = []
for option in filter_options:
    selected = st.checkbox(option)
    if selected:
        selected_options.append(option)

# フィルタリング
df_search = df[df["対象事業者"].apply(lambda x: all(opt in x.split("／") for opt in selected_options))]

# 結果の表示
st.write(df_search)


# Show the results and balloons
st.write(df_search)
st.balloons()

# Prepare the initial question
info_to_ask = f"地域は {selected_地域} で {selected_対象事業者} への補助金 {len(df_search)} 個と一致するリスト"

# Get user's input
user_input = st.text_input("あなたの質問を入力してください", value=info_to_ask)

if st.button("送信"):
    # Filter the dataframe using the user's input
    df_search = df[(df["地域"] == selected_地域) & (df["対象事業者"] == selected_対象事業者)]


    # Check if the dataframe is empty
    if df_search.empty:
        st.write("No matching data found.")
    else:
        # If not, use the data to generate a message for GPT-3
        message = f"I found {len(df_search)} matches for the 地域 '{user_input}'. Here's the first one: {df_search.iloc[0].to_dict()}"

        # Use OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "あなたは優秀なデータサイエンティストです。全て日本語で返答してください."},
                {"role": "user", "content": message}
            ]
        )
        # Show OpenAI's response
        st.write(response['choices'][0]['message']['content'])
        
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
        st.markdown(f {row['上限金額・助成額'].strip()}*")
        st.markdown(f"詳細: {row['詳細'].strip()}")
        st.markdown(f"**[リンク]({row['リンク'].strip()})**")
        st.markdown(f"地域: {row['地域'].strip()}")
        st.markdown(f"実施機関: {row['実施機関'].strip()}")
        st.markdown(f"対象事業者: {row['対象事業者'].strip()}")
        st.markdown(f"公式公募ページ: {row['公式公募ページ'].strip()}")
