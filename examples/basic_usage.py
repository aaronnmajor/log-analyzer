#!/usr/bin/env python3
"""
Basic usage example for the Conversion Log Analyzer.

This script demonstrates how to use the log analyzer programmatically.
"""

from conversion_log_analyzer import LogParser, LogAnalyzer, CSVReporter, MarkdownReporter


def main():
    # Initialize components
    parser = LogParser()
    analyzer = LogAnalyzer()
    
    # Define your log files
    log_files = [
        'conversion.log',
        'database.log',
    ]
    
    # Parse each file and analyze
    print("Parsing log files...")
    for log_file in log_files:
        try:
            for entry in parser.parse_file(log_file):
                analyzer.add_entry(entry, filename=log_file)
            print(f"✓ Processed {log_file}")
        except FileNotFoundError:
            print(f"✗ File not found: {log_file}")
        except Exception as e:
            print(f"✗ Error processing {log_file}: {e}")
    
    # Get summary statistics
    summary = analyzer.get_summary()
    
    print(f"\nAnalysis Results:")
    print(f"  Total entries: {summary['total_entries']}")
    print(f"  CRITICAL: {summary['level_counts'].get('CRITICAL', 0)}")
    print(f"  ERROR: {summary['level_counts'].get('ERROR', 0)}")
    print(f"  WARNING: {summary['level_counts'].get('WARNING', 0)}")
    
    if summary['steps']:
        print(f"  Steps found: {', '.join(summary['steps'])}")
    
    # Generate reports
    output_dir = 'reports'
    
    # CSV reports
    csv_reporter = CSVReporter(output_dir)
    csv_summary = csv_reporter.generate_summary_report(summary)
    csv_detailed = csv_reporter.generate_detailed_report(analyzer)
    
    # Markdown reports
    md_reporter = MarkdownReporter(output_dir)
    md_summary = md_reporter.generate_summary_report(summary)
    md_detailed = md_reporter.generate_detailed_report(analyzer)
    
    print(f"\nReports generated in '{output_dir}/' directory:")
    print(f"  - {csv_summary}")
    print(f"  - {csv_detailed}")
    print(f"  - {md_summary}")
    print(f"  - {md_detailed}")


if __name__ == '__main__':
    main()
