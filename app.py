import pandas as pd
import streamlit as st
import requests
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

# 対象事業者の各文字列を取得して一意の値を生成
filter_options = set()
for item in df["対象事業者"]:
    options = item.split("／")
    filter_options.update(options)

# フィルタリング用の選択ボックスを作成
cols = 4  # 1行に表示するチェックボックスの数
num_checkboxes = len(filter_options)
num_rows = (num_checkboxes + cols - 1) // cols
checkboxes = []
for row in range(num_rows):
    col1, col2, col3, col4 = st.beta_columns(cols)
    for col_index, option_index in enumerate(range(row * cols, min((row + 1) * cols, num_checkboxes))):
        option = list(filter_options)[option_index]
        checkbox = col1.checkbox(option, key=option_index)
        checkboxes.append(checkbox)

selected_options = [option for option, checkbox in zip(filter_options, checkboxes) if checkbox]

# フィルタリング
df_search = df[df["対象事業者"].apply(lambda x: all(opt in x.split("／") for opt in selected_options))]

# 結果の表示
st.write(df_search)

# Show the results and balloons
st.write(df_search)
st.balloons()
