"""
Reporter Module

Generates reports in CSV and Markdown formats.
"""

import csv
import os
from datetime import datetime
from typing import Dict, Any


class BaseReporter:
    """Base class for reporters."""
    
    def __init__(self, output_dir: str):
        """
        Initialize the reporter.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_filename(self, prefix: str, extension: str) -> str:
        """
        Generate a filename with timestamp.
        
        Args:
            prefix: Prefix for the filename
            extension: File extension
            
        Returns:
            Full file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"
        return os.path.join(self.output_dir, filename)


class CSVReporter(BaseReporter):
    """Generate CSV reports from log analysis."""
    
    def generate_summary_report(self, summary: Dict[str, Any], filename: str = None) -> str:
        """
        Generate a CSV summary report.
        
        Args:
            summary: Summary data from LogAnalyzer
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to the generated report
        """
        if filename is None:
            filename = self.generate_filename("summary", "csv")
        else:
            filename = os.path.join(self.output_dir, filename)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write overall statistics
            writer.writerow(["Category", "Value"])
            writer.writerow(["Total Entries", summary['total_entries']])
            writer.writerow([])
            
            # Write level counts
            writer.writerow(["Level", "Count"])
            for level in ['CRITICAL', 'ERROR', 'WARNING']:
                count = summary['level_counts'].get(level, 0)
                writer.writerow([level, count])
            writer.writerow([])
            
            # Write step counts if available
            if summary['step_counts']:
                writer.writerow(["Step", "CRITICAL", "ERROR", "WARNING", "Total"])
                for step, counts in sorted(summary['step_counts'].items()):
                    critical = counts.get('CRITICAL', 0)
                    error = counts.get('ERROR', 0)
                    warning = counts.get('WARNING', 0)
                    total = critical + error + warning
                    writer.writerow([step, critical, error, warning, total])
        
        return filename
    
    def generate_detailed_report(self, analyzer, filename: str = None) -> str:
        """
        Generate a detailed CSV report with all entries.
        
        Args:
            analyzer: LogAnalyzer instance
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to the generated report
        """
        if filename is None:
            filename = self.generate_filename("detailed", "csv")
        else:
            filename = os.path.join(self.output_dir, filename)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Level", "Step", "Line Number", "Filename", "Message"])
            
            # Write all entries sorted by level
            for level in ['CRITICAL', 'ERROR', 'WARNING']:
                entries = analyzer.get_entries_by_level(level)
                for entry in entries:
                    writer.writerow([
                        entry['level'],
                        entry.get('step', ''),
                        entry['line_number'],
                        entry.get('filename', ''),
                        entry['message']
                    ])
        
        return filename


class MarkdownReporter(BaseReporter):
    """Generate Markdown reports from log analysis."""
    
    def generate_summary_report(self, summary: Dict[str, Any], filename: str = None) -> str:
        """
        Generate a Markdown summary report.
        
        Args:
            summary: Summary data from LogAnalyzer
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to the generated report
        """
        if filename is None:
            filename = self.generate_filename("summary", "md")
        else:
            filename = os.path.join(self.output_dir, filename)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Log Analysis Summary Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall statistics
            f.write("## Overall Statistics\n\n")
            f.write(f"- **Total Entries:** {summary['total_entries']}\n\n")
            
            # Level counts
            f.write("## Error Level Frequency\n\n")
            f.write("| Level | Count |\n")
            f.write("|-------|-------|\n")
            for level in ['CRITICAL', 'ERROR', 'WARNING']:
                count = summary['level_counts'].get(level, 0)
                f.write(f"| {level} | {count} |\n")
            f.write("\n")
            
            # Step counts if available
            if summary['step_counts']:
                f.write("## Errors by Step/Module\n\n")
                f.write("| Step | CRITICAL | ERROR | WARNING | Total |\n")
                f.write("|------|----------|-------|---------|-------|\n")
                for step, counts in sorted(summary['step_counts'].items()):
                    critical = counts.get('CRITICAL', 0)
                    error = counts.get('ERROR', 0)
                    warning = counts.get('WARNING', 0)
                    total = critical + error + warning
                    f.write(f"| {step} | {critical} | {error} | {warning} | {total} |\n")
                f.write("\n")
        
        return filename
    
    def generate_detailed_report(self, analyzer, filename: str = None, max_entries: int = 100) -> str:
        """
        Generate a detailed Markdown report with sample entries.
        
        Args:
            analyzer: LogAnalyzer instance
            filename: Optional filename (auto-generated if not provided)
            max_entries: Maximum entries per level to include
            
        Returns:
            Path to the generated report
        """
        if filename is None:
            filename = self.generate_filename("detailed", "md")
        else:
            filename = os.path.join(self.output_dir, filename)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Detailed Log Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write entries by level
            for level in ['CRITICAL', 'ERROR', 'WARNING']:
                entries = analyzer.get_entries_by_level(level)
                if not entries:
                    continue
                
                f.write(f"## {level} Messages ({len(entries)} total)\n\n")
                
                # Show first max_entries
                display_entries = entries[:max_entries]
                for entry in display_entries:
                    f.write(f"### Line {entry['line_number']}")
                    if entry.get('filename'):
                        f.write(f" - {entry['filename']}")
                    if entry.get('step'):
                        f.write(f" - [STEP: {entry['step']}]")
                    f.write("\n\n")
                    f.write(f"```\n{entry['message']}\n```\n\n")
                
                if len(entries) > max_entries:
                    f.write(f"*...and {len(entries) - max_entries} more {level} messages*\n\n")
        
        return filename
