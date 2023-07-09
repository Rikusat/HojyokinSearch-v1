import streamlit as st
import pandas as pd
import requests
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Page setup
st.set_page_config(page_title="補助金検索くん　関東圏", page_icon="🎈", layout="wide")
st.title("補助金検索くん　関東圏🎈")

# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Read the data from the URL and perform data cleaning
df = pd.read_csv(url, dtype=str).fillna("")

# Function to filter data based on selected 地域 and selected_options
def filter_data(selected_地域, selected_options):
    df_filtered = df.loc[(df["地域"] == selected_地域) & (df["対象事業者"].str.contains("|".join(selected_options))), :]
    return df_filtered

# Get a list of unique 地域
unique_地域 = df["地域"].unique()

# Create a selectbox for 地域
selected_地域 = st.selectbox('地域を選択', unique_地域, index=0)

# Filter options based on selected_地域
filter_options = set()
for item in df.loc[df["地域"] == selected_地域, "対象事業者"]:
    options = item.split("／")
    filter_options.update(options)

# Show the options as a selectbox
selected_options = st.multiselect("当てはまる項目を選択 : 複数可", list(filter_options))

# Filter the data
df_search = filter_data(selected_地域, selected_options)

# Prepare the initial question
info_to_ask = f"地域は{selected_地域}で、対象事業者は{', '.join(selected_options)} "

# Get user's input
user_input = st.text_input("補足情報を自由に入力してください", value=info_to_ask)

if st.button("AIに聞く"):
    # Check if the dataframe is empty
    if df_search.empty:
        st.write("No matching data found.")
    else:
        # If not, use the data to generate a message for GPT-3
        message = f"I found {len(df_search)} matches for the 地域 '{user_input}'. Here's the first one: {df_search.iloc[0].to_dict()}"

        # Add user's input to the message
        message += f"\n{user_input}"

       # Use OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        # Show OpenAI's response
        st.write(response.choices[0].text)

st.markdown("---")
        
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
        st.caption(f"{row['詳細'].strip()}")
        st.markdown(f"{row['上限金額・助成額'].strip()}")
        st.markdown(f"{row['申請期間'].strip()}")
        st.markdown(f"地域: {row['地域'].strip()}")
        st.markdown(f"実施機関: {row['実施機関'].strip()}")
        st.markdown(f"対象事業者: {row['対象事業者'].strip()}")
        st.markdown(f"公式公募ページ: {row['公式公募ページ'].strip()}")
        st.markdown(f"**[掲載元]({row['掲載元'].strip()})**")
        st.markdown("---")
