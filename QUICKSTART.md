# Quick Start Guide

Get started with the Conversion Log Analyzer in 3 easy steps!

## Installation

```bash
# Clone the repository
git clone https://github.com/aaronnmajor/log-analyzer.git
cd log-analyzer

# Install the package (optional)
pip install -e .
```

## Basic Usage

### Option 1: Command Line (Quick)

```bash
# Analyze logs in a directory
python analyze_logs.py --input logs/ --output reports/

# Or use the installed command
analyze-logs --input logs/ --output reports/
```

### Option 2: GUI (Visual)

```bash
python analyze_logs_gui.py
```

Then use the graphical interface to:
1. Click "Browse" to select your log file or directory
2. Click "Browse" to select where to save reports
3. Choose your report format (CSV, Markdown, or Both)
4. Click "Analyze Logs"

## Try the Example

```bash
# Run the example analysis
python analyze_logs.py --input examples/sample.log --output example_reports/ --detailed

# Check the generated reports
ls example_reports/
```

## Log Format

Your logs should contain messages with ERROR, WARNING, or CRITICAL:

```
2024-01-15 10:00:00 ERROR: Something went wrong
2024-01-15 10:00:01 WARNING: Be careful
2024-01-15 10:00:02 [STEP:DataLoad] CRITICAL: System failure
```

The `[STEP:...]` tag is optional but allows grouping of errors by module/step.

## What You Get

The analyzer generates:
- **Summary reports**: Overview of error counts by type and step
- **Detailed reports**: Complete list of all errors with line numbers
- **CSV format**: For spreadsheet analysis
- **Markdown format**: For documentation

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Look at [examples/](examples/) for code samples
- Run `python analyze_logs.py --help` for CLI options

## Common Commands

```bash
# Analyze with verbose output
python analyze_logs.py -i logs/ -o reports/ --verbose

# Generate detailed reports
python analyze_logs.py -i logs/ -o reports/ --detailed

# CSV format only
python analyze_logs.py -i logs/ -o reports/ --format csv

# Markdown format only
python analyze_logs.py -i logs/ -o reports/ --format markdown

# Both formats (default)
python analyze_logs.py -i logs/ -o reports/ --format both
```

That's it! You're ready to analyze your conversion logs! 🚀
