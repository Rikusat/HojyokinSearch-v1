import streamlit as st
import pandas as pd
import requests


# Page setup
st.set_page_config(page_title="関東圏：補助金検索くん", page_icon="🎈", layout="wide")
st.title("関東圏：補助金検索くん🎈")

# Correct the formation of the URL
sheet_id = "1s-LHhUIa-SgYJFHggP94LyG-KXqaNr_Xx7SPROtTaSI"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str)

# Show the cards
N_cards_per_row = 3
cols = st.columns(N_cards_per_row, gap="large")
for n_row, row in df_search.iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
    # draw the card
    with cols[i]:
        st.markdown(f"**{row['question'].strip()}**")
        st.caption(f"{row['answer'].strip()}")
        st.markdown(f"{row['sources'].strip()}")
