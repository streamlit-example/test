from page_manager.page_urls import page_urls

page_urls(__file__)
import streamlit as st

st.sidebar.markdown("BBB sidebar")

"""
### ワイヤーフレーム制作
以下を題材に、Streamlitでワイヤーフレームを制作するための基本的な方法について紹介します。

- ソースコード: [streamlit-example / wireframe-example](https://github.com/streamlit-example/wireframe-example/)
- アプリ: [Wireframe Sample](https://wireframe-example-rammpl3kzfse7okypdcutk.streamlit.app/)
"""
print("Bの読み込み")

st.button(":material/drive_folder_upload:",help="upload files")
st.checkbox(":material/edit:",help="edit data")
st.toggle(":material/edit:",help="edit data",label_visibility ="collapsed")