from flask import Flask
from .extensions import db, migrate, bcrypt, jwt
from .routes.auth import auth_bp
from .routes.protected import protected_bp
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Allow API access from Vercel frontend
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"]}})

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(protected_bp, url_prefix='/api')

    # Root route
    @app.route("/")
    def home():
        return {"status": "Backend running", "message": "API works"}

    return app
