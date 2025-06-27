from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    db_path = '/opt/render/project/src/recipes.db' if os.getenv('RENDER') else os.path.join(os.path.dirname(__file__), 'recipes.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a1b2c3d4e5f6g7h8i9j0')
    
    logger.debug(f"Database path: {db_path}")
    if not os.path.exists(db_path):
        logger.error(f"Database file not found at: {db_path}")
    
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        CORS(app, resources={r"/*": {
            "origins": ["http://localhost:5173", "https://recipes-platform.vercel.app", "*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }})
        
        with app.app_context():
            db.create_all()
            logger.info("Database tables created: %s", db.engine.table_names())
        
        from . import models
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp)
        
        return app
    except Exception as e:
        logger.error(f"Error initializing app: {str(e)}")
        raise