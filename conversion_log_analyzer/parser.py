"""
Log Parser Module

Handles parsing of log files with regex patterns for ERROR, WARNING, and CRITICAL messages.
Optimized for large files using streaming/chunked processing.
"""

import re
from typing import Iterator, Dict, Optional
from dataclasses import dataclass


@dataclass
class LogEntry:
    """Represents a single log entry"""
    line_number: int
    message: str
    level: str  # ERROR, WARNING, or CRITICAL
    step: Optional[str] = None  # Extracted from [STEP:...] tags


class LogParser:
    """
    Parser for log files that extracts ERROR, WARNING, and CRITICAL messages.
    Supports large files through streaming.
    """
    
    # Regex patterns for log levels
    ERROR_PATTERN = re.compile(r'\bERROR\b', re.IGNORECASE)
    WARNING_PATTERN = re.compile(r'\bWARNING\b', re.IGNORECASE)
    CRITICAL_PATTERN = re.compile(r'\bCRITICAL\b', re.IGNORECASE)
    
    # Pattern for extracting step information
    STEP_PATTERN = re.compile(r'\[STEP:([^\]]+)\]', re.IGNORECASE)
    
    def __init__(self, chunk_size: int = 8192):
        """
        Initialize the parser.
        
        Args:
            chunk_size: Size of chunks for reading files (in bytes)
        """
        self.chunk_size = chunk_size
    
    def parse_file(self, filepath: str, encoding: str = 'utf-8') -> Iterator[LogEntry]:
        """
        Parse a log file and yield LogEntry objects for relevant messages.
        
        Args:
            filepath: Path to the log file
            encoding: File encoding (default: utf-8)
            
        Yields:
            LogEntry objects for ERROR, WARNING, and CRITICAL messages
        """
        try:
            with open(filepath, 'r', encoding=encoding, errors='replace') as f:
                line_number = 0
                for line in f:
                    line_number += 1
                    entry = self._parse_line(line, line_number)
                    if entry:
                        yield entry
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
    
    def _parse_line(self, line: str, line_number: int) -> Optional[LogEntry]:
        """
        Parse a single line and return a LogEntry if it contains ERROR, WARNING, or CRITICAL.
        
        Args:
            line: The log line to parse
            line_number: Line number in the file
            
        Returns:
            LogEntry object or None if the line doesn't match
        """
        level = None
        
        # Check for log level (in order of severity)
        if self.CRITICAL_PATTERN.search(line):
            level = "CRITICAL"
        elif self.ERROR_PATTERN.search(line):
            level = "ERROR"
        elif self.WARNING_PATTERN.search(line):
            level = "WARNING"
        
        if level is None:
            return None
        
        # Extract step information if present
        step = None
        step_match = self.STEP_PATTERN.search(line)
        if step_match:
            step = step_match.group(1).strip()
        
        return LogEntry(
            line_number=line_number,
            message=line.strip(),
            level=level,
            step=step
        )
    
    def parse_multiple_files(self, filepaths: list, encoding: str = 'utf-8') -> Iterator[tuple]:
        """
        Parse multiple log files.
        
        Args:
            filepaths: List of file paths to parse
            encoding: File encoding (default: utf-8)
            
        Yields:
            Tuples of (filepath, LogEntry)
        """
        for filepath in filepaths:
            for entry in self.parse_file(filepath, encoding):
                yield (filepath, entry)
