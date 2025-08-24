import csv
from typing import List
from collections import defaultdict
from models import Transaction, BackType

class TransactionFormatter:
    
    MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    def format_transactions(self, transactions: List[Transaction]) -> List[List[str]]:
        grouped = self._group_transactions_by_month(transactions)
        
        sorted_months = self._sort_months(grouped.keys())
        
        formatted_rows = []
        
        for month in sorted_months:
            formatted_rows.append([f"⬜⬜⬜⬜  {month}  ⬜⬜⬜⬜"])
            
            month_transactions = grouped[month]
            
            transaction_types = list(month_transactions.keys())
            
            for i, transaction_type in enumerate(transaction_types):
                transactions_of_type = month_transactions[transaction_type]
                
                for transaction in transactions_of_type:
                    formatted_rows.append(transaction.to_csv_row())
                
                if i < len(transaction_types) - 1 and transactions_of_type:
                    formatted_rows.append([""])
        
        return formatted_rows
    
    def _group_transactions_by_month(self, transactions: List[Transaction]) -> dict:
        grouped = defaultdict(lambda: defaultdict(list))
        
        for transaction in transactions:
            month = transaction.month_name
            grouped[month][transaction.source_type].append(transaction)
        
        return dict(grouped)
    
    def _sort_months(self, months: set) -> List[str]:
        return sorted(months, key=lambda x: self.MONTH_ORDER.index(x))
    
    def write_to_csv(self, formatted_rows: List[List[str]], output_file: str):
        try:
            with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
                writer = csv.writer(outfile, delimiter=";")
                writer.writerows(formatted_rows)
            print(f"Output saved in {output_file}")
        except Exception as e:
            print(f"Errore save file: {e}")
            raise