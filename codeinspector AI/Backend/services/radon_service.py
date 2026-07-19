from radon.visitors import ComplexityVisitor
from radon.metrics import mi_visit
import os

class RadonService:
    @staticmethod
    def analyze_file(file_path):
        """
        Performs structural complexity profiling using Radon metrics engine.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            # 1. Compute Cyclomatic Complexity metrics using ComplexityVisitor
            visitor = ComplexityVisitor.from_code(code_content)
            
            total_complexity = 0
            functions_scanned = len(visitor.functions)
            
            for function in visitor.functions:
                total_complexity += function.complexity
                
            avg_complexity = round(total_complexity / functions_scanned, 2) if functions_scanned > 0 else 1.0

            # 2. Compute Maintainability Index metric score (0-100 scale)
            maintainability_score = round(mi_visit(code_content, multi=True), 2)

            return {
                "cyclomatic_complexity": avg_complexity,
                "maintainability_index": maintainability_score,
                "total_functions": functions_scanned,
                "total_classes": len(visitor.classes)
            }
            
        except Exception as e:
            return {
                "cyclomatic_complexity": 1.0,
                "maintainability_index": 50.0,
                "total_functions": 0,
                "total_classes": 0
            }