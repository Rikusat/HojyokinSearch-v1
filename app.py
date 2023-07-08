import pandas as pd
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# スプレッドシートからデータをフェッチする関数
def fetch_data_from_spreadsheet(sheet_id, sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url, dtype=str).fillna("")
    return df

# スプレッドシートの情報をフェッチ
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
df = fetch_data_from_spreadsheet(sheet_id, sheet_name)

# Page setup
st.set_page_config(page_title="補助金検索くん", page_icon="🎈", layout="wide")
st.title("補助金検索くん🎈")

# Function to filter data based on selected 地域 and selected_options
def filter_data(selected_地域, selected_options):
    df_filtered = df[(df["地域"] == selected_地域) & (df["対象事業者"].str.contains("|".join(selected_options)))]
    return df_filtered

# Get a list of unique 地域
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

# AIによる回答生成
def generate_answer(query):
 response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt=query,
    max_tokens=50
)

    )
    return response.choices[0].text.strip()

# ユーザーからの質問入力
user_question = st.text_input("ご質問を入力してください")

# 質問が入力された場合の処理
if user_question:
    # AIによる回答生成
    answer = generate_answer(user_question)

    # 回答を表示
    st.write("AIの回答:")
    st.write(answer)


        
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
