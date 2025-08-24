#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from processor import TransactionProcessor
from parser.satispay_parser import SatispayParser
from parser.splitwise_parser import SplitwiseParser
from parser.paypal_parser import PaypalParser

DIRECTORY = "../resources/"
DEFAULT_SPLITWISE_FILE = DIRECTORY + "slitwise.csv"
DEFAULT_PAYPAL_FILE = DIRECTORY + "paypal.csv"
DEFAULT_SATYSPAY_FILE = DIRECTORY + "satispay.xlsx"
DEFAULT_OUTPUT_FILE = "../output/output.csv"
DEFAULT_ONWER = "christian rocchetti"


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process Splitwise and PayPal CSV files")
    
    parser.add_argument('--splitwise', type=str, default=DEFAULT_SPLITWISE_FILE,
                       help=f'Splitwise CSV file (default: {DEFAULT_SPLITWISE_FILE})')
    
    parser.add_argument('--splitwise-onwer', type=str, default=DEFAULT_ONWER,
                       help=f'Splitwise onwe (default: {DEFAULT_ONWER})')
    
    parser.add_argument('--paypal', type=str, default=DEFAULT_PAYPAL_FILE,
                       help=f'PayPal CSV file (default: {DEFAULT_PAYPAL_FILE})')
    
    parser.add_argument('--satispay', type=str, default=DEFAULT_SATYSPAY_FILE,
                       help=f'Satispay CSV file (default: {DEFAULT_SATYSPAY_FILE})')
    
    parser.add_argument('-o', '--output', type=str, default=DEFAULT_OUTPUT_FILE,
                       help=f'Output file (default: {DEFAULT_OUTPUT_FILE})')
    
    parser.add_argument('--skip-splitwise', action='store_true', help='Skip Splitwise processing')
    parser.add_argument('--skip-paypal', action='store_true', help='Skip PayPal processing')
    parser.add_argument('--skip-satispay', action='store_true', help='Skip Satispay processing')
    
    return parser.parse_args()

def validate_files(args):
    files_to_check = []
    
    if not args.skip_splitwise:
        files_to_check.append(('Splitwise', args.splitwise))
    
    if not args.skip_paypal:
        files_to_check.append(('PayPal', args.paypal))

    if not args.skip_satispay:
        files_to_check.append(('Satispay', args.satispay))        
    
    missing_files = []
    for file_type, filepath in files_to_check:
        if not Path(filepath).exists():
            missing_files.append(f"{file_type}: {filepath}")
    
    if missing_files:
        print("Missing files:")
        for missing in missing_files:
            print(f"  - {missing}")
        print("\nContinuing with available files...")

def main():
    try:
        args = parse_arguments()
        validate_files(args)
        
        splitwise_parser_name = 'splitwise'
        paypal_parser_name = 'paypal'
        satispay_parser_name = 'satispay'

        file_mappings = {}
        if not args.skip_splitwise: file_mappings[splitwise_parser_name] = args.splitwise
        if not args.skip_paypal: file_mappings[paypal_parser_name] = args.paypal
        if not args.skip_satispay: file_mappings[satispay_parser_name] = args.satispay
        output_file = args.output
        
        parsers = {
            splitwise_parser_name: SplitwiseParser(args.splitwise_onwer),
            paypal_parser_name: PaypalParser(),
            satispay_parser_name: SatispayParser()
        }
        
        processor = TransactionProcessor(parsers)
        processor.process_files(file_mappings, output_file)
        
        print("Processing completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()