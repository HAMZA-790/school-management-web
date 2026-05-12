import os
from flask import Flask
from app.web.routes import web_bp

def create_app():
    # Ensure database is initialized for SQLite
    if os.getenv("DB_TYPE") == "sqlite":
        from setup_sqlite import setup_sqlite_database
        setup_sqlite_database()

    app = Flask(__name__, template_folder='app/web/templates', static_folder='app/web/static')
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "super_secret_key_123")
    
    # Register blueprints
    app.register_blueprint(web_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    # When running locally, ensure db type is set to sqlite for testing
    if not os.getenv("DB_TYPE"):
        os.environ["DB_TYPE"] = "sqlite"
        from setup_sqlite import setup_sqlite_database
        setup_sqlite_database()
        
    app.run(debug=True, host="0.0.0.0", port=5000)
