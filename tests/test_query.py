def test_query_requires_auth(client):
    response = client.post("/v1/query", json={"query": "test"})
    assert response.status_code == 401

def test_query_returns_answer(client):
    response = client.post(
        "/v1/query",
        json={"query": "US equity markets", "top_k": 2},
        headers={"Authorization": "Bearer change-me"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
