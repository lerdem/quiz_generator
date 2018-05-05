from flask.views import MethodView


class Index(MethodView):

    def get(self):
        print('CACHED'*10)
        return "Index"
