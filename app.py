from flask import Flask
from config import Config
from database import db
from routes.product_routes import product_bp
from routes.restock_routes import restock_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register Blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(restock_bp)

    @app.route("/")
    def home():
        return {
            "message": "Welcome to the Stock Management API 🚀",
            "endpoints": [
                "POST   /product",
                "GET    /product",
                "GET    /product/<id>",
                "PUT    /product/<id>",
                "DELETE /product/<id>",
                "GET    /restock/<id>",
                "PUT    /restock/update/<id>",
                "GET    /restock/list"
            ]
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)
