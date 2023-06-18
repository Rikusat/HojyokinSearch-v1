# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="補助金検索くん", page_icon="🐍", layout="wide")
st.title("補助金検索くん🐍")


# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

# Assuming that the "上限金額・助成額" column contains strings with commas as thousands separator,
# we first remove the commas and convert the column to numeric
df['上限金額・助成額'] = pd.to_numeric(df['上限金額・助成額'].str.replace(',', ''))

# User selects 地域
unique_地域 = df["地域"].unique()
selected_地域 = st.selectbox('地域を選択してください', unique_地域)

# Filter 対象事業者 based on selected 地域
unique_対象事業者 = df[df["地域"] == selected_地域]["対象事業者"].unique()
selected_対象事業者 = st.selectbox('対象事業者を選択してください', unique_対象事業者)

# User selects order
order = st.selectbox('ソート順を選択してください', ['大きい順', '小さい順'])

# Filter the dataframe
df_search = df[(df["地域"] == selected_地域) & (df["対象事業者"] == selected_対象事業者)]

# Order the dataframe
if order == '大きい順':
    df_search = df_search.sort_values(by='上限金額・助成額', ascending=False)
elif order == '小さい順':
    df_search = df_search.sort_values(by='上限金額・助成額')

# Display the data
st.write(df_search)
st.balloons()

# Show the cards
N_cards_per_row = 3
for n_row, row in df_search.reset_index().iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
        cols = st.columns(N_cards_per_row, gap="large")
    with cols[n_row % N_cards_per_row]:
        st.caption(f"{row['地域'].strip()} - {row['対象事業者'].strip()} - {row['補助金名'].strip()}")
        st.markdown(f"**申請期間: {row['申請期間'].strip()}**")
        st.markdown(f"*上限金額・助成額: {row['上限金額・助成額']:,}*")
        st.markdown(f"補助率: {row['補助率'].strip()}")
        st.markdown(f"目的: {row['目的'].strip()}")
        st.markdown(f"対象経費: {row['対象経費'].strip()}")
        st.markdown(f"**[リンク]({row['リンク'].strip()})**")
