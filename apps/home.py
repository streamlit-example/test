import streamlit as st
from streamlit_card import card

from utils.page_manager import PAGES, page_contents, page_urls

page_urls(__file__)

"""
# テストページ
"""
cols=st.columns(2)
with cols[0]:
    card(
    title="to B",
    text="hoge",
    image="http://placekitten.com/200/300",
    url="http://localhost:8501/b",
    styles={
        "card": {
            "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
            "height": "300px", # <- if you want to set the card height to 300px
            "target": "_self"
            }
        }
    )
with cols[1]:
    card(
    title="to C",
    text="hoge",
    image="http://placekitten.com/200/300",
    url=".../c",
    styles={
        "card": {
            "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
            "height": "300px" # <- if you want to set the card height to 300px
            }
        }
    )

page_contents()
