import csv
from datetime import datetime
from typing import List
from models import Transaction, BackType
from parser.parser import TransactionParser

class PaypalParser(TransactionParser):
    
    def get_source_prefix(self) -> str:
        return "(Paypal)"
    
    def parse_file(self, filepath: str) -> List[Transaction]:
        transactions = []
        
        try:
            with open(filepath, mode="r", encoding="utf-8-sig") as infile:
                reader = csv.DictReader(infile, 
                                      delimiter=',', 
                                      quotechar='"',
                                      skipinitialspace=True)
                rows = list(reader)
            
            for row in rows:
                if self.should_include_transaction(row):
                    transaction = self._create_transaction_from_row(row)
                    transactions.append(transaction)
            
            transactions.sort(key=lambda x: x.date)
            
        except FileNotFoundError:
            print(f"File PayPal {filepath} don't found. Skipped PayPal transaction.")
            return []
        except Exception as e:
            print(f"Error parsing PayPal file: {e}")
            return []
            
        return transactions
    
    def should_include_transaction(self, raw_data: dict) -> bool:
        try:
            lordo_field = raw_data.get("Lordo ", raw_data.get("Lordo", "0"))
            lordo = float(lordo_field.replace(",", "."))
            return lordo < 0
        except (ValueError, KeyError, AttributeError):
            return False
    
    def _create_transaction_from_row(self, row: dict) -> Transaction:
        description = row["Nome"].strip() if row["Nome"].strip() else row["Descrizione"]
        lordo_field = row.get("Lordo ", row.get("Lordo", "0"))
        amount = abs(float(lordo_field.replace(",", ".")))
        date = datetime.strptime(row["Data"], "%d/%m/%Y")
        
        return Transaction(
            description=description,
            amount=amount,
            date=date,
            source_type=BackType.PAYPAL,
            source_prefix=self.get_source_prefix(),
            raw_data=row
        )