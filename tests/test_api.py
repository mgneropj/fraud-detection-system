from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def make_transaction():
    return {
        "Time": 10000,
        "V1": 0,
        "V2": 0,
        "V3": 0,
        "V4": 0,
        "V5": 0,
        "V6": 0,
        "V7": 0,
        "V8": 0,
        "V9": 0,
        "V10": 0,
        "V11": 0,
        "V12": 0,
        "V13": 0,
        "V14": 0,
        "V15": 0,
        "V16": 0,
        "V17": 0,
        "V18": 0,
        "V19": 0,
        "V20": 0,
        "V21": 0,
        "V22": 0,
        "V23": 0,
        "V24": 0,
        "V25": 0,
        "V26": 0,
        "V27": 0,
        "V28": 0,
        "Amount": 100,
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json=make_transaction()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "prediction" in data
    assert "transaction_id" in data

    prediction = data["prediction"]

    assert "fraud_probability" in prediction
    assert "final_risk_score" in prediction
    assert "risk_level" in prediction
    assert "decision" in prediction


def test_transactions_endpoint():
    response = client.get("/transactions")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "count" in data
    assert "transactions" in data