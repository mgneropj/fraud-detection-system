from src.rules_engine import calculate_rule_score


def test_low_risk_transaction():
    transaction = {
        "Amount": 100,
        "V10": 0,
        "V12": 0,
        "V14": 0,
    }

    score, reasons = calculate_rule_score(transaction)

    assert score == 0
    assert reasons == []


def test_high_amount_rule():
    transaction = {
        "Amount": 6000,
        "V10": 0,
        "V12": 0,
        "V14": 0,
    }

    score, reasons = calculate_rule_score(transaction)

    assert score == 30
    assert "Very high transaction amount" in reasons


def test_multiple_fraud_rules():
    transaction = {
        "Amount": 6000,
        "V10": -6,
        "V12": -6,
        "V14": -6,
    }

    score, reasons = calculate_rule_score(transaction)

    assert score == 100
    assert len(reasons) == 4


def test_medium_risk_rules():
    transaction = {
        "Amount": 2500,
        "V10": -5.5,
        "V12": 0,
        "V14": 0,
    }

    score, reasons = calculate_rule_score(transaction)

    assert score == 35
    assert "High transaction amount" in reasons
    assert "Unusual V10 pattern" in reasons