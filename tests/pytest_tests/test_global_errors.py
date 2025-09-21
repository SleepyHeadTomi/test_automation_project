from sqlalchemy.exc import IntegrityError

def _install_test_route(app, rule, view_func):
    app.add_url_rule(rule, endpoint=rule, view_func=view_func)

def test_integrity_error_handler_returns_500_and_rolls_back(client, monkeypatch):
    app = client.application
    app.config['PROPAGATE_EXCEPTIONS'] = False

    from app.models import db
    called = {"rollback": False}
    def fake_rollback():
        called["rollback"] = True
    monkeypatch.setattr(db.session, "rollback", fake_rollback, raising=True)

    def boom():
        raise IntegrityError("stmt", {"param": "x"}, Exception("orig"))
    _install_test_route(app, "/__test__/integrity_boom", boom)

    response = client.get("/__test__/integrity_boom")
    assert response.status_code == 500
    assert response.is_json
    assert response.get_json() == {"error": "Database integrity error"}
    assert called["rollback"] is True

def test_generic_exception_handler_returns_500_and_json(client):
    app = client.application
    app.config['PROPAGATE_EXCEPTIONS'] = False

    def crash():
        raise RuntimeError("boom")
    _install_test_route(app, "/__test__/crash", crash)

    response = client.get("/__test__/crash")
    assert response.status_code == 500
    assert response.is_json
    assert response.get_json() == {"error": "Internal server error"}