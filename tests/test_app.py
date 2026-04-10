import importlib


def test_app_imports():
    mod = importlib.import_module("app")
    assert hasattr(mod, "app")


def test_index_route():
    mod = importlib.import_module("app")
    client = mod.app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    assert b"vulnerable app" in r.data
