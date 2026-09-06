 🛡️ Fraud Detection System

> An end-to-end machine learning fraud detection platform that evaluates payment transactions using XGBoost, explainable business rules, risk scoring, FastAPI, React, and Docker.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-red)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikit-learn)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Pytest](https://img.shields.io/badge/Pytest-Tested-0A9EDC)
![Fraud Detection](https://img.shields.io/badge/AI-Fraud%20Detection-purple)

</p>

---

# 🚀 Overview

**Fraud Detection System** is a full-stack machine learning application designed to identify potentially fraudulent payment transactions.

The system combines:

- Machine learning fraud prediction
- Explainable rule-based risk signals
- Hybrid risk scoring
- Automated approve/review/block decisions
- FastAPI REST APIs
- React dashboard
- Transaction history
- Docker containerization
- Automated testing

The goal is to demonstrate how a machine learning model can be integrated into a practical transaction risk-decisioning workflow.

---

# ✨ Features

- 🤖 XGBoost fraud classification
- 📊 Logistic Regression baseline
- ⚖️ Class imbalance handling using `scale_pos_weight`
- 🎯 Threshold analysis
- 🧠 Hybrid ML + rule-based risk scoring
- 🔍 Explainable fraud signals
- 📈 Risk score from 0-100
- 🟢 LOW risk classification
- 🟡 MEDIUM risk classification
- 🔴 HIGH risk classification
- ✅ APPROVE decision
- ⚠️ REVIEW decision
- 🚫 BLOCK decision
- ⚡ FastAPI REST API
- ⚛️ React dashboard
- 📋 Transaction history
- 🧪 Automated Pytest test suite
- 🐳 Docker support
- 🐳 Docker Compose support

---

## 📸 Application Screenshots

### 🖥️ Fraud Detection Dashboard

The dashboard provides a real-time interface for analyzing transactions using the XGBoost model, explainable fraud rules, and automated risk decisions.

![Fraud Detection Dashboard](<img width="1840" height="898" alt="Screenshot 2026-09-06 144533" src="https://github.com/user-attachments/assets/c7ed199a-3743-47bc-be8b-ee61825abe42" />
)

---

### 🟢 LOW Risk — APPROVE

Low-risk transactions are automatically approved when no significant fraud signals are detected.

![LOW Risk Transaction](<img width="1919" height="741" alt="Screenshot 2026-09-06 144551" src="https://github.com/user-attachments/assets/e018d6f8-41fb-4cef-8fbf-3cc190961518" />
)

---

### 🟡 MEDIUM Risk — REVIEW

Medium-risk transactions trigger explainable rule-based signals and are sent for manual review.

![MEDIUM Risk Transaction](<img width="1876" height="763" alt="Screenshot 2026-09-06 144611" src="https://github.com/user-attachments/assets/02e8b149-fa15-4ea7-a411-c95b061afc43" />
)

---

### 🔴 HIGH Risk — BLOCK

High-risk transactions trigger multiple fraud signals and are automatically blocked by the risk engine.

![HIGH Risk Transaction](<img width="1891" height="835" alt="Screenshot 2026-09-06 144627" src="https://github.com/user-attachments/assets/b2c103e6-78a4-4c78-9e41-08cdde6af5ca" />
)

---

### 📊 Transaction History

The dashboard maintains a recent transaction history showing fraud probability, risk score, risk level, and the final decision.

![Transaction History](<img width="1889" height="356" alt="Screenshot 2026-09-06 144638" src="https://github.com/user-attachments/assets/87458d7e-931a-416d-bc0a-f6d451782bbc" />
)

# 🏗️ System Architecture

The application follows a complete transaction-to-decision fraud detection pipeline.

```mermaid
flowchart TD

    A[Customer Transaction] --> B[React Dashboard]

    B --> C[FastAPI API]

    C --> D[Feature Validation]

    D --> E[XGBoost Fraud Model]
    D --> F[Rule-Based Risk Engine]

    E --> G[Fraud Probability]
    G --> H[ML Risk Score]

    F --> I[Rule Risk Score]

    H --> J[Final Risk Engine]
    I --> J

    J --> K[Final Risk Score 0-100]

    K --> L{Risk Level}

    L -->|0-29.99| M[LOW]
    L -->|30-69.99| N[MEDIUM]
    L -->|70-100| O[HIGH]

    M --> P[APPROVE]
    N --> Q[REVIEW]
    O --> R[BLOCK]

    P --> S[Transaction History]
    Q --> S
    R --> S

    S --> B
