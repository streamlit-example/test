from page_manager.page_urls import page_contents, page_urls
from streamlit_card import card
import streamlit as st

from page_manager.page_urls import PAGES
page_urls(__file__)

"""
### レクチャ用ページ
これはPythonを触ったことがない人向けにStreamlitをレクチャするためのページです。
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
