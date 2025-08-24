from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class BackType(Enum):
    SPLITWISE = 1
    PAYPAL = 2
    SATISPAY = 3

@dataclass
class Transaction:
    description: str
    amount: float
    date: datetime
    source_type: BackType
    source_prefix: str 
    raw_data: dict = None
    
    @property
    def month_name(self) -> str:
        month_map = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
            5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
            9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }
        return month_map[self.date.month]
    
    def format_amount(self) -> str:
        return f"{abs(self.amount):.2f}€".replace(".", ",")
    
    def to_csv_row(self) -> list:
        return [f"{self.source_prefix} {self.description}", "", self.format_amount(), self.month_name]