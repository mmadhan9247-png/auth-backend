from flask import Flask, send_from_directory
from .extensions import db, migrate, bcrypt, jwt, cors
from .routes.auth import auth_bp
from .routes.protected import protected_bp
from config import Config
import os

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

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        build_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "build")
        )
        file_path = os.path.join(build_path, path)

        if path != "" and os.path.exists(file_path):
            return send_from_directory(build_path, path)

        return send_from_directory(build_path, "index.html")

    return app
