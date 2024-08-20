import os
from dataclasses import dataclass, field
from typing import List, Optional

import streamlit as st


@dataclass
class Page:
    file: str
    title: str
    category: Optional[str] = None
    icon: Optional[str] = None
    children: Optional[List] = field(default_factory=list)


PAGES = Page(
    file="apps/home.py",
    title="Home",
    icon="🏠",
    children=[
        Page(
            file="apps/a.py",
            title="A",
            icon=":material/search:",
            category="a",
        ),
        Page(
            file="apps/b.py",
            title="B",
            icon="🖼️",
            category="b",
        ),
        Page(
            file="apps/c.py",
            title="C",
            icon=":material/refresh:",
            category="c",
        ),
    ],
)


def page_urls(opened_file):
    opened_file = os.path.basename(opened_file).split(".")[0]
    with st.sidebar:
        with st.popover("Menu"):
            st.page_link(PAGES.file, label=PAGES.title)

            for pp in PAGES.children:
                st.page_link(pp.file, label=pp.title, icon=pp.icon)


def page_contents():
    st.markdown("### Contents:material/search:")
    disp_ = ""
    for pp in PAGES.children:
        disp_ += f"- :material/search: {pp.title}\n"
        for p in pp.children:
            disp_ += f"  - {p.title}\n\n"

    st.markdown(disp_)
