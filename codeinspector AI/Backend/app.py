from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config
import os

# Extensions ko globally declare kar rahe hain taaki dusri files use kar sakein
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable Cross-Origin Resource Sharing for frontend communication
    CORS(app)
    
    # Initialize core tools with app engine context
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Ensure the upload folder exists physically on disk
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Circular imports se bachne ke liye routes ko function ke andar import kiya hai
    from routes.auth import auth_bp
    from routes.upload import upload_bp
    from routes.review import review_bp
    
    # API endpoints blueprints registration
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(upload_bp, url_prefix='/api/code')
    app.register_blueprint(review_bp, url_prefix='/api/review')

    # Tables ko auto-create karne ka check snippet
    with app.app_context():
        db.create_all()

    # Health check route (Testing ke liye)
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "AI Code Review Assistant Full Day-5 Architecture Engine is operational!"
        }), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)