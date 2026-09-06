from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.predictor import predict_transaction


app = FastAPI(
    title="Fraud Detection API",
    description="ML-powered fraud detection and risk scoring API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# TRANSACTION MODEL
# ============================================================

class Transaction(BaseModel):
    Time: float

    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    Amount: float


# ============================================================
# IN-MEMORY TRANSACTION HISTORY
# ============================================================

transaction_history = []


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Fraud Detection API is running",
        "docs": "/docs",
        "health": "/health",
        "prediction_endpoint": "/predict",
        "transactions_endpoint": "/transactions"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "fraud-detection-api",
        "model": "xgboost"
    }


# ============================================================
# PREDICT
# ============================================================

@app.post("/predict")
def predict(transaction: Transaction):

    try:
        transaction_data = transaction.model_dump()

        result = predict_transaction(
            transaction_data
        )

        transaction_record = {
            "transaction_id": str(uuid4())[:8],
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "amount": transaction.Amount,
            "fraud_probability": result["fraud_probability"],
            "ml_score": result["ml_score"],
            "rule_score": result["rule_score"],
            "final_risk_score": result["final_risk_score"],
            "risk_level": result["risk_level"],
            "decision": result["decision"],
            "reasons": result["reasons"]
        }

        transaction_history.insert(
            0,
            transaction_record
        )

        # Keep only the latest 50 transactions
        transaction_history[:] = transaction_history[:50]

        return {
            "success": True,
            "prediction": result,
            "transaction_id": transaction_record["transaction_id"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# TRANSACTION HISTORY
# ============================================================

@app.get("/transactions")
def get_transactions():

    return {
        "success": True,
        "count": len(transaction_history),
        "transactions": transaction_history
    }