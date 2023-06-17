# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AI補助金検索くん2.0", page_icon="🐍", layout="wide")
st.title("AI補助金検索くん2.0")

# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search videos by title or speaker", value="")

# Filter the dataframe using masks
m1 = df["氏名"].str.contains(text_search)
m2 = df["年齢"].str.contains(text_search)
df_search = df[m1 | m2]

# Show the results, if you have a text_search
if text_search:
    st.write(df_search)

# Another way to show the filtered results
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
            st.caption(f"{row['氏名'].strip()} - {row['氏名（ひらがな）'].strip()} - {row['年齢'].strip()} - {row['生年月日'].strip()} - {row['性別'].strip()}")
            st.markdown(f"**氏名: {row['氏名'].strip()}**")
            st.markdown(f"*氏名（ひらがな）: {row['氏名（ひらがな）'].strip()}*")
            st.markdown(f"年齢: {row['年齢'].strip()}")
            st.markdown(f"生年月日: {row['生年月日'].strip()}")
            st.markdown(f"性別: {row['性別'].strip()}")
