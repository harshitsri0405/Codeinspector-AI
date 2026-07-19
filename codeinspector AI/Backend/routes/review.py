from flask import Blueprint, jsonify
from app import db
from models.project import Project, Review, ReviewFinding
from services.pylint_service import PylintService
from services.bandit_service import BanditService
from services.radon_service import RadonService
from services.openai_service import AIService
from flask_jwt_extended import jwt_required
import os

review_bp = Blueprint('review', __name__)

@review_bp.route('/analyze/<int:project_id>', methods=['POST'])
@jwt_required()
def run_analysis(project_id):
    project = Project.query.get_or_404(project_id)
    
    from flask import current_app
    filename_snippet = f"snippet_{project.id}.py"
    file_path = None
    
    for file in os.listdir(current_app.config['UPLOAD_FOLDER']):
        if file.startswith(f"{project.id}_") or file == filename_snippet:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file)
            break
            
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Target source file script not found on disk"}), 404

    # 1. Run Static Tools (Day 5 & 6)
    pylint_results = PylintService.analyze_file(file_path)
    bandit_findings = BanditService.analyze_file(file_path)
    radon_metrics = RadonService.analyze_file(file_path)
    
    # Read text for AI submission
    with open(file_path, 'r', encoding='utf-8') as f:
        code_body = f.read()

    # 2. Trigger the Day 8 AI Review Engine Pipeline
    ai_report = AIService.review_code(code_body, os.path.basename(file_path))

    # Calculate final balanced score (Average of Static Pylint Score and AI rating)
    static_score = pylint_results['score'] * 10.0
    ai_score = ai_report.get('score', 80)
    blended_score = round((static_score + ai_score) / 2, 2)

    # 3. Save Master Review Record to Database
    summary_text = f"AI Review Summary: {ai_report.get('summary')}. Maintainability index: {radon_metrics['maintainability_index']}."
    new_review = Review(
        project_id=project.id,
        review_score=blended_score,
        summary=summary_text
    )
    db.session.add(new_review)
    db.session.commit()

    # 4. Save Static Analysis Findings
    for flaw in bandit_findings:
        db.session.add(ReviewFinding(
            review_id=new_review.id,
            severity=flaw['severity'],
            issue=f"[Security] {flaw['issue']}",
            explanation=flaw['explanation'],
            suggestion=flaw['suggestion'],
            file_name=os.path.basename(file_path),
            line_number=flaw['line_number']
        ))

    # 5. Save AI Insights Findings (Bugs, Naming suggestions, Refactoring)
    for ai_finding in ai_report.get('findings', []):
        db.session.add(ReviewFinding(
            review_id=new_review.id,
            severity=ai_finding.get('severity', 'Medium'),
            issue=f"[AI Engine] {ai_finding.get('issue', 'Optimization Opportunity')}",
            explanation=ai_finding.get('explanation', ''),
            suggestion=ai_finding.get('suggestion', ''),
            file_name=os.path.basename(file_path)
        ))
        
    db.session.commit()

    return jsonify({
        "message": "AI & Static Hybrid Code Review Pipeline complete!",
        "review_id": new_review.id,
        "metrics": {
            "overall_score": blended_score,
            "cyclomatic_complexity": radon_metrics['cyclomatic_complexity'],
            "maintainability_index": radon_metrics['maintainability_index'],
            "classes_count": radon_metrics['total_classes'],
            "functions_count": radon_metrics['total_functions']
        }
    }), 200