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

# Filter the 対象事業者 based on selected 地域
unique_対象事業者 = df[df["地域"] == selected_地域]["対象事業者"].unique()

# Create a selectbox for 対象事業者 in the sidebar
selected_対象事業者 = st.sidebar.selectbox('対象事業者を選択してください', unique_対象事業者)

# Filter the dataframe using selected 地域 and 対象事業者
df_search = df[(df["地域"] == selected_地域) & (df["対象事業者"] == selected_対象事業者)]

# Show the results and balloons
st.write(df_search)
st.balloons()

# Get the information to ask OpenAI
info_to_ask = f"地域は {selected_地域} で、 {selected_対象事業者}が受けれる補助金を {len(df_search)} 個のリストの中から探してください"

# Define the message input for OpenAI
message = st.text_input("ユーザーからのメッセージ:", value=info_to_ask)

# Load the data
df = pd.read_csv(url)

# Get user's input
user_input = st.text_input("Please enter your question")

# Assuming that the user's input is a column name in the data
# You might need to process the user's input further to match it to the data in your Google spreadsheet
if user_input in df.columns:
    # Get the unique values in the selected column
    unique_values = df[user_input].unique()

    # Convert the unique values to a string
    unique_values_str = ', '.join([str(val) for val in unique_values])

    # Prepare the message for the model
    message = f"The unique values in the {user_input} column are: {unique_values_str}. Can you provide more details?"

    if st.button("送信"):
        # Use OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        # Show OpenAI's response
        st.write(response['choices'][0]['message']['content'])
    
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
