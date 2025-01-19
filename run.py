from flask import Flask
from app.routes import app  # Import your Flask app instance from routes.py

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
