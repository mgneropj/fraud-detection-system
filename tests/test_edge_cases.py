import pytest

from backend.predictor import predict_transaction
from src.rules_engine import calculate_rule_score


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


def test_extreme_rules_cap_score_at_100():
    transaction = {
        "Amount": 100000,
        "V10": -100,
        "V12": -100,
        "V14": -100,
    }

    score, reasons = calculate_rule_score(transaction)

    assert score == 100
    assert 0 <= score <= 100
    assert len(reasons) == 4


def test_negative_amount_does_not_trigger_amount_rule():
    transaction = {
        "Amount": -500,
        "V10": 0,
        "V12": 0,
        "V14": 0,
    }

    score, reasons = calculate_rule_score(transaction)

    assert score == 0
    assert reasons == []


def test_prediction_score_stays_within_range():
    transaction = base_transaction()

    transaction["Amount"] = 100000
    transaction["V10"] = -100
    transaction["V12"] = -100
    transaction["V14"] = -100

    result = predict_transaction(transaction)

    assert 0 <= result["final_risk_score"] <= 100
    assert 0 <= result["ml_score"] <= 100
    assert 0 <= result["rule_score"] <= 100


def test_missing_feature_is_rejected():
    transaction = base_transaction()

    del transaction["V14"]

    with pytest.raises(ValueError):
        predict_transaction(transaction)