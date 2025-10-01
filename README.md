# Conversion Log Analyzer

A powerful Python tool for parsing and analyzing large log files from data conversions. It searches for ERROR, WARNING, and CRITICAL messages using regex, summarizes their frequency, and groups them by module/step tags. The tool supports both CLI and GUI interfaces and is optimized for huge files (gigabytes).

## Features

- 🔍 **Pattern Matching**: Uses regex to identify ERROR, WARNING, and CRITICAL messages
- 📊 **Frequency Analysis**: Summarizes the count of each error type
- 🏷️ **Step Grouping**: Groups errors by module/step using `[STEP:...]` tags in logs
- 📄 **Multiple Export Formats**: Generates both CSV and Markdown reports
- 💻 **CLI Interface**: Command-line tool for batch processing
- 🖥️ **GUI Interface**: User-friendly graphical interface using tkinter
- ⚡ **Optimized for Large Files**: Streaming/chunked processing for gigabyte-sized log files
- 🔄 **Multi-file Support**: Process entire directories of log files at once

## Installation

### Using pip (recommended)

```bash
pip install -e .
```

### Manual setup

Simply clone the repository and ensure Python 3.6+ is installed. No external dependencies required!

```bash
git clone https://github.com/aaronnmajor/log-analyzer.git
cd log-analyzer
```

## Usage

### Command-Line Interface (CLI)

Basic usage:

```bash
python analyze_logs.py --input logs/ --output reports/
```

Process a single file:

```bash
python analyze_logs.py --input conversion.log --output reports/
```

Generate only CSV reports:

```bash
python analyze_logs.py --input logs/ --output reports/ --format csv
```

Generate detailed reports with all log entries:

```bash
python analyze_logs.py --input logs/ --output reports/ --detailed
```

Full options:

```bash
python analyze_logs.py --help

options:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input log file or directory containing log files
  --output OUTPUT, -o OUTPUT
                        Output directory for reports
  --format {csv,markdown,both}, -f {csv,markdown,both}
                        Report format (default: both)
  --detailed            Generate detailed reports with log entries
  --encoding ENCODING   File encoding (default: utf-8)
  --verbose, -v         Verbose output
```

### Graphical User Interface (GUI)

Launch the GUI:

```bash
python analyze_logs_gui.py
```

The GUI provides:
- File/directory browser for input selection
- Directory browser for output selection
- Report format selection (CSV, Markdown, or both)
- Option for detailed reports
- Real-time output display
- Progress indicator

## Log Format

The analyzer looks for log messages containing:
- `ERROR` (case-insensitive)
- `WARNING` (case-insensitive)
- `CRITICAL` (case-insensitive)

### Step/Module Tagging

To group errors by step or module, include tags in your log messages:

```
2024-01-15 10:23:45 [STEP:DataValidation] ERROR: Invalid format in field 'date'
2024-01-15 10:24:12 [STEP:DataTransform] WARNING: Missing optional field 'description'
2024-01-15 10:25:30 [STEP:DataLoad] CRITICAL: Database connection failed
```

The analyzer will automatically extract the step name and group statistics accordingly.

## Output Reports

### Summary Reports

Summary reports include:
- Total number of entries found
- Count of each error level (CRITICAL, ERROR, WARNING)
- Breakdown by step/module (if tags are present)

### Detailed Reports

Detailed reports include:
- All information from summary reports
- Complete list of log entries with:
  - Line number
  - Filename
  - Step/module
  - Full message text

### Report Formats

#### CSV Format
- Easy to import into spreadsheets (Excel, Google Sheets)
- Machine-readable for further processing
- Separate files for summary and detailed reports

#### Markdown Format
- Human-readable formatted tables
- Perfect for documentation and GitHub
- Can be converted to HTML, PDF, etc.

## Examples

### Example Log File

```
2024-01-15 10:00:00 [STEP:Initialization] INFO: Starting data conversion
2024-01-15 10:00:15 [STEP:DataValidation] WARNING: Field 'phone' has unusual format
2024-01-15 10:01:23 [STEP:DataValidation] ERROR: Required field 'email' is missing in row 145
2024-01-15 10:02:45 [STEP:DataTransform] ERROR: Unable to parse date field in row 289
2024-01-15 10:03:12 [STEP:DataLoad] CRITICAL: Database connection timeout
2024-01-15 10:03:15 [STEP:DataLoad] ERROR: Failed to insert record 456
```

### Example Output

**Summary (Markdown):**

| Level | Count |
|-------|-------|
| CRITICAL | 1 |
| ERROR | 3 |
| WARNING | 1 |

**Errors by Step:**

| Step | CRITICAL | ERROR | WARNING | Total |
|------|----------|-------|---------|-------|
| DataValidation | 0 | 1 | 1 | 2 |
| DataTransform | 0 | 1 | 0 | 1 |
| DataLoad | 1 | 1 | 0 | 2 |

## Performance

The analyzer is optimized for large files:
- **Streaming processing**: Reads files line-by-line without loading entire file into memory
- **Efficient regex**: Compiled patterns for fast matching
- **Scalable**: Successfully tested with multi-gigabyte log files
- **Memory efficient**: Constant memory usage regardless of file size

## Architecture

```
conversion_log_analyzer/
├── __init__.py          # Package initialization
├── parser.py            # LogParser - regex-based log parsing
├── analyzer.py          # LogAnalyzer - statistics and grouping
├── reporter.py          # CSV and Markdown report generation
├── cli.py               # Command-line interface
└── gui.py               # Graphical user interface

analyze_logs.py          # CLI entry point
analyze_logs_gui.py      # GUI entry point
```

## Development

### Running Tests

```bash
# Create sample logs for testing
mkdir -p test_logs
echo '[STEP:Test] ERROR: Test error' > test_logs/test.log
echo '[STEP:Test] WARNING: Test warning' >> test_logs/test.log

# Run the analyzer
python analyze_logs.py --input test_logs/ --output test_reports/
```

### Project Structure

```
.
├── conversion_log_analyzer/    # Main package
│   ├── __init__.py
│   ├── parser.py              # Log parsing with regex
│   ├── analyzer.py            # Statistics and analysis
│   ├── reporter.py            # Report generation
│   ├── cli.py                 # CLI interface
│   └── gui.py                 # GUI interface
├── analyze_logs.py            # CLI launcher
├── analyze_logs_gui.py        # GUI launcher
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies (none needed!)
└── README.md                  # This file
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.