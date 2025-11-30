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

    # Ensure database tables exist (e.g., users table) so registration works
    with app.app_context():
        db.create_all()

    # Allow API access from Vercel frontend
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                    r"https://auth-frontend-ggah.*\.vercel\.app",
                ]
            }
        },
    )

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(protected_bp, url_prefix='/api')

    # Root route
    @app.route("/")
    def home():
        return {"status": "Backend running", "message": "API works"}

    return app
