def calculate_rule_score(transaction):
    """
    Calculate an explainable risk score using simple fraud rules.

    Returns:
        rule_score: integer from 0 to 100
        reasons: list of triggered rules
    """

    score = 0
    reasons = []

    # Rule 1: Very large transaction
    amount = transaction.get("Amount", 0)

    if amount > 5000:
        score += 30
        reasons.append("Very high transaction amount")

    elif amount > 2000:
        score += 15
        reasons.append("High transaction amount")

    # Rule 2: Extremely unusual V14 value
    v14 = transaction.get("V14", 0)

    if v14 < -5:
        score += 30
        reasons.append("Unusual V14 pattern")

    # Rule 3: Extremely unusual V10 value
    v10 = transaction.get("V10", 0)

    if v10 < -5:
        score += 20
        reasons.append("Unusual V10 pattern")

    # Rule 4: Extremely unusual V12 value
    v12 = transaction.get("V12", 0)

    if v12 < -5:
        score += 20
        reasons.append("Unusual V12 pattern")

    # Keep score between 0 and 100
    score = min(score, 100)

    return score, reasons


if __name__ == "__main__":

    # Example transaction
    transaction = {
        "Amount": 6000,
        "V10": -6,
        "V12": -2,
        "V14": -7
    }

    score, reasons = calculate_rule_score(transaction)

    print("=" * 60)
    print("RULE ENGINE TEST")
    print("=" * 60)

    print(f"Rule Risk Score: {score}")

    print("\nTriggered Rules:")

    if reasons:
        for reason in reasons:
            print(f"- {reason}")
    else:
        print("- No suspicious rules triggered")

    print("\nRules engine working successfully!")