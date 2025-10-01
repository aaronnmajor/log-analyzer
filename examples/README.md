# Examples

This directory contains example scripts and sample log files to help you get started with the Conversion Log Analyzer.

## Files

- `basic_usage.py` - Demonstrates programmatic usage of the analyzer
- `sample.log` - Sample log file with various error types and step tags

## Running the Examples

### Using the CLI

```bash
# From the repository root
python analyze_logs.py --input examples/sample.log --output examples/reports/
```

### Using the GUI

```bash
# From the repository root
python analyze_logs_gui.py
# Then select examples/sample.log as input
```

### Using the Python API

```bash
cd examples
python basic_usage.py
```

## Sample Log Format

The `sample.log` file demonstrates the expected format:

```
2024-01-15 10:00:00 [STEP:Initialization] INFO: Starting data conversion process
2024-01-15 10:00:15 [STEP:DataValidation] WARNING: Field 'phone' has unusual format
2024-01-15 10:01:23 [STEP:DataValidation] ERROR: Required field 'email' is missing
```

Key features:
- Timestamps (optional)
- `[STEP:StepName]` tags for grouping (optional)
- Log levels: ERROR, WARNING, CRITICAL (case-insensitive)
- Descriptive messages
