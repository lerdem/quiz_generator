def bad_request(e):
    return 'ERROR 400', 400


def unauthorized(e):
    return 'ERROR 401', 401


def forbidden(e):
    return 'ERROR 403', 403


def not_found(e):
    return 'ERROR 404', 404


def gone(e):
    return 'ERROR 410', 410


def internal_server(e):
    return 'ERROR 500', 500
