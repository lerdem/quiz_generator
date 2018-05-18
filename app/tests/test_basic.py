
class TestApp:
    def test_server_is_up_and_running(self, app):
        # with app.test_client('/account/') as test_client:
        client = app.test_client()
        response = client.get('/account/')
        assert response.status_code == 200
