from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import db
from app.routes import routes

def create_app(database_uri: str = 'sqlite:///user.db') -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(routes)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({'error': 'Internal server error'}), 500

    with app.app_context():
        db.create_all()

    return app