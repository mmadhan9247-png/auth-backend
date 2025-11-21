from flask import Flask, send_from_directory, jsonify
from app import create_app
import os

app = create_app()

# Path to React build folder
BUILD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """
    Serve React frontend files
    """
    # If file exists (like JS, CSS, images), serve it
    if path and os.path.exists(os.path.join(BUILD_PATH, path)):
        return send_from_directory(BUILD_PATH, path)
    
    # Otherwise, always return index.html (React entry point)
    return send_from_directory(BUILD_PATH, "index.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
