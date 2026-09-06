from backend.predictor import predict_transaction


def base_transaction():
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


def test_low_risk_decision():
    transaction = base_transaction()

    result = predict_transaction(transaction)

    assert result["risk_level"] == "LOW"
    assert result["decision"] == "APPROVE"


def test_medium_risk_decision():
    transaction = base_transaction()

    transaction["Amount"] = 2500
    transaction["V10"] = -5.5

    result = predict_transaction(transaction)

    assert result["rule_score"] == 35
    assert result["final_risk_score"] >= 50
    assert result["risk_level"] == "MEDIUM"
    assert result["decision"] == "REVIEW"


def test_high_risk_decision():
    transaction = base_transaction()

    transaction["Amount"] = 6000
    transaction["V10"] = -7
    transaction["V12"] = -7
    transaction["V14"] = -7

    result = predict_transaction(transaction)

    assert result["rule_score"] == 100
    assert result["final_risk_score"] >= 70
    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "BLOCK"