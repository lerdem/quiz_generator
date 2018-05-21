from flask import render_template, Blueprint, request, current_app
from flask.views import MethodView

from app.account.models import User
from app.extensions import sentry
from app.account.tasks import add_together


class Index(MethodView):

    def get(self):

        add_together.delay(23, 4)
        sentry.captureMessage(f'hello, world! {sentry.get_user_info(request)}')
        current_app.logger.info(f'{sentry.get_user_info(request)} failed to log in')

        context = {
            "users": User.query.all(),
            "cycle": range(1000),
        }

        return render_template('index.html', context=context)


blueprint = Blueprint('account', __name__, url_prefix='/account')
blueprint.add_url_rule('/', view_func=Index.as_view('index'))
