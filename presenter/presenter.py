from model.calculator import Calculator
from model.datamodel import History
from utils.utils import get_current_time
from view.view import View


class Presenter:
    def __init__(self):
        self.calculator = Calculator()
        self.history = History()
        # コンテナをセッション状態として保持することができないため、viewはここでは初期化しない。
        # 重いデータは適宜キャッシュすることで毎回読み込まれることを防ぐ。

    def perform_calculation(self, operator: str, a: float, b: float) -> str:
        if operator == "add":
            result = self.calculator.add(a, b)
        elif operator == "subtract":
            result = self.calculator.subtract(a, b)
        elif operator == "multiply":
            result = self.calculator.multiply(a, b)
        elif operator == "divide":
            result = self.calculator.divide(a, b)
        else:
            result = "Unknown operator"

        if not isinstance(result, str):
            result = f"{result:.2f}"
        return result

    def add_to_history(self, operator: str, a: float, b: float, result: str):
        self.history.add_log(
            time=get_current_time(),
            number1=a,
            number2=b,
            operator=operator,
            result=result,
        )

    def run(self):
        print("Aの読み込み")
        view = View()
        a, b, operator, calc_button = view.input()

        if calc_button:
            result = self.perform_calculation(operator, a, b)
            self.add_to_history(operator, a, b, result)
            view.disp_result(result)

        history = self.history.get_detail()
        view.disp_history(history)
