from flask import render_template, Blueprint
from flask.views import MethodView

from app.account.models import User
from app.extensions import cache


class Index(MethodView):

    def get(self):
        from app.account.tasks import add_together
        print(add_together.delay(23, 4))
        cache.set('KEY', "VALUE")
        print(f"CACHE {cache.get('KEY')}")
        context = {
            "users": User.query.all(),
            "cycle": range(100000),
        }
        return render_template('index.html', context=context)


blueprint = Blueprint('account', __name__, url_prefix='/account')
blueprint.add_url_rule('/', view_func=Index.as_view('index'))
