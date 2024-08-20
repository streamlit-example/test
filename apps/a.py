from streamlit import session_state as stss

from presenter.presenter import Presenter
from page_manager.page_urls import page_urls

page_urls(__file__)

def main():
    if "presenter" not in stss:
        stss.presenter = Presenter()
    
    stss.presenter.run()


main()
