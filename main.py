import streamlit as st

from utils.page_manager import PAGES

st.set_page_config(layout="wide")


pages = {
    "Home": [
        st.Page(PAGES.file, title=PAGES.title, icon=PAGES.icon),
    ]
}
for pp in PAGES.children:  # type: ignore
    pages[pp.title] = [st.Page(pp.file, title=pp.title, icon=pp.icon)]
    pages[pp.title] += [
        st.Page(p.file, title=p.title, icon=p.icon) for p in pp.children
    ]

pg = st.navigation(pages, position="hidden")


pg.run()
