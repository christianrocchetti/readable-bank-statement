from typing import List, Dict, Optional
from models import Transaction
from parser.parser import TransactionParser
from formatter import TransactionFormatter

class TransactionProcessor:
    def __init__(self, parsers: Dict[str, TransactionParser] = None):
        self.parsers = parsers or {}
        self.formatter = TransactionFormatter()
    
    def process_files(self, file_mappings: Dict[str, str], output_file: str = "output.csv") -> None:
        all_transactions = []
        
        for parser_name, file_path in file_mappings.items():
            if file_path and parser_name in self.parsers:
                transactions = self.parsers[parser_name].parse_file(file_path)
                all_transactions.extend(transactions)
                print(f"Processed {len(transactions)} {parser_name} transactions")
        
        if not all_transactions:
            print("No transactions found.")
            return
        
        formatted_rows = self.formatter.format_transactions(all_transactions)
        self.formatter.write_to_csv(formatted_rows, output_file)
        
        print(f"Total transactions processed: {len(all_transactions)}")
    
    def add_parser(self, name: str, parser: TransactionParser):
        self.parsers[name] = parser
    
    def remove_parser(self, name: str):
        if name in self.parsers:
            del self.parsers[name]
    
    def get_available_parsers(self) -> List[str]:
        return list(self.parsers.keys())
    
    def get_transaction_summary(self, transactions: List[Transaction]) -> dict:
        source_counts = {}
        for transaction in transactions:
            source_type = transaction.source_type.name
            source_counts[source_type] = source_counts.get(source_type, 0) + 1
        
        return {
            'total_transactions': len(transactions),
            'total_amount': sum(t.amount for t in transactions),
            'by_source': source_counts
        }