from http import HTTPStatus


def test_iris_predict(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    r = client.post("/ml/iris-predict", json=payload)

    assert r.status_code == HTTPStatus.OK

    body = r.json()

    assert "predictions" in body
    assert isinstance(body["predictions"], list)
    assert len(body["predictions"]) == 1

    if "latency_sec" in body and body["latency_sec"] is not None:
        assert isinstance(body["latency_sec"], (int, float))
