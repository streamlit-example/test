from typing import List

from pydantic import BaseModel


class Log(BaseModel):
    id: int
    time: str
    number1: float
    number2: float
    operator: str
    result: str

    def get_detail(self) -> str:
        return (
            f"[{self.id:03}] [{self.time}] {self.operator}"
            f"({self.number1:.1f}, {self.number2:.1f}) -> {self.result}"
        )


class History(BaseModel):
    items: List[Log] = []
    id_latest: int = 0

    def add_log(
        self,
        time: str,
        number1: float,
        number2: float,
        operator: str,
        result: str,
    ):
        self.id_latest += 1
        new_log = Log(
            id=self.id_latest,
            time=time,
            number1=number1,
            number2=number2,
            operator=operator,
            result=result,
        )
        # 先頭に新しい要素を追加
        self.items.insert(0, new_log)

    def get_detail(self) -> str:
        return "\n\n".join(item.get_detail() for item in self.items)
