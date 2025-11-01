import time


def test_index_and_search(client):
    # index
    payload = {
        "items": [
            {"id": 1, "text": "яблоко и груша это фрукты"},
            {"id": 2, "text": "банан — желтый фрукт"},
            {"id": 3, "text": "огурец — овощ"}
        ]

    }
    r = client.post("/index", json=payload)
    assert r.status_code == 200
    assert r.json()["indexed"] == 3
    time.sleep(0.2)

    #search
    r = client.post("/search", json={"query": "фрукты", "top_k": 2})
    assert r.status_code == 200
    hits = r.json()["hits"]
    assert len(hits) == 2
    assert all("id" in h and "score" in h for h in hits)
