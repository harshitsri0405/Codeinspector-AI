from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_name = db.Column(db.String(150), nullable=False)
    upload_type = db.Column(db.String(50), nullable=False) # 'file' or 'snippet'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='project', lazy=True, cascade="all, delete-orphan")


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    review_score = db.Column(db.Float, nullable=True) # Score assigned out of 100
    summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    findings = db.relationship('ReviewFinding', backref='review', lazy=True, cascade="all, delete-orphan")


class ReviewFinding(db.Model):
    __tablename__ = 'review_findings'
    
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    severity = db.Column(db.String(50), nullable=False) # 'Low', 'Medium', 'High', 'Critical'
    issue = db.Column(db.String(255), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    suggestion = db.Column(db.Text, nullable=False)
    file_name = db.Column(db.String(255), nullable=True)
    line_number = db.Column(db.Integer, nullable=True)