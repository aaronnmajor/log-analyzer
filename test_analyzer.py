#!/usr/bin/env python3
"""
Simple test script to verify the log analyzer functionality.

This script runs basic tests to ensure the analyzer is working correctly.
"""

import tempfile
import os
from conversion_log_analyzer import LogParser, LogAnalyzer, CSVReporter, MarkdownReporter


def test_parser():
    """Test the log parser."""
    print("Testing LogParser...")
    
    test_content = """
2024-01-15 10:00:00 ERROR: Test error
2024-01-15 10:00:01 WARNING: Test warning
2024-01-15 10:00:02 [STEP:TestStep] CRITICAL: Test critical
2024-01-15 10:00:03 INFO: This should be ignored
2024-01-15 10:00:04 [STEP:AnotherStep] ERROR: Another error
"""
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        parser = LogParser()
        entries = list(parser.parse_file(temp_file))
        
        assert len(entries) == 4, f"Expected 4 entries, got {len(entries)}"
        
        # Check levels
        levels = [e.level for e in entries]
        assert 'ERROR' in levels
        assert 'WARNING' in levels
        assert 'CRITICAL' in levels
        
        # Check steps
        steps = [e.step for e in entries if e.step]
        assert len(steps) == 2, f"Expected 2 steps, got {len(steps)}"
        
        print("✓ LogParser tests passed")
        return True
    finally:
        os.unlink(temp_file)


def test_analyzer():
    """Test the log analyzer."""
    print("Testing LogAnalyzer...")
    
    from conversion_log_analyzer.parser import LogEntry
    
    analyzer = LogAnalyzer()
    
    # Add test entries
    entries = [
        LogEntry(1, "ERROR: Test 1", "ERROR", "Step1"),
        LogEntry(2, "ERROR: Test 2", "ERROR", "Step1"),
        LogEntry(3, "WARNING: Test 3", "WARNING", "Step2"),
        LogEntry(4, "CRITICAL: Test 4", "CRITICAL", "Step2"),
    ]
    
    for entry in entries:
        analyzer.add_entry(entry, "test.log")
    
    # Check summary
    summary = analyzer.get_summary()
    assert summary['total_entries'] == 4
    assert summary['level_counts']['ERROR'] == 2
    assert summary['level_counts']['WARNING'] == 1
    assert summary['level_counts']['CRITICAL'] == 1
    
    # Check step grouping
    assert len(summary['steps']) == 2
    assert 'Step1' in summary['steps']
    assert 'Step2' in summary['steps']
    
    print("✓ LogAnalyzer tests passed")
    return True


def test_reporters():
    """Test the report generators."""
    print("Testing Reporters...")
    
    from conversion_log_analyzer.parser import LogEntry
    
    analyzer = LogAnalyzer()
    analyzer.add_entry(LogEntry(1, "ERROR: Test", "ERROR", "TestStep"), "test.log")
    
    summary = analyzer.get_summary()
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test CSV reporter
        csv_reporter = CSVReporter(tmpdir)
        csv_file = csv_reporter.generate_summary_report(summary)
        assert os.path.exists(csv_file), "CSV file not created"
        
        # Test Markdown reporter
        md_reporter = MarkdownReporter(tmpdir)
        md_file = md_reporter.generate_summary_report(summary)
        assert os.path.exists(md_file), "Markdown file not created"
        
        print("✓ Reporter tests passed")
        return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("Running Conversion Log Analyzer Tests")
    print("=" * 50)
    print()
    
    tests = [
        test_parser,
        test_analyzer,
        test_reporters,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
