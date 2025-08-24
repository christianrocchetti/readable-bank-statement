import csv
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from models import Transaction, BackType

class TransactionParser(ABC):
    
    @abstractmethod
    def parse_file(self, filepath: str) -> List[Transaction]:
        pass
    
    @abstractmethod
    def should_include_transaction(self, raw_data: dict) -> bool:
        pass
    
    @abstractmethod
    def get_source_prefix(self) -> str:
        pass

