from flask import render_template
from flask.views import MethodView


class Index(MethodView):

    def get(self):
        from app import add_together
        print(add_together.delay(23, 4))
        print('CACHED'*10)
        context = {"name": "Dima"}
        return render_template('index.html', context=context)
