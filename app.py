# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AI補助金サーチくん2.0", page_icon="🐍", layout="wide")
st.title("AI補助金サーチくん2.0")

# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search videos by title or speaker", value="")
