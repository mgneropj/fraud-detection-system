import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [transaction, setTransaction] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState("Checking...");
  const [scenario, setScenario] = useState("LOW");

  // Live dashboard analytics
  const totalTransactions = history.length;

  const approvedCount = history.filter(
    (item) => item.decision === "APPROVE"
  ).length;

  const reviewCount = history.filter(
    (item) => item.decision === "REVIEW"
  ).length;

  const blockedCount = history.filter(
    (item) => item.decision === "BLOCK"
  ).length;

  useEffect(() => {
    checkApiHealth();
    loadHistory();
  }, []);

  const checkApiHealth = async () => {
    try {
      await axios.get(`${API_URL}/health`);
      setApiStatus("Connected");
    } catch (error) {
      setApiStatus("Offline");
    }
  };

  const loadHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/transactions`);
      setHistory(response.data.transactions || []);
    } catch (error) {
      console.error("Unable to load transaction history:", error);
    }
  };

  const randomFeature = () =>
    Number((Math.random() * 4 - 2).toFixed(4));

  const generateTransaction = () => {
    let sample = {
      Time: Math.floor(Math.random() * 172000),
      V1: randomFeature(),
      V2: randomFeature(),
      V3: randomFeature(),
      V4: randomFeature(),
      V5: randomFeature(),
      V6: randomFeature(),
      V7: randomFeature(),
      V8: randomFeature(),
      V9: randomFeature(),
      V10: randomFeature(),
      V11: randomFeature(),
      V12: randomFeature(),
      V13: randomFeature(),
      V14: randomFeature(),
      V15: randomFeature(),
      V16: randomFeature(),
      V17: randomFeature(),
      V18: randomFeature(),
      V19: randomFeature(),
      V20: randomFeature(),
      V21: randomFeature(),
      V22: randomFeature(),
      V23: randomFeature(),
      V24: randomFeature(),
      V25: randomFeature(),
      V26: randomFeature(),
      V27: randomFeature(),
      V28: randomFeature(),
      Amount: Number((Math.random() * 1000).toFixed(2)),
    };

    if (scenario === "MEDIUM") {
      sample.Amount = Number(
        (1500 + Math.random() * 1500).toFixed(2)
      );

      sample.V10 = -5.5;
    }

    if (scenario === "HIGH") {
      sample.Amount = Number(
        (5000 + Math.random() * 3000).toFixed(2)
      );

      sample.V10 = -7;
      sample.V12 = -7;
      sample.V14 = -7;
    }

    setTransaction(sample);
    setPrediction(null);
  };

  const analyzeTransaction = async () => {
    if (!transaction) {
      generateTransaction();
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/predict`,
        transaction
      );

      setPrediction(response.data.prediction);
      setApiStatus("Connected");

      await loadHistory();
    } catch (error) {
      console.error(error);
      setApiStatus("Offline");
      alert("Unable to connect to the Fraud Detection API.");
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (level) => {
    if (level === "HIGH") return "high";
    if (level === "MEDIUM") return "medium";
    return "low";
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return "-";
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>Fraud Detection System</h1>
          <p>ML-powered transaction risk analysis</p>
        </div>

        <div className="status">
          <span
            className={`status-dot ${
              apiStatus === "Connected" ? "online" : ""
            }`}
          ></span>

          API {apiStatus}
        </div>
      </header>

      <main className="container">

        {/* HERO */}
        <section className="hero">
          <div>
            <span className="badge">
              XGBoost + Rules Engine
            </span>

            <h2>
              Real-Time Transaction Risk Analysis
            </h2>

            <p>
              Evaluate transactions using machine learning,
              explainable fraud rules, and automated risk decisions.
            </p>
          </div>

          <div className="hero-actions">

            <select
              className="scenario-select"
              value={scenario}
              onChange={(event) => {
                setScenario(event.target.value);
                setTransaction(null);
                setPrediction(null);
              }}
            >
              <option value="LOW">
                Low Risk Demo
              </option>

              <option value="MEDIUM">
                Medium Risk Demo
              </option>

              <option value="HIGH">
                High Risk Demo
              </option>
            </select>

            <button
              className="secondary-button"
              onClick={generateTransaction}
            >
              Generate Transaction
            </button>

            <button
              className="primary-button"
              onClick={analyzeTransaction}
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Analyze Transaction"}
            </button>

          </div>
        </section>


        {/* LIVE ANALYTICS */}
        <section className="stats">

          <div className="stat-card">
            <span>Total Transactions</span>
            <strong>{totalTransactions}</strong>
            <small>Analyzed transactions</small>
          </div>

          <div className="stat-card">
            <span>Approved</span>
            <strong>{approvedCount}</strong>
            <small>Low-risk transactions</small>
          </div>

          <div className="stat-card">
            <span>Under Review</span>
            <strong>{reviewCount}</strong>
            <small>Medium-risk transactions</small>
          </div>

          <div className="stat-card">
            <span>Blocked</span>
            <strong>{blockedCount}</strong>
            <small>High-risk transactions</small>
          </div>

        </section>


        {/* RISK RESULT */}
        {prediction && (

          <section className="result-section">

            <div className="result-header">

              <div>
                <span className="section-label">
                  TRANSACTION ANALYSIS
                </span>

                <h2>Risk Assessment</h2>
              </div>

              <div
                className={`decision ${getRiskClass(
                  prediction.risk_level
                )}`}
              >
                {prediction.decision}
              </div>

            </div>


            <div className="risk-grid">

              <div className="risk-card main-risk">

                <span>Final Risk Score</span>

                <div className="risk-score">
                  {prediction.final_risk_score}
                </div>

                <div
                  className={`risk-level ${getRiskClass(
                    prediction.risk_level
                  )}`}
                >
                  {prediction.risk_level} RISK
                </div>

              </div>


              <div className="risk-card">

                <span>Fraud Probability</span>

                <strong>
                  {(prediction.fraud_probability * 100).toFixed(2)}%
                </strong>

                <small>XGBoost prediction</small>

              </div>


              <div className="risk-card">

                <span>ML Score</span>

                <strong>
                  {prediction.ml_score}
                </strong>

                <small>70% of final score</small>

              </div>


              <div className="risk-card">

                <span>Rule Score</span>

                <strong>
                  {prediction.rule_score}
                </strong>

                <small>30% of final score</small>

              </div>

            </div>


            <div className="analysis-grid">

              <div className="panel">

                <h3>Risk Decision</h3>

                <div className="decision-row">
                  <span>Final Score</span>

                  <strong>
                    {prediction.final_risk_score}/100
                  </strong>
                </div>

                <div className="decision-row">
                  <span>Risk Level</span>

                  <strong
                    className={getRiskClass(
                      prediction.risk_level
                    )}
                  >
                    {prediction.risk_level}
                  </strong>
                </div>

                <div className="decision-row">
                  <span>Action</span>

                  <strong
                    className={getRiskClass(
                      prediction.risk_level
                    )}
                  >
                    {prediction.decision}
                  </strong>
                </div>

              </div>


              <div className="panel">

                <h3>Explainable Risk Signals</h3>

                {prediction.reasons &&
                prediction.reasons.length > 0 ? (

                  <ul className="reasons">

                    {prediction.reasons.map(
                      (reason, index) => (

                        <li key={index}>
                          <span>!</span>
                          {reason}
                        </li>

                      )
                    )}

                  </ul>

                ) : (

                  <div className="no-reasons">
                    <span>✓</span>
                    No suspicious rules triggered.
                  </div>

                )}

              </div>

            </div>

          </section>

        )}


        {/* EMPTY STATE */}
        {!prediction && (

          <section className="empty-state">

            <div className="empty-icon">
              ◈
            </div>

            <h2>No Transaction Analyzed</h2>

            <p>
              Select a demo scenario, generate a transaction,
              and analyze it to see the fraud risk assessment.
            </p>

          </section>

        )}


        {/* TRANSACTION HISTORY */}
        <section className="history-section">

          <div className="history-header">

            <div>

              <span className="section-label">
                ACTIVITY
              </span>

              <h2>Transaction History</h2>

              <p>
                Recent transactions analyzed by the risk engine.
              </p>

            </div>

            <div className="history-count">
              {history.length} transactions
            </div>

          </div>


          {history.length === 0 ? (

            <div className="history-empty">
              <p>No transactions recorded yet.</p>
            </div>

          ) : (

            <div className="table-container">

              <table className="transaction-table">

                <thead>

                  <tr>
                    <th>Transaction</th>
                    <th>Time</th>
                    <th>Amount</th>
                    <th>Fraud Probability</th>
                    <th>Risk Score</th>
                    <th>Risk Level</th>
                    <th>Decision</th>
                  </tr>

                </thead>

                <tbody>

                  {history.map((item) => (

                    <tr key={item.transaction_id}>

                      <td>
                        <span className="transaction-id">
                          #{item.transaction_id}
                        </span>
                      </td>

                      <td>
                        {formatTimestamp(item.timestamp)}
                      </td>

                      <td>
                        ${Number(item.amount).toFixed(2)}
                      </td>

                      <td>
                        {(item.fraud_probability * 100).toFixed(2)}%
                      </td>

                      <td>
                        <strong>
                          {item.final_risk_score}
                        </strong>
                      </td>

                      <td>
                        <span
                          className={`table-badge ${getRiskClass(
                            item.risk_level
                          )}`}
                        >
                          {item.risk_level}
                        </span>
                      </td>

                      <td>
                        <span
                          className={`table-decision ${getRiskClass(
                            item.risk_level
                          )}`}
                        >
                          {item.decision}
                        </span>
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          )}

        </section>

      </main>


      {/* FOOTER */}
      <footer>

        <span>
          Fraud Detection System
        </span>

        <span>
          Built with React + FastAPI + XGBoost
        </span>

      </footer>

    </div>
  );
}

export default App;
