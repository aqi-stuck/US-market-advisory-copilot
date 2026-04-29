def test_ingest_requires_auth(client):
    response = client.post("/v1/ingest", json={"lane": "stocks", "documents": []})
    assert response.status_code == 401


def test_ingest_empty_documents(client):
    response = client.post(
        "/v1/ingest",
        json={"lane": "stocks", "documents": []},
        headers={"Authorization": "Bearer test-api-key-12345"},
    )
    assert response.status_code == 200
    assert response.json()["documents_processed"] == 0
