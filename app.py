import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="AIvest: Financial Learning & Investment Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .lesson-title {
        color: #1e3a8a;
        font-weight: 700;
    }
    .quiz-box {
        background-color: #f1f5f9;
        border-left: 4px solid #2563eb;
        padding: 15px;
        border-radius: 4px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

if "cash" not in st.session_state:
    st.session_state.cash = 10000.0 
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {"AAPL": 0.0, "TSLA": 0.0, "BTC-USD": 0.0, "ETH-USD": 0.0}
if "history" not in st.session_state:
    st.session_state.history = []

LESSONS_DATA = [
    {
        "id": 1,
        "title": "1. Financial Literacy & Budgeting Basics",
        "concept": """
        **Core Principles:**
        Financial literacy begins with cash flow management. The foundational guideline is the **50/30/20 Rule**:
        - **50% Needs:** Rent, groceries, utilities, debt minimums.
        - **30% Wants:** Entertainment, dining out, hobbies.
        - **20% Savings & Debt Acceleration:** Emergency fund, retirement accounts, market investments.

        *Emergency Reserve:* Maintain 3 to 6 months of living expenses in high-yield liquid instruments before aggressive investing.
        """,
        "quiz": {
            "q": "Under the 50/30/20 rule, which category does funding your emergency reserve belong to?",
            "options": ["Needs", "Wants", "Savings & Investments", "Discretionary"],
            "correct": 2,
            "explain": "The 20% bucket is explicitly allocated to building emergency cushions and financial assets."
        },
        "practice": "Calculate your net monthly surplus: if monthly income is $4,000 and fixed expenses are $2,200, determine the ideal emergency allocation."
    },
    {
        "id": 2,
        "title": "2. The Power of Compound Interest & Time Value of Money",
        "concept": """
        **The Mathematical Multiplier:**
        Compound interest is calculated using:
        $$A = P \\left(1 + \\frac{r}{n}\\right)^{nt}$$
        Where $P$ is principal, $r$ is annual rate, $n$ is compounding frequency, and $t$ is time in years.

        **The Rule of 72:** To estimate how many years it takes to double your money at interest rate $R\\%$, calculate:
        $$\\text{Years to Double} \\approx \\frac{72}{R}$$
        At 8% annual return, capital doubles approximately every 9 years without additional contributions.
        """,
        "quiz": {
            "q": "Using the Rule of 72, roughly how long does it take an investment to double at 9% annualized return?",
            "options": ["6 years", "8 years", "9 years", "12 years"],
            "correct": 1,
            "explain": "72 / 9 = 8 years."
        },
        "practice": "Experiment with the compound interest calculator in the Simulator tab to visualize a 15-year holding period."
    },
    {
        "id": 3,
        "title": "3. Understanding Equities & Stock Valuation",
        "concept": """
        **What is an Equity Share?**
        Purchasing stock represents fractional ownership of an enterprise. Valuation models evaluate whether shares trade above or below fair value:
        - **P/E (Price-to-Earnings):** Price relative to per-share profit. High P/E often indicates strong expected growth.
        - **EPS (Earnings Per Share):** Net income divided by total outstanding shares.
        - **Dividend Yield:** Percentage dividend payout relative to current market price.
        """,
        "quiz": {
            "q": "What does a very high P/E ratio typically indicate about market expectations?",
            "options": ["The company is about to go bankrupt", "Investors expect strong future earnings growth",
                        "The company pays massive dividends", "The stock is completely risk-free"],
            "correct": 1,
            "explain": "A high P/E indicates investors are willing to pay a premium now for anticipated future earnings acceleration."
        },
        "practice": "Look up Apple (AAPL) in the Live Market tab and observe its current price momentum."
    },
    {
        "id": 4,
        "title": "4. Fixed Income, Bonds & Macro Interest Rates",
        "concept": """
        **Bond Dynamics & Interest Rates:**
        Bonds are debt obligations where an investor loans capital to a government or corporation in exchange for recurring coupon payments and face value return at maturity.

        **Fundamental Law of Bonds:** Bond prices move **inversely** to market interest rates:
        - If the central bank raises benchmark rates, existing lower-yielding bonds drop in price.
        - If benchmark rates drop, existing higher-coupon bonds appreciate.
        """,
        "quiz": {
            "q": "When a central bank increases interest rates, what typically happens to the price of existing bonds?",
            "options": ["Prices surge", "Prices decline", "Prices stay exactly constant", "Coupons are canceled"],
            "correct": 1,
            "explain": "Bond prices and yields share an inverse relationship; higher market yields devalue existing lower-yielding paper."
        },
        "practice": "Assess whether defensive portfolios should tilt toward short-duration bonds in a high-rate cycle."
    },
    {
        "id": 5,
        "title": "5. Index Funds, ETFs & Passive Investing",
        "concept": """
        **Diversification via Indexation:**
        - **ETF (Exchange-Traded Fund):** A basket of hundreds of securities traded intraday like a single stock.
        - **Market Capitalization Weighting:** Indexes like the S&P 500 allocate higher percentages to mega-cap leaders (e.g., Apple, Microsoft, Nvidia).
        - **Expense Ratio:** The annual administrative management fee deducted from portfolio assets. Low-cost index ETFs charge as little as 0.03% to 0.07%.
        """,
        "quiz": {
            "q": "What is the primary advantage of a broad-market index ETF over individual stock picking for novice investors?",
            "options": ["Guaranteed 50% returns", "Instant diversification and minimal expense ratios",
                        "Zero market volatility", "Direct control over board meetings"],
            "correct": 1,
            "explain": "Broad ETFs distribute risk across hundreds of corporations at low operational costs."
        },
        "practice": "Compare the performance of an individual stock like TSLA to a broader tech allocation."
    },
    {
        "id": 6,
        "title": "6. Modern Portfolio Theory (MPT) & Diversification",
        "concept": """
        **Unsystematic vs. Systematic Risk:**
        - **Systematic Risk:** Market-wide macroeconomic events affecting all participants (recessions, liquidity shocks, inflation). Cannot be diversified away.
        - **Unsystematic Risk:** Company- or sector-specific risks (factory fires, leadership failure, product recalls). Mitigated through non-correlated asset diversification.

        Harry Markowitz showed that combining uncorrelated assets shifts the **Efficient Frontier**, increasing expected return per unit of volatility.
        """,
        "quiz": {
            "q": "Which type of risk can be effectively mitigated through asset class diversification?",
            "options": ["Systematic risk", "Unsystematic (idiosyncratic) risk", "Currency extinction",
                        "Sovereign inflation"],
            "correct": 1,
            "explain": "Idiosyncratic company-specific risks are diluted when holding diverse assets across various sectors."
        },
        "practice": "Construct a portfolio in the Simulator containing both equities and digital assets to monitor balance shifts."
    },
    {
        "id": 7,
        "title": "7. Digital Assets: Bitcoin & Ethereum Architecture",
        "concept": """
        **Decentralized Ledgers:**
        - **Bitcoin (BTC):** Digital store of value and permissionless settlement network with a hard-coded maximum supply limit of 21 million units.
        - **Ethereum (ETH):** Programmable decentralized blockchain supporting Turing-complete smart contracts, decentralized finance (DeFi), and token standards.
        - **Volatility Profile:** Cryptocurrencies carry significantly higher annualized volatility and drawdown potential than traditional blue-chip equities.
        """,
        "quiz": {
            "q": "What is the primary architectural differentiator of Ethereum compared to Bitcoin?",
            "options": ["Ethereum has a 21M hard cap", "Ethereum enables programmable smart contracts and dApps",
                        "Ethereum does not use cryptography", "Ethereum is centralized under a single bank"],
            "correct": 1,
            "explain": "Ethereum's virtual machine allows developers to execute arbitrary decentralized application code."
        },
        "practice": "Review the 30-day forecast curves for BTC and ETH in the Market Forecast module."
    },
    {
        "id": 8,
        "title": "8. Risk Management, Drawdowns & Position Sizing",
        "concept": """
        **Capital Preservation Rules:**
        1. **Maximum Drawdown (MDD):** The peak-to-trough drop in total equity.
        2. **Asymmetry of Loss:** A 50% loss requires a 100% gain just to break even; an 80% loss requires a 400% recovery.
        3. **Position Sizing:** Never risk more than 1-2% of total net liquid portfolio value on any single speculative position.
        """,
        "quiz": {
            "q": "If your portfolio suffers a 50% drawdown, what percentage gain is required to return to the original capital level?",
            "options": ["50%", "75%", "100%", "200%"],
            "correct": 2,
            "explain": "If $10,000 drops to $5,000, you must gain $5,000 on the $5,000 base—a 100% return."
        },
        "practice": "Formulate a stop-loss guideline before entering a trade in the paper trading simulator."
    },
    {
        "id": 9,
        "title": "9. Behavioral Finance & Investor Psychology",
        "concept": """
        **Cognitive Biases in Markets:**
        - **Loss Aversion:** The psychological pain of losing $1,000 is twice as impactful as the pleasure of gaining $1,000.
        - **FOMO (Fear Of Missing Out):** Chasing parabolic price rallies near cyclical market tops.
        - **Confirmation Bias:** Selectively seeking news analysis that supports an existing winning or losing trade.
        """,
        "quiz": {
            "q": "Selling winning assets too early while stubbornly holding losing assets hoping to break even is driven by:",
            "options": ["Loss aversion & the Disposition Effect", "Efficient Market Hypothesis",
                        "Arbitrage Pricing Theory", "Pure rational choice"],
            "correct": 0,
            "explain": "The disposition effect leads investors to realize gains prematurely while avoiding the emotional pain of booking losses."
        },
        "practice": "Document your rationale before executing your next simulated trade to eliminate impulse triggers."
    },
    {
        "id": 10,
        "title": "10. Advanced Asset Allocation & Systematic Rebalancing",
        "concept": """
        **Portfolio Governance:**
        Strategic asset allocation establishes target weightings based on risk tolerance (e.g., 70% Global Equities, 20% Fixed Income, 10% Alternative/Crypto).

        **Calendar vs. Band Rebalancing:**
        - Periodically selling assets that have appreciated above target weights and buying depressed classes restores your intended risk profile.
        - Systematically enforces: **Sell high, buy low.**
        """,
        "quiz": {
            "q": "What is the primary disciplined benefit of systematic portfolio rebalancing?",
            "options": ["Maximizing leverage",
                        "Enforcing a systematic process of trimming appreciated assets and buying cheaper assets",
                        "Eliminating tax liabilities completely", "Preventing all price drops"],
            "correct": 1,
            "explain": "Rebalancing resets portfolio risk back to baseline by taking profits from outperforming assets and reallocating to lagging ones."
        },
        "practice": "Review your simulator positions. If one asset exceeds 40% of total allocation, rebalance into cash or other holdings."
    }
]

ASSETS = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD"
}


@st.cache_data(ttl=3600)
def load_market_data(ticker: str, period="1y"):
    df = yf.download(ticker, period=period, interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.dropna(inplace=True)
    return df


def generate_forecast(df: pd.DataFrame, forecast_days=30):
    df_clean = df.reset_index()
    df_clean['Day_Index'] = np.arange(len(df_clean))

    X = df_clean[['Day_Index']]
    y = df_clean['Close']

    model = LinearRegression()
    model.fit(X, y)

    last_date = df_clean['Date'].iloc[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]
    future_indices = np.arange(len(df_clean), len(df_clean) + forecast_days).reshape(-1, 1)

    predicted_prices = model.predict(future_indices)

    return future_dates, predicted_prices, model.coef_[0]


#main navigation
tabs = st.tabs(["Academy (10 Lessons & Tests)", "Real-Time Markets & Forecast", "Investment Simulator"])

with tabs[0]:
    st.header("Financial Literacy & Investment Curriculum")
    st.markdown(
        "Select a module to study foundational economics, complete comprehension quizzes, and execute practical exercises.")

    lesson_titles = [f"Module {l['id']}: {l['title'].split('. ')[1]}" for l in LESSONS_DATA]
    selected_module_idx = st.selectbox("Choose Lesson Module:", range(len(lesson_titles)),
                                       format_func=lambda x: lesson_titles[x])

    current_lesson = LESSONS_DATA[selected_module_idx]

    st.subheader(current_lesson["title"])
    st.markdown(current_lesson["concept"])

    # practical task
    st.info(f"**Practical Exercise:** {current_lesson['practice']}")

    # quiz block
    st.markdown("---")
    st.markdown("Module Assessment")
    quiz = current_lesson["quiz"]

    quiz_key = f"quiz_{current_lesson['id']}"
    user_answer = st.radio(quiz["q"], quiz["options"], key=quiz_key)

    if st.button("Submit Answer", key=f"btn_{current_lesson['id']}"):
        chosen_idx = quiz["options"].index(user_answer)
        if chosen_idx == quiz["correct"]:
            st.success(f"✅ Correct! {quiz['explain']}")
        else:
            st.error(f"❌ Incorrect. {quiz['explain']}")

# markets and forecats
with tabs[1]:
    st.header("Real-Time Markets & Price Forecast Engine")
    st.markdown("Live market tracking for **Apple, Tesla, Bitcoin, and Ethereum** with statistical trend forecasting.")

    col_sel, col_days = st.columns([2, 1])
    with col_sel:
        asset_label = st.selectbox("Select Asset to Analyze:", list(ASSETS.keys()))
        selected_ticker = ASSETS[asset_label]
    with col_days:
        forecast_horizon = st.slider("Forecast Horizon (Days):", min_value=7, max_value=60, value=30)

    with st.spinner("Fetching market telemetry..."):
        try:
            hist_df = load_market_data(selected_ticker, period="1y")

            if hist_df.empty:
                st.error("No pricing data found. Please check internet connection or retry.")
            else:
                current_price = float(hist_df['Close'].iloc[-1])
                prev_price = float(hist_df['Close'].iloc[-2])
                price_delta = current_price - prev_price
                pct_delta = (price_delta / prev_price) * 100

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Current Market Price", f"${current_price:,.2f}", delta=f"{pct_delta:.2f}% (1D)")
                m2.metric("52-Week High", f"${float(hist_df['High'].max()):,.2f}")
                m3.metric("52-Week Low", f"${float(hist_df['Low'].min()):,.2f}")

                future_dates, predictions, trend_slope = generate_forecast(hist_df, forecast_days=forecast_horizon)
                forecast_target = predictions[-1]
                m4.metric(f"{forecast_horizon}D Projected Trend", f"${forecast_target:,.2f}",
                          delta=f"Slope: {trend_slope:+.2f}/day")

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=hist_df.index,
                    y=hist_df['Close'],
                    mode='lines',
                    name='Historical Price (USD)',
                    line=dict(color='#2563eb', width=2)
                ))

                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=predictions,
                    mode='lines',
                    name=f'{forecast_horizon}-Day Trend Forecast',
                    line=dict(color='#f97316', width=2.5, dash='dash')
                ))

                fig.update_layout(
                    title=f"{asset_label} Historical Trends & Predictive Projection",
                    xaxis_title="Date",
                    yaxis_title="Price ($ USD)",
                    template="plotly_white",
                    hovermode="x unified",
                    height=550
                )

                st.plotly_chart(fig, use_container_width=True)

                st.caption(
                    "**Statistical Note:** Trend projection is generated via linear least-squares regression over the past 365 days of close prices for educational and strategic modeling.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

# simulator
with tabs[2]:
    st.header("Live Paper-Trading Simulator")
    st.markdown("Practice capital allocation in a simulated sandbox with your starting **$10,000** bankroll.")

    asset_prices = {}
    for name, ticker in ASSETS.items():
        try:
            d = load_market_data(ticker, period="5d")
            asset_prices[ticker] = float(d['Close'].iloc[-1])
        except:
            asset_prices[ticker] = 100.0

    portfolio_value = st.session_state.cash
    for ticker, shares in st.session_state.portfolio.items():
        portfolio_value += shares * asset_prices.get(ticker, 0.0)

    pnl = portfolio_value - 10000.0
    pnl_pct = (pnl / 10000.0) * 100

    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric("Available Cash Balance", f"${st.session_state.cash:,.2f}")
    col_c2.metric("Total Portfolio Equity", f"${portfolio_value:,.2f}")
    col_c3.metric("Total Sandbox PnL", f"${pnl:+,.2f}", delta=f"{pnl_pct:+.2f}%")

    st.markdown("---")


    
    st.subheader("Execute Trade Order")
    trade_col1, trade_col2, trade_col3, trade_col4 = st.columns(4)

    with trade_col1:
        trade_asset_name = st.selectbox("Select Asset:", list(ASSETS.keys()), key="trade_asset")
        trade_ticker = ASSETS[trade_asset_name]
    with trade_col2:
        unit_price = asset_prices.get(trade_ticker, 0.0)
        st.write(f"**Spot Price:** ${unit_price:,.2f}")
        order_action = st.radio("Action:", ["BUY", "SELL"], horizontal=True)
    with trade_col3:
        trade_qty = st.number_input("Quantity:", min_value=0.001, max_value=100000.0, value=1.0, step=0.1)
    with trade_col4:
        total_trade_val = trade_qty * unit_price
        st.write(f"**Estimated Value:** ${total_trade_val:,.2f}")
        execute_trade = st.button("Execute Transaction", type="primary")

    if execute_trade:
        if order_action == "BUY":
            if total_trade_val > st.session_state.cash:
                st.error("❌ Insufficient liquid funds to execute purchase.")
            else:
                st.session_state.cash -= total_trade_val
                st.session_state.portfolio[trade_ticker] += trade_qty
                st.session_state.history.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Type": "BUY",
                    "Asset": trade_ticker,
                    "Units": trade_qty,
                    "Execution Price": unit_price,
                    "Total": total_trade_val
                })
                st.success(f"✅ Successfully bought {trade_qty:.4f} shares/units of {trade_ticker}!")
                st.rerun()
        elif order_action == "SELL":
            current_holding = st.session_state.portfolio.get(trade_ticker, 0.0)
            if trade_qty > current_holding:
                st.error(f"❌ Cannot sell more than you hold. Current holding: {current_holding:.4f}")
            else:
                st.session_state.cash += total_trade_val
                st.session_state.portfolio[trade_ticker] -= trade_qty
                st.session_state.history.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Type": "SELL",
                    "Asset": trade_ticker,
                    "Units": trade_qty,
                    "Execution Price": unit_price,
                    "Total": total_trade_val
                })
                st.success(f"✅ Successfully sold {trade_qty:.4f} units of {trade_ticker}!")
                st.rerun()

    st.markdown("---")


    h_col1, h_col2 = st.columns([1, 1])
    with h_col1:
        st.subheader("Your Asset Allocations")
        alloc_data = []
        for ticker, qty in st.session_state.portfolio.items():
            if qty > 0:
                pos_val = qty * asset_prices.get(ticker, 0.0)
                alloc_data.append({"Ticker": ticker, "Quantity": qty, "Market Value ($)": round(pos_val, 2)})

        if alloc_data:
            df_alloc = pd.DataFrame(alloc_data)
            st.dataframe(df_alloc, use_container_width=True)

            fig_alloc = go.Figure(
                data=[go.Pie(labels=df_alloc["Ticker"], values=df_alloc["Market Value ($)"], hole=0.4)])
            fig_alloc.update_layout(title="Asset Weight Distribution", margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_alloc, use_container_width=True)
        else:
            st.info("No active equity or digital asset holdings. You are currently 100% in cash.")

    with h_col2:
        st.subheader("Transaction History Ledger")
        if st.session_state.history:
            df_hist = pd.DataFrame(st.session_state.history)
            st.dataframe(df_hist.iloc[::-1], use_container_width=True)
        else:
            st.write("No transactions executed yet.")
