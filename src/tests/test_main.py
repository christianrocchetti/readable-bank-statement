import unittest
import tempfile
import os
import sys
from pathlib import Path
import openpyxl
from openpyxl import Workbook
sys.path.insert(0, str(Path(__file__).parent.parent))
from parser.satispay_parser import SatispayParser
from parser.splitwise_parser import SplitwiseParser
from parser.paypal_parser import PaypalParser
from formatter import TransactionFormatter
from processor import TransactionProcessor

class SplitWiseTransformationTest(unittest.TestCase):
    def test_transformation_with_temp_files(self):
        input_file_path = "./tests/resources/splitwise-example.csv"
        output_file_path = "./tests/resources/output-test.csv"
        try:
            parser = SplitwiseParser()
            formatter = TransactionFormatter()
            transactions = parser.parse_file(input_file_path)
            transformed = formatter.format_transactions(transactions)
            formatter.write_to_csv(transformed, output_file_path)
            
            rows = []
            with open(output_file_path, 'r', encoding='utf-8') as file:
                output_content = file.read()
                rows = output_content.splitlines()
            
            self.assertIn("⬜⬜⬜⬜  Apr  ⬜⬜⬜⬜", rows[0])
            self.assertIn("(Split) Cena da mario;;25,00€;Apr", output_content)
            self.assertIn("(Split) spesa;;35,00€;Apr", output_content)
            self.assertIn("(Split) Mercato;;7,50€;May", output_content)
            self.assertIn("⬜⬜⬜⬜  May  ⬜⬜⬜⬜", rows[3])
            self.assertNotIn("Cena da mario 2", output_content)
            
            output_lines = output_content.strip().split('\n')
            split_lines = [line for line in output_lines if "(Split)" in line]
            self.assertEqual(len(split_lines), 3, "You must 3 rows (Split)")
        finally:
            if os.path.exists(output_file_path):
                os.unlink(output_file_path)

class SatispayTransformationTest(unittest.TestCase):
    def test_transformation_with_temp_xlsx_file(self):
        try:
            output_file_path = "./tests/resources/output-test.csv"
            parser = SatispayParser()
            formatter = TransactionFormatter()
            transactions = parser.parse_file("./tests/resources/satispay-example.xlsx")
            transformed = formatter.format_transactions(transactions)
            formatter.write_to_csv(transformed, output_file_path)
            
            with open(output_file_path, 'r', encoding='utf-8') as file:
                output_content = file.read()
                output_lines = output_content.splitlines()
            
            expected_output = [
                '⬜⬜⬜⬜  Apr  ⬜⬜⬜⬜',
                '(Satispay) Bar Rossi;;8,00€;Apr',
                '(Satispay) Bar Rossi;;9,00€;Apr',
                '(Satispay) Bus;;3,70€;Apr',
                '(Satispay) Caffè;;2,00€;Apr',
                '(Satispay) Craft Beers;;12,00€;Apr',
            ]
            print("output_lines", output_lines)
            for i, expected_line in enumerate(expected_output):
                self.assertEqual(output_lines[i], expected_line)
            
            self.assertNotIn("Satispay Top-up", output_content)
        finally:
            if os.path.exists(output_file_path):
                os.unlink(output_file_path)

class PaypalTransformationTest(unittest.TestCase):
    def test_transformation(self):
        input_paypal_file_path = "./tests/resources/paypal-example.csv"
        output_file_path = "./tests/resources/output-test.csv"
        try:
            parser = PaypalParser()
            formatter = TransactionFormatter()
            transactions = parser.parse_file(input_paypal_file_path)
            transformed = formatter.format_transactions(transactions)
            formatter.write_to_csv(transformed, output_file_path)
            
            with open(output_file_path, 'r', encoding='utf-8') as file:
                output_content = file.read()
                rows_paypal = output_content.splitlines()
            
            self.assertIn("⬜⬜⬜⬜  Feb  ⬜⬜⬜⬜", rows_paypal[0])
            self.assertIn("(Paypal) Viaggi Marco Polo SRL;;35,50€;Feb", output_content)
            self.assertIn("(Paypal) Clinica Salute Plus SRL;;75,00€;Feb", output_content)
        finally:
            if os.path.exists(output_file_path):
                os.unlink(output_file_path)

class AcceptanceCriteriaTest(unittest.TestCase):
    def test_transformation_with_temp_files(self):
        output_file_path = "./tests/resources/output-test.csv"
        try:
            parsers = {
                'splitwise': SplitwiseParser(),
                'paypal': PaypalParser(),
                'satispay': SatispayParser()
            }
            processor = TransactionProcessor(parsers)
            file_mappings = {}
            file_mappings['splitwise'] = "./tests/resources/splitwise-example.csv"
            file_mappings['paypal'] = "./tests/resources/paypal-example.csv"
            file_mappings['satispay'] = "./tests/resources/satispay-example.xlsx"
            
            processor.process_files(
                file_mappings=file_mappings,
                output_file=output_file_path
            )
            
            rows_paypal = []
            with open(output_file_path, 'r', encoding='utf-8') as file:
                output_content = file.read()
                output_lines = output_content.strip().split('\n')
            
            expected_output = [
                '⬜⬜⬜⬜  Feb  ⬜⬜⬜⬜',
                '(Paypal) Viaggi Marco Polo SRL;;35,50€;Feb',
                '(Paypal) Clinica Salute Plus SRL;;75,00€;Feb',
                '⬜⬜⬜⬜  Apr  ⬜⬜⬜⬜',
                '(Split) Cena da mario;;25,00€;Apr',
                '(Split) spesa;;35,00€;Apr',
                '""',
                '(Paypal) Elettronica Moderna SPA;;89,20€;Apr',
                '(Paypal) Energia Verde SpA;;58,90€;Apr',
                '""',
                '(Satispay) Bar Rossi;;8,00€;Apr',
                '(Satispay) Bar Rossi;;9,00€;Apr',
                '(Satispay) Bus;;3,70€;Apr',
                '(Satispay) Caffè;;2,00€;Apr',
                '(Satispay) Craft Beers;;12,00€;Apr',
                '⬜⬜⬜⬜  May  ⬜⬜⬜⬜',
                '(Split) Mercato;;7,50€;May',
                '""',
                '(Paypal) Mario Rossi;;18,50€;May',
                '(Paypal) Clinica Salute Plus SRL;;75,00€;May'
            ]
            
            self.assertEqual(len(output_lines), len(expected_output))
            
            for i, expected_line in enumerate(expected_output):
                self.assertEqual(output_lines[i], expected_line)
        finally:
            if os.path.exists(output_file_path):
                os.unlink(output_file_path)

if __name__ == '__main__':
    unittest.main()