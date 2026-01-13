from flask_sqlalchemy import SQAlchemy
from flask_migrate import Migrate

db = SQAlchemy()
migrate = Migrate()