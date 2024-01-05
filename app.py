# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Python Talks Search Engine", page_icon="🐍", layout="wide")
st.title("Python Talks Search Engine")

# Connect to the Google Sheet
sheet_id = "1s-LHhUIa-SgYJFHggP94LyG-KXqaNr_Xx7SPROtTaSI"
sheet_name = "charlas"
url = f"<https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}>"
df = pd.read_csv(url, dtype=str).fillna("")

# Show the dataframe (we'll delete this later)
st.write(df)
