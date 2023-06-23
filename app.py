# Import libraries
import streamlit as st
import pandas as pd
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

# Create a selectbox for 地域 in the sidebar
selected_地域 = st.sidebar.selectbox('地域を選択してください', unique_地域)

# Filter the 実施機関 based on selected 地域
unique_実施機関 = df[df["地域"] == selected_地域]["実施機関"].unique()

# Create a selectbox for 実施機関 in the sidebar
selected_実施機関 = st.sidebar.selectbox('実施機関を選択してください', unique_実施機関)

# Filter the 対象事業者 based on selected 地域 and 実施機関
unique_対象事業者 = df[(df["地域"] == selected_地域) & (df["実施機関"] == selected_実施機関)]["対象事業者"].unique()

# Create a selectbox for 対象事業者 in the sidebar
selected_対象事業者 = st.sidebar.selectbox('対象事業者を選択してください', unique_対象事業者)

# Filter the dataframe using selected 地域, 実施機関, and 対象事業者
df_search = df[(df["地域"] == selected_地域) & (df["実施機関"] == selected_実施機関) & (df["対象事業者"] == selected_対象事業者)]

# Show the results and balloons
st.write(df_search)
st.balloons()

# Prepare the initial question
info_to_ask = f"地域は {selected_地域}、実施機関は {selected_実施機関}、対象事業者は {selected_対象事業者} で補助金 {len(df_search)} 個と一致するリスト"

# Get user's input
user_input = st.text_input("あなたの質問を入力してください", value=info_to_ask)

if st.button("送信"):
    # Filter the dataframe using the user's input
    df_search = df[(df["地域"] == selected_地域) & (df["実施機関"] == selected_実施機関) & (df["対象事業者"] == selected_対象事業者)]



# Show the results and balloons
st.write(df_search)
st.balloons()

# Prepare the initial question
info_to_ask = f"地域は {selected_実施機関} で {selected_対象事業者} への補助金 {len(df_search)} 個と一致するリスト"

# Get user's input
user_input = st.text_input("あなたの質問を入力してください", value=info_to_ask)

if st.button("送信"):
    # Filter the dataframe using the user's input
    df_search = df[(df["実施機関"] == selected_実施機関) & (df["対象事業者"] == selected_対象事業者)]


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
        st.caption(f"{row['実施機関'].strip()} - {row['対象事業者'].strip()} - {row['補助金名'].strip()}")
        st.markdown(f"**申請期間: {row['申請期間'].strip()}**")
        st.markdown(f"*上限金額・助成額: {row['上限金額・助成額'].strip()}*")
        st.markdown(f"詳細: {row['詳細'].strip()}")
        st.markdown(f"**[リンク]({row['リンク'].strip()})**")
        st.markdown(f"地域: {row['地域'].strip()}")
        st.markdown(f"実施機関: {row['実施機関'].strip()}")
        st.markdown(f"補助率: {row['補助率'].strip()}")
        st.markdown(f"目的: {row['目的'].strip()}")
        st.markdown(f"対象経費: {row['対象経費'].strip()}")
        st.markdown(f"対象事業者: {row['対象事業者'].strip()}")
        st.markdown(f"公式公募ページ: {row['公式公募ページ'].strip()}")
