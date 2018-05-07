from flask import render_template, Blueprint
from flask.views import MethodView

from app.account.models import User


class Index(MethodView):

    def get(self):
        from app.account.tasks import add_together
        print(add_together.delay(23, 4))
        context = {"users": User.query.all()}
        return render_template('index.html', context=context)


blueprint = Blueprint('account', __name__, url_prefix='/account', template_folder='templates')
blueprint.add_url_rule('/', view_func=Index.as_view('index'))
