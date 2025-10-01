"""
CLI Module

Command-line interface for the log analyzer.
"""

import argparse
import os
import sys
from pathlib import Path
from .parser import LogParser
from .analyzer import LogAnalyzer
from .reporter import CSVReporter, MarkdownReporter


def find_log_files(input_path: str) -> list:
    """
    Find all log files in the input path.
    
    Args:
        input_path: File or directory path
        
    Returns:
        List of log file paths
    """
    path = Path(input_path)
    
    if path.is_file():
        return [str(path)]
    elif path.is_dir():
        # Find all .log files and .txt files
        log_files = list(path.glob('*.log')) + list(path.glob('*.txt'))
        return [str(f) for f in log_files]
    else:
        print(f"Error: {input_path} is not a valid file or directory")
        return []


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze log files for ERROR, WARNING, and CRITICAL messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input logs/ --output reports/
  %(prog)s --input conversion.log --output reports/ --format both
  %(prog)s -i logs/ -o reports/ -f markdown
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input log file or directory containing log files'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for reports'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['csv', 'markdown', 'both'],
        default='both',
        help='Report format (default: both)'
    )
    
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Generate detailed reports with log entries'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Find log files
    if args.verbose:
        print(f"Searching for log files in: {args.input}")
    
    log_files = find_log_files(args.input)
    
    if not log_files:
        print("No log files found!")
        sys.exit(1)
    
    if args.verbose:
        print(f"Found {len(log_files)} log file(s):")
        for f in log_files:
            print(f"  - {f}")
    
    # Parse and analyze logs
    print("Parsing log files...")
    log_parser = LogParser()
    analyzer = LogAnalyzer()
    
    for log_file in log_files:
        if args.verbose:
            print(f"Processing: {log_file}")
        
        try:
            for entry in log_parser.parse_file(log_file, encoding=args.encoding):
                analyzer.add_entry(entry, filename=os.path.basename(log_file))
        except Exception as e:
            print(f"Error processing {log_file}: {e}")
    
    # Get summary
    summary = analyzer.get_summary()
    
    print(f"\nAnalysis complete!")
    print(f"Total entries found: {summary['total_entries']}")
    print(f"  CRITICAL: {summary['level_counts'].get('CRITICAL', 0)}")
    print(f"  ERROR: {summary['level_counts'].get('ERROR', 0)}")
    print(f"  WARNING: {summary['level_counts'].get('WARNING', 0)}")
    
    if summary['steps']:
        print(f"  Steps identified: {len(summary['steps'])}")
    
    # Generate reports
    print(f"\nGenerating reports in: {args.output}")
    
    if args.format in ['csv', 'both']:
        csv_reporter = CSVReporter(args.output)
        summary_file = csv_reporter.generate_summary_report(summary)
        print(f"  Created: {summary_file}")
        
        if args.detailed:
            detailed_file = csv_reporter.generate_detailed_report(analyzer)
            print(f"  Created: {detailed_file}")
    
    if args.format in ['markdown', 'both']:
        md_reporter = MarkdownReporter(args.output)
        summary_file = md_reporter.generate_summary_report(summary)
        print(f"  Created: {summary_file}")
        
        if args.detailed:
            detailed_file = md_reporter.generate_detailed_report(analyzer)
            print(f"  Created: {detailed_file}")
    
    print("\nDone!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
