import csv
from datetime import datetime
from typing import List
from models import Transaction, BackType
from parser.parser import TransactionParser

class SplitwiseParser(TransactionParser):
    def __init__(self, name_onwer = "christian rocchetti"):
        self.name_onwer = name_onwer


    def get_source_prefix(self) -> str:
        return "(Split)"
    
    def parse_file(self, filepath: str) -> List[Transaction]:
        transactions = []
        
        try:
            with open(filepath, mode="r", encoding="utf-8") as infile:
                reader = csv.DictReader(infile)
                rows = list(reader)
            
            rows.sort(key=lambda x: x["Data"])
            
            for row in rows:
                if self.should_include_transaction(row):
                    transaction = self.__create_transaction_from_row(row)
                    transactions.append(transaction)
                    
        except FileNotFoundError:
            print(f"File Splitwise {filepath} don't found. Skipped Splitwise transaction.")
            return []
        except Exception as e:
            print(f"Errore parsing Splitwise file: {e}")
            return []
            
        return transactions
    
    def should_include_transaction(self, raw_data: dict) -> bool:
        try:            
            return self.__not_include_if_christian_all_paid(raw_data)
        except (ValueError, KeyError):
            return False

    def __not_include_if_christian_all_paid(self, raw_data) -> bool:
        price_total = float(raw_data["Costo"])
        christian_price = float(raw_data[self.name_onwer])
        price_total_round = int(round(price_total * 100))
        christian_price_round = int(round(christian_price * 100))
        return not (christian_price_round > 0 and christian_price_round == price_total_round)
    
    def __create_transaction_from_row(self, row: dict) -> Transaction:
        description = row["Descrizione"]
        amount = abs(float(row[self.name_onwer]))
        date = datetime.strptime(row["Data"], "%Y-%m-%d")
        
        return Transaction(
            description=description,
            amount=amount,
            date=date,
            source_type=BackType.SPLITWISE,
            source_prefix=self.get_source_prefix(),
            raw_data=row
        )