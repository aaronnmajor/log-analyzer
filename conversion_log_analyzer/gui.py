"""
GUI Module

Graphical user interface for the log analyzer using tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
from .parser import LogParser
from .analyzer import LogAnalyzer
from .reporter import CSVReporter, MarkdownReporter


class LogAnalyzerGUI:
    """GUI application for log analysis."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Conversion Log Analyzer")
        self.root.geometry("900x700")
        
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.format_var = tk.StringVar(value="both")
        self.detailed_var = tk.BooleanVar(value=False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Conversion Log Analyzer", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input selection
        ttk.Label(main_frame, text="Input (File/Directory):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.input_path).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5
        )
        ttk.Button(main_frame, text="Browse...", command=self.browse_input).grid(
            row=1, column=2, sticky=tk.W, pady=5
        )
        
        # Output selection
        ttk.Label(main_frame, text="Output Directory:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.output_path).grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5
        )
        ttk.Button(main_frame, text="Browse...", command=self.browse_output).grid(
            row=2, column=2, sticky=tk.W, pady=5
        )
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Format selection
        ttk.Label(options_frame, text="Report Format:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        format_frame = ttk.Frame(options_frame)
        format_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(
            format_frame, text="CSV", variable=self.format_var, value="csv"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            format_frame, text="Markdown", variable=self.format_var, value="markdown"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            format_frame, text="Both", variable=self.format_var, value="both"
        ).pack(side=tk.LEFT, padx=5)
        
        # Detailed report checkbox
        ttk.Checkbutton(
            options_frame, 
            text="Generate detailed reports", 
            variable=self.detailed_var
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Analyze button
        self.analyze_btn = ttk.Button(
            main_frame, 
            text="Analyze Logs", 
            command=self.analyze_logs,
            style='Accent.TButton'
        )
        self.analyze_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=300
        )
        self.progress.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Output text area
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            height=15, 
            wrap=tk.WORD,
            state='disabled'
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear button
        ttk.Button(
            main_frame, 
            text="Clear Output", 
            command=self.clear_output
        ).grid(row=7, column=0, columnspan=3, pady=5)
    
    def browse_input(self):
        """Browse for input file or directory."""
        path = filedialog.askdirectory(title="Select Log Directory")
        if not path:
            path = filedialog.askopenfilename(
                title="Select Log File",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
        if path:
            self.input_path.set(path)
    
    def browse_output(self):
        """Browse for output directory."""
        path = filedialog.askdirectory(title="Select Output Directory")
        if path:
            self.output_path.set(path)
    
    def log_message(self, message):
        """Add a message to the output text area."""
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)
        self.output_text.configure(state='disabled')
        self.root.update_idletasks()
    
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state='disabled')
    
    def find_log_files(self, input_path):
        """Find all log files in the input path."""
        path = Path(input_path)
        
        if path.is_file():
            return [str(path)]
        elif path.is_dir():
            log_files = list(path.glob('*.log')) + list(path.glob('*.txt'))
            return [str(f) for f in log_files]
        else:
            return []
    
    def analyze_logs(self):
        """Analyze the selected log files."""
        # Validate inputs
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input file or directory")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        # Disable button and start progress
        self.analyze_btn.configure(state='disabled')
        self.progress.start(10)
        self.clear_output()
        
        # Run analysis in separate thread
        thread = threading.Thread(target=self._run_analysis)
        thread.daemon = True
        thread.start()
    
    def _run_analysis(self):
        """Run the analysis (called in separate thread)."""
        try:
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            
            self.log_message(f"Searching for log files in: {input_path}")
            
            # Find log files
            log_files = self.find_log_files(input_path)
            
            if not log_files:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", "No log files found!"
                ))
                return
            
            self.log_message(f"Found {len(log_files)} log file(s)")
            for f in log_files:
                self.log_message(f"  - {os.path.basename(f)}")
            
            # Parse and analyze
            self.log_message("\nParsing log files...")
            log_parser = LogParser()
            analyzer = LogAnalyzer()
            
            for log_file in log_files:
                self.log_message(f"Processing: {os.path.basename(log_file)}")
                
                try:
                    for entry in log_parser.parse_file(log_file):
                        analyzer.add_entry(entry, filename=os.path.basename(log_file))
                except Exception as e:
                    self.log_message(f"Error processing {log_file}: {e}")
            
            # Get summary
            summary = analyzer.get_summary()
            
            self.log_message(f"\nAnalysis complete!")
            self.log_message(f"Total entries found: {summary['total_entries']}")
            self.log_message(f"  CRITICAL: {summary['level_counts'].get('CRITICAL', 0)}")
            self.log_message(f"  ERROR: {summary['level_counts'].get('ERROR', 0)}")
            self.log_message(f"  WARNING: {summary['level_counts'].get('WARNING', 0)}")
            
            if summary['steps']:
                self.log_message(f"  Steps identified: {len(summary['steps'])}")
            
            # Generate reports
            self.log_message(f"\nGenerating reports in: {output_path}")
            
            report_format = self.format_var.get()
            detailed = self.detailed_var.get()
            
            if report_format in ['csv', 'both']:
                csv_reporter = CSVReporter(output_path)
                summary_file = csv_reporter.generate_summary_report(summary)
                self.log_message(f"  Created: {os.path.basename(summary_file)}")
                
                if detailed:
                    detailed_file = csv_reporter.generate_detailed_report(analyzer)
                    self.log_message(f"  Created: {os.path.basename(detailed_file)}")
            
            if report_format in ['markdown', 'both']:
                md_reporter = MarkdownReporter(output_path)
                summary_file = md_reporter.generate_summary_report(summary)
                self.log_message(f"  Created: {os.path.basename(summary_file)}")
                
                if detailed:
                    detailed_file = md_reporter.generate_detailed_report(analyzer)
                    self.log_message(f"  Created: {os.path.basename(detailed_file)}")
            
            self.log_message("\nDone!")
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                "Log analysis completed successfully!\nReports have been generated."
            ))
            
        except Exception as e:
            self.log_message(f"\nError: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror(
                "Error", 
                f"An error occurred during analysis:\n{str(e)}"
            ))
        
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self._finish_analysis)
    
    def _finish_analysis(self):
        """Finish the analysis (called from main thread)."""
        self.progress.stop()
        self.analyze_btn.configure(state='normal')


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = LogAnalyzerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
