import os
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def main_interface():
    df = gsheet() 
    col1, col2 = st.columns([1, 2]) 

    with col1:
        st.image("Asset/lokalista_logo.png", width=150)
        
    with col2:
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

        recommended_items = []
        total_price = 0
        for row in filtered_df.itertuples():
            if total_price + int(row.PricePHP) <= budget:
                recommended_items.append([row.Province, row.Commodity, row.Unit, row.PricePHP])
                total_price += int(row.PricePHP)
        
        if recommended_items:
            recommended_df = pd.DataFrame(recommended_items, columns=["Province", "Commodity", "Unit", "Price (PHP)"])
            st.table(recommended_df)
        else:
            st.write("No items within budget.")


    st.header("Get your list in Notion!")
    st.write("Remember to add our integration to your Page")
    page_url = st.text_input(label="Enter your Notion Page ID here", value="https://www.notion.so/API-TEST-b7b7540389a84514a3ab6b49215817a9")
    st.button("Save", key="btn2", on_click=notion, args=[page_url, df])


def gsheet():   
    url = "https://docs.google.com/spreadsheets/d/1RiUc_unHWsdjHpAG8mIvMb1GD3_atoSSI_D_cSCCu2k/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url)
    return data


def todolist(page_id, notion, commodity, city, price):
    notion.blocks.children.append(
        **{
            "block_id": page_id,
            "children": [
                {
                    "to_do": {
                        "rich_text": [{
                            "text": {
                                "content": f"{commodity} {city} {price}"
                            }
                        }],
                        "checked": False,
                        "color": "default",
                    }
                }
            ]
        }
    )


def notion(page_url, df):
    page_id = page_url[-32:]
    print(page_id)
   
    notion_client = Client(auth=os.environ["NOTION_TOKEN"])

    notion_client.blocks.children.append(
        **{
            "block_id": page_id,
            "children": [
                {
                    "heading_2": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": "Shopping List"
                                },
                            },
                        ],
                        "color": "red"
                    },
                },
            ]
        }
    )

    ctr = 0
    for row in df.itertuples():
        if ctr < 20:
            todolist(page_id, notion_client, str(row.Commodity), str(row.City), str(row.PricePHP))
            ctr += 1
        else:
            break


def generate():
    pass

main_interface()
