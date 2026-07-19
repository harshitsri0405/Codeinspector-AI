import sys
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import io
import re

class PylintService:
    @staticmethod
    def analyze_file(file_path):
        """
        Executes a programmatic Pylint scan on a target source file
        and extracts structural feedback alongside a raw quality score.
        """
        # Capture stdout to read the report directly in memory
        pylint_output = io.StringIO()
        reporter = TextReporter(pylint_output)
        
        try:
            # Run Pylint on the target script file
            # --disable=R to skip extreme style metrics for baseline optimization
            Run([file_path, '--disable=R'], reporter=reporter, exit=False)
        except Exception as e:
            return {
                "score": 0.0,
                "raw_output": f"Pylint execution failure: {str(e)}",
                "findings": []
            }
            
        raw_report = pylint_output.getvalue()
        
        # Parse Pylint's score syntax using regex matching (e.g., "Your code has been rated at 8.50/10")
        score_match = re.search(r"rated at (-?\d+\.\d+)/10", raw_report)
        extracted_score = float(score_match.group(1)) if score_match else 0.0
        
        # Re-map negative values cleanly to absolute positive baselines
        if extracted_score < 0:
            extracted_score = 0.0
            
        # Parse individual specific findings line by line
        findings = []
        lines = raw_report.split('\n')
        for line in lines:
            # Check for standard Pylint message formats: file.py:line: [category(symbol), function] message
            if ":" in line and ("[" in line or "]" in line):
                findings.append(line.strip())
                
        return {
            "score": round(extracted_score, 2),
            "raw_output": raw_report,
            "findings": findings
        }