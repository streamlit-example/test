import streamlit as st


class View:
    def __init__(self):
        # set layout
        st.title("Calc App (Sample of MVP Architecture)")
        self.container_num1 = st.empty()
        self.container_num2 = st.empty()
        self.container_selectbox = st.empty()
        self.container_button = st.empty()
        st.divider()
        cols = st.columns([1, 3])
        cols[0].subheader("Result")
        self.container_result = cols[0].empty()

        cols[1].subheader("Calculation History")
        self.container_history = cols[1].empty()

    def input(self) -> tuple[float, float, str, bool]:
        a: float = self.container_num1.number_input("Enter first number", value=0)
        b: float = self.container_num2.number_input("Enter second number", value=0)
        operator: str = self.container_selectbox.selectbox(
            "Choose an operator", ["add", "subtract", "multiply", "divide"]
        )
        button: bool = self.container_button.button("Calculate")

        return a, b, operator, button

    def disp_result(self, result: float | str):
        self.container_result.markdown(result)

    def disp_history(self, history: str):
        self.container_history.markdown(history)
