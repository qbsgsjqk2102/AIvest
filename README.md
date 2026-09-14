# AIvest: Financial Literacy Academy & Investment Simulator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**AIvest** is an open-source, interactive web platform engineered to bridge the gap between theoretical financial literacy, data-driven market analytics, and risk-free quantitative portfolio experimentation.

Built natively in Python using **Streamlit**, **Plotly**, and **Scikit-Learn**, the platform provides a complete environment featuring a 10-module economics curriculum, real-time telemetry from equity and cryptocurrency markets, algorithmic trend projection, and a full paper-trading execution desk.

---

## Key Architecture & Modules

### 1. Financial Literacy Curriculum (10 Modules)
A progressive academic sequence designed around foundational and quantitative investing paradigms:
- **Module 1:** Budgeting Frameworks & The 50/30/20 Rule
- **Module 2:** The Mathematics of Compounding & Time Value of Money (Rule of 72)
- **Module 3:** Equity Valuation Fundamentals ($P/E$, $EPS$, Dividend Yield)
- **Module 4:** Fixed-Income Instruments, Bond Pricing & Interest Rate Inverse Law
- **Module 5:** Indexation, Broad-Market ETFs & Expense Ratio Drag
- **Module 6:** Modern Portfolio Theory (MPT), Efficient Frontier & Idiosyncratic Risk Mitigation
- **Module 7:** Digital Assets Architecture: Bitcoin vs. Ethereum Virtual Machine (EVM)
- **Module 8:** Quantitative Risk Management, Position Sizing & Drawdown Asymmetry
- **Module 9:** Behavioral Economics & Cognitive Investor Biases (Loss Aversion, FOMO)
- **Module 10:** Strategic Asset Allocation & Dynamic Rebalancing Thresholds

*Every module includes comprehensive conceptual write-ups, interactive single-choice evaluations with automated feedback loops, and actionable practical exercises.*

### 2. Real-Time Telemetry & Predictive Price Engine
- **Live Feeds:** Real-time data streaming for flagship market benchmarks: **Apple (AAPL)**, **Tesla (TSLA)**, **Bitcoin (BTC)**, and **Ethereum (ETH)** via `yfinance`.
- **Telemetry Cards:** 52-week price bounds, intraday basis deltas, and automated percentage fluctuations.
- **Predictive Trajectory:** Linear least-squares regression trendline projections across configurable horizons (7–60 trading sessions) rendered via interactive `Plotly` graphs.

### 3. Sandbox Investment Simulator (Paper-Trading Desk)
- **Live Capital Engine:** Real-time spot valuation with an initial $10,000 liquidity balance.
- **Order Execution:** Instant execution of `BUY` and `SELL` market orders with validation checks (anti-insolvency and share balance clamping).
- **Portfolio Analytics:** Dynamic asset weighting donut visualizations and an immutable chronological transaction audit trail.

---

## Technology Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Data Engineering:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Market Data Provider:** [yfinance](https://pypi.org/project/yfinance/)
- **Data Visualization:** [Plotly Graph Objects](https://plotly.com/python/)
- **Machine Learning & Modeling:** [Scikit-Learn](https://scikit-learn.org/) (Linear Regression Engine)

---

## Quickstart & Local Setup

### Prerequisites
- Python `3.10` or higher
- Git

### 1. Clone Repository
```bash
git clone [https://github.com/qbsgsjqk2102/AIvest.git](https://github.com/qbsgsjqk2102/AIvest.git)
cd AIvest
