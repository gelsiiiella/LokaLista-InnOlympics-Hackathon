import streamlit as st
import pandas as pd
from streamlit_extras.tags import tagger_component
from streamlit_gsheets import GSheetsConnection

def main_interface():
    plaintext = st.text_input(label="Tell us what you want to generate ")
    selected_tags = tagger_component("Categories", ["canned goods", "dairy products", "meat"], color_name=["blue", "orange", "lightblue"])
    st.button("Submit")
    
def gsheet():
    url = "https://docs.google.com/spreadsheets/d/1JDy9md2VZPz4JbYtRPJLs81_3jUK47nx6GYQjgU8qNY/edit?usp=sharing"
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url, usecols=[0, 6])
    st.dataframe(data)

def notion():
    pass

def generate():
    pass


main_interface()
    
    

