import os
from pathlib import Path
from flask import Flask
from app.models import db
from app.routes import routes

app = Flask(__name__, instance_relative_config=True)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)

env = os.getenv('APP_ENV', 'dev').lower()

db_name = 'test.db' if env == 'test' else 'users.db'
default_uri = f'sqlite:///{(Path(app.instance_path) / db_name).as_posix()}'

app.config.update(
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", default_uri),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    TESTING=(env == 'test'),
)

db.init_app(app)
app.register_blueprint(routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print('APP_ENV       =', env)
    print('INSTANCE_PATH =', app.instance_path)
    print('DB_URI        =', app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=(env != 'prod'))