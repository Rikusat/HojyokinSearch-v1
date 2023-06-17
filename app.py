# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="補助金検索くん", page_icon="🐍", layout="wide")
st.title("🐍補助金検索くん")


# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("地域または対象事業者を入力してください", value="")

# Filter the dataframe using masks
m1 = df["地域"].str.contains(text_search)
m2 = df["対象事業者"].str.contains(text_search)
df_search = df[m1 | m2]

# Show the results and balloons, if you have a text_search
if text_search:
    st.write(df_search)
    st.balloons()
    
# Show the cards
N_cards_per_row = 3
if text_search:
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

