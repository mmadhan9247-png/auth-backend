from flask import Flask
from .extensions import db, migrate, bcrypt, jwt, cors
from .routes.auth import auth_bp
from .routes.protected import protected_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(protected_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return {'message': 'Flask Auth API is running!'}

    return app