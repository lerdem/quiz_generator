from flask import url_for

from app.extensions import cache


def test_server_is_up_and_running(app):
    client = app.test_client()
    response = client.get(url_for('account.index'))
    assert response.status_code == 200


def test_cache():
    key = "test_key"
    value = 'test_value'
    cache.set(key, value)
    assert cache.get(key) == value
