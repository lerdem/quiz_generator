import pytest
import requests
from flask import current_app


@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    def test_server_is_up_and_running(self):

        print(current_app.config)
        # raise AttributeError
        res = requests.get(f'http://{current_app.config["SERVER_NAME"]}/account/')
        assert res.status_code == 200
