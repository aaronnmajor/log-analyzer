#!/usr/bin/env python3
"""
Main CLI script for conversion log analyzer.

Usage:
    python analyze_logs.py --input logs/ --output reports/
"""

from conversion_log_analyzer.cli import main

if __name__ == '__main__':
    main()
