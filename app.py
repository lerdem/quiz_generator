import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from views import Index

app = Flask(__name__)
app.config.from_object(f'configs.{os.environ["CONFIG_CLASS"]}')
db = SQLAlchemy(app)

app.add_url_rule('/', view_func=Index.as_view('index'))

