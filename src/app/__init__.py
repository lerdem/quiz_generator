from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_migrate import Migrate

from configs import Config


app = Config.create_app()
app.jinja_env.undefined = Config.JINJA_UNDEFINED  # maybe there is a better way to pass this variable
db = SQLAlchemy(app)
cache = Cache(app)
migrate = Migrate(app, db)
celery = Config.make_celery(app)

from app.account.views import blueprint as account_bp

app.register_blueprint(account_bp)
