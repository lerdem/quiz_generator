from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_migrate import Migrate
from flask_compress import Compress
from flask_assets import Environment

db = SQLAlchemy()
cache = Cache()
migrate = Migrate()
compress = Compress()
assets = Environment()
