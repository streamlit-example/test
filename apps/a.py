from streamlit import session_state as stss

from presenter.presenter import Presenter
from utils.page_manager import page_urls

page_urls(__file__)

def main():
    if "presenter" not in stss:
        stss.presenter = Presenter()
    
    stss.presenter.run()


main()
