"""
Log Analyzer Module

Analyzes parsed log entries and generates statistics.
"""

from collections import defaultdict
from typing import List, Dict, Any
from .parser import LogEntry


class LogAnalyzer:
    """
    Analyzes log entries and produces summary statistics.
    """
    
    def __init__(self):
        """Initialize the analyzer with empty statistics."""
        self.reset()
    
    def reset(self):
        """Reset all statistics."""
        self.total_entries = 0
        self.level_counts = defaultdict(int)
        self.step_counts = defaultdict(lambda: defaultdict(int))
        self.entries_by_level = defaultdict(list)
        self.entries_by_step = defaultdict(list)
    
    def add_entry(self, entry: LogEntry, filename: str = None):
        """
        Add a log entry to the analysis.
        
        Args:
            entry: LogEntry object to analyze
            filename: Optional filename for tracking
        """
        self.total_entries += 1
        
        # Count by level
        self.level_counts[entry.level] += 1
        
        # Store entry with filename
        entry_data = {
            'line_number': entry.line_number,
            'message': entry.message,
            'level': entry.level,
            'step': entry.step,
            'filename': filename
        }
        
        self.entries_by_level[entry.level].append(entry_data)
        
        # Count and store by step if present
        if entry.step:
            self.step_counts[entry.step][entry.level] += 1
            self.entries_by_step[entry.step].append(entry_data)
    
    def analyze_entries(self, entries: List[LogEntry], filename: str = None):
        """
        Analyze a list of log entries.
        
        Args:
            entries: List of LogEntry objects
            filename: Optional filename for tracking
        """
        for entry in entries:
            self.add_entry(entry, filename)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the analysis.
        
        Returns:
            Dictionary containing analysis summary
        """
        return {
            'total_entries': self.total_entries,
            'level_counts': dict(self.level_counts),
            'step_counts': {
                step: dict(counts) 
                for step, counts in self.step_counts.items()
            },
            'steps': list(self.step_counts.keys())
        }
    
    def get_level_frequency(self) -> Dict[str, int]:
        """
        Get the frequency count of each error level.
        
        Returns:
            Dictionary mapping level to count
        """
        return dict(self.level_counts)
    
    def get_step_frequency(self) -> Dict[str, Dict[str, int]]:
        """
        Get the frequency count of errors grouped by step.
        
        Returns:
            Dictionary mapping step to level counts
        """
        return {
            step: dict(counts)
            for step, counts in self.step_counts.items()
        }
    
    def get_entries_by_level(self, level: str) -> List[Dict]:
        """
        Get all entries for a specific level.
        
        Args:
            level: The log level (ERROR, WARNING, CRITICAL)
            
        Returns:
            List of entry dictionaries
        """
        return self.entries_by_level.get(level, [])
    
    def get_entries_by_step(self, step: str) -> List[Dict]:
        """
        Get all entries for a specific step.
        
        Args:
            step: The step name
            
        Returns:
            List of entry dictionaries
        """
        return self.entries_by_step.get(step, [])
