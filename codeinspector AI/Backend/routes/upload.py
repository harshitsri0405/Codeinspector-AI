from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from app import db
from models.project import Project, Review
from flask_jwt_extended import jwt_required, get_jwt_identity

upload_bp = Blueprint('upload', __name__)

# Allowed code file formats specified in the project stack
ALLOWED_EXTENSIONS = {'py', 'js', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_code():
    current_user_id = get_jwt_identity()
    
    # Check if the user is submitting a pasted code snippet
    if 'snippet' in request.json if request.is_json else False:
        data = request.get_json()
        project_name = data.get('project_name', 'Pasted Snippet')
        snippet_content = data.get('snippet')
        
        if not snippet_content:
            return jsonify({"error": "Snippet content cannot be empty"}), 400
            
        # 1. Save to Database
        new_project = Project(user_id=int(current_user_id), project_name=project_name, upload_type='snippet')
        db.session.add(new_project)
        db.session.commit()
        
        # 2. Save snippet as a physical file on disk for static analysis tools
        from flask import current_app
        filename = f"snippet_{new_project.id}.py"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(snippet_content)
            
        return jsonify({
            "message": "Snippet submitted successfully!",
            "project_id": new_project.id,
            "file_path": file_path
        }), 201

    # Check if the user is uploading a physical file instead
    if 'file' not in request.files:
        return jsonify({"error": "No file or snippet provided"}), 400
        
    file = request.files['file']
    project_name = request.form.get('project_name', file.filename)
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        from flask import current_app
        filename = secure_filename(file.filename)
        
        # 1. Create a database record
        new_project = Project(user_id=int(current_user_id), project_name=project_name, upload_type='file')
        db.session.add(new_project)
        db.session.commit()
        
        # 2. Save file physically to the uploads directory
        # Prepend project ID to prevent filename conflicts
        unique_filename = f"{new_project.id}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        return jsonify({
            "message": "File uploaded successfully!",
            "project_id": new_project.id,
            "file_path": file_path
        }), 201
        
    return jsonify({"error": "Unsupported file extension format"}), 400