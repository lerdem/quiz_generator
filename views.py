from flask.views import MethodView


class Index(MethodView):

    def get(self):
        return "Index"
