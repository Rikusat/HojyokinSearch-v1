import pandas as pd
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Page setup
st.set_page_config(page_title="補助金検索くん", page_icon="🎈", layout="wide")
st.title("補助金検索くん🎈")

# Add additional text above the title
st.markdown("**補助金を効率的に検索するツールです**")

# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Function to filter data based on selected 地域 and selected_options
def filter_data(selected_地域, selected_options):
    df = pd.read_csv(url, dtype=str).fillna("")
    df_filtered = df[(df["地域"] == selected_地域) & (df["対象事業者"].str.contains("|".join(selected_options)))]
    return df_filtered

# Get a list of unique 地域
df = pd.read_csv(url, dtype=str).fillna("")
unique_地域 = df["地域"].unique()

# Create a selectbox for 地域
selected_地域 = st.selectbox('地域を選択してください', unique_地域)

# 対象事業者の各文字列を取得して一意の値を生成
filter_options = set()
for item in df[df["地域"] == selected_地域]["対象事業者"]:
    options = item.split("／")
    filter_options.update(options)

# Show the options as a selectbox
selected_options = st.multiselect("対象事業者を選択してください", list(filter_options))

# フィルタリング
df_search = filter_data(selected_地域, selected_options)

# Get user's input
user_input = st.text_input("補足情報を入力してください")

if st.button("送信"):
    # Check if the dataframe is empty
    if df_search.empty:
        st.write("No matching data found.")
    else:
        # If not, use the data to generate a message for GPT-3
        message = f"I found {len(df_search)} matches for the 地域 '{selected_地域}'. Here's the first one: {df_search.iloc[0].to_dict()}"

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
