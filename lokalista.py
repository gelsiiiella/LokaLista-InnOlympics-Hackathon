import streamlit as st
import pandas as pd
from streamlit_extras.tags import tagger_component
from streamlit_gsheets import GSheetsConnection
from dotenv import load_dotenv
import os
from notion_client import Client

load_dotenv()

def main_interface():
    df = gsheet() 
    st.markdown("<h1 style='text-align: center; color: #f63366;'>LOKALISTA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>Your Local Food Recommender</p>", unsafe_allow_html=True)
    
    plaintext = st.text_input(label="Enter your budget amount", value="600")
    budget = int(plaintext)

    st.markdown("---")
    st.header("Local Produce")

    categories = df["Category"].unique().tolist()

    selected_categories = st.multiselect("Select categories", categories)

    filtered_df = df[df["Category"].isin(selected_categories)] if selected_categories else df

    st.dataframe(filtered_df)

    if st.button("Submit", key="btn1"):
        st.markdown("---")
        st.header("Recommended Items")

        recommended_list = ""
        total_price = 0
        for row in filtered_df.itertuples():
            if total_price + int(row.PricePHP) <= budget:
                recommended_list += f"{row.Province}  ||  {row.Commodity}  ||  {row.Unit}  ||  {row.PricePHP}\n"
                total_price += int(row.PricePHP)

        if recommended_list:
            recommended_list_data = [line.split("  ||  ") for line in recommended_list.split('\n') if line.strip()]
            st.table(pd.DataFrame(recommended_list_data, columns=['Province','Commodity', 'Unit', 'PricePHP']))
            st.subheader("Total Price: " + str(total_price))
        else:
            st.warning("No items found within the budget.")

    st.header("Get your list in Notion!")
    st.header("Remember to add connection to your Page")
    page_url=st.text_input(label="Enter your Notion Page ID here",value="https://www.notion.so/API-TEST-b7b7540389a84514a3ab6b49215817a9")
    st.button("Save", key="btn2", on_click=notion,args=[page_url,recommended_list])
    

def gsheet():   
    url = "https://docs.google.com/spreadsheets/d/1RiUc_unHWsdjHpAG8mIvMb1GD3_atoSSI_D_cSCCu2k/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url)
    return data

def todolist(page_id,content):
    notion.blocks.children.append(
        **{
            "block_id":page_id,
            "children":[
                {
                    "to_do": 
                    {
                        "rich_text": [{
                            "text": {
                                "content": "Finish Q3 goals",
                            }
                        },],
                        "checked": False,
                        "color": "default",
                    }
                }
            ]
        }
    )

def notion(page_url):
    page_id=(page_url[-32:])
    print(page_id)
   
    notion = Client(auth=os.environ["NOTION_TOKEN"])

    notion.blocks.children.append(
        **{
            "block_id":page_id,
            "children":[
                {
                    "heading_2": {
                        "rich_text": [
                        {
                            "text": {
                                "content": "Shopping List"
                            },
                        },
                        ],
                        "color":"red"
                    },
                },
            ]
        }
    )

    
main_interface()

