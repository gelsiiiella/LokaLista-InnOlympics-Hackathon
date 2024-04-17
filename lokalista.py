import streamlit as st
import pandas as pd
from streamlit_extras.tags import tagger_component
from streamlit_gsheets import GSheetsConnection

def main_interface():
    plaintext = st.text_input(label="Enter your budget amount", value="1000")
    
    st.markdown("---")
    st.header("Ingredients")
    categories = ["canned goods", "dairy products", "meat", "fish", "vegetables", "fruits", "beverages", "snacks", "condiments", "frozen foods", "baking supplies", "cleaning supplies", "personal care"]
    
    rows = 5
    cols = st.columns(3)
    selected_categories = {}
    for i in range(rows):
        for j in range(3):
            index = i * 3 + j
            if index < len(categories):
                selected_categories[categories[index]] = cols[j].checkbox(categories[index])
    
    st.button("Submit")
    
def gsheet():   
    url = "https://docs.google.com/spreadsheets/d/1RiUc_unHWsdjHpAG8mIvMb1GD3_atoSSI_D_cSCCu2k/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3, 4, 5])
    st.dataframe(data)

def notion():
    pass

def generate():
    pass

def search():
    pass
    
main_interface()
gsheet()

