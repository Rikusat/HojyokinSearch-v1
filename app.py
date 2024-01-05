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

# Show the dataframe (we'll delete this later)
st.write(df)



# Another way to show the filtered results
# Show the cards
N_cards_per_row = 3
if text_search:
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['question']
            st.markdown(f"**{row['answer'].strip()}**")
            st.markdown(f"*{row['sources'].strip()}*")
