import streamlit as st
import pandas as pd
from streamlit_extras.tags import tagger_component
from streamlit_gsheets import GSheetsConnection
import streamlit_scrollable_textbox as stx
from dotenv import load_dotenv
import os
from notion_client import Client

load_dotenv()

def main_interface():
    plaintext = st.text_input(label="Enter your budget amount", value="600")
    budget = int(plaintext)


    st.markdown("---")
    st.header("Local Produce")
    categories = ["canned goods", "dairy products", "meat", "fish", "vegetables", "fruits", "beverages", "snacks", "condiments", "frozen foods", "baking supplies"]
    
    rows = 5
    cols = st.columns(3)
    selected_categories = {}
    for i in range(rows):
        for j in range(3):
            index = i * 3 + j
            if index < len(categories):
                selected_categories[categories[index]] = cols[j].checkbox(categories[index])

    st.button("Submit", key="btn1")

    st.markdown("---")
    st.header("Recommended")
    
    df = gsheet()

    recommended_list = ""
    total_price = 0
    for row in df.itertuples():
        if total_price + int(row.PricePHP) <= budget:
            recommended_list += f"{row.City}  ||  {row.Commodity}  ||  {row.PricePHP}\n"
            total_price += int(row.PricePHP)

    if recommended_list:
        recommended_list_data = [line.split("  ||  ") for line in recommended_list.split('\n') if line.strip()]
        st.table(pd.DataFrame(recommended_list_data, columns=['City', 'Commodity', 'PricePHP']))
    else:
        st.warning("No items found within the budget.")

    #stx.scrollableTextbox(recommended_list, height=300)

    st.subheader("Total Price: " + str(total_price))

    st.header("Get your list in Notion!")
    st.header("Remember to add our integration to your Page")
    page_url=st.text_input(label="Enter your Notion Page ID here",value="https://www.notion.so/API-TEST-b7b7540389a84514a3ab6b49215817a9")
    st.button("Save", key="btn2", on_click=notion,args=[page_url,df])
    
def gsheet():   
    url = "https://docs.google.com/spreadsheets/d/1RiUc_unHWsdjHpAG8mIvMb1GD3_atoSSI_D_cSCCu2k/edit?usp=sharing"
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url)
    return data

def todolist(page_id,notion,commodity,city,price):
    notion.blocks.children.append(
        **{
            "block_id":page_id,
            "children":[
                {
                    "to_do": 
                    {
                        "rich_text": [{
                            "text": {
                                "content": commodity+" "+city+" "+price
                            }
                        },
                        ],
                        "checked": False,
                        "color": "default",
                    }
                }
            ]
        }
    )

def notion(page_url,df):
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

    ctr=0
    for row in df.itertuples():
        if(ctr<20):
            todolist(page_id,notion,str(row.Commodity),str(row.City),str(row.PricePHP))
            ctr+=1
        else:
            break
    
        

def generate():
    pass

main_interface()

