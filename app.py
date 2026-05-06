import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📊 Stock Market Dashboard")

# -----------------------------
# Input Section
# -----------------------------
col1, col2 = st.columns([3, 1])

with col1:
    stock = st.text_input("🔍 Enter Stock Symbol", placeholder="e.g. AAPL")

with col2:
    period = st.selectbox("📅 Select Period", ["7d", "1mo", "3mo", "6mo", "1y"])

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🚀 Analyze"):

    # Validation
    if not stock:
        st.warning("⚠️ Please enter a stock symbol")
        st.stop()

    try:
        with st.spinner("Fetching stock data..."):

            data = yf.Ticker(stock)
            hist = data.history(period=period)

            # Check if valid
            if hist.empty:
                st.error("❌ Invalid stock symbol")
                st.stop()

            # -----------------------------
            # Metrics
            # -----------------------------
            current_price = hist['Close'].iloc[-1]
            high_price = hist['High'].max()
            low_price = hist['Low'].min()

            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Current Price", f"{current_price:.2f}")
            col2.metric("📈 Highest", f"{high_price:.2f}")
            col3.metric("📉 Lowest", f"{low_price:.2f}")

            # -----------------------------
            # Chart
            # -----------------------------
            st.subheader("📊 Price Trend")
            st.line_chart(hist['Close'])

            # -----------------------------
            # Data Table
            # -----------------------------
            st.subheader("📋 Data Table")
            st.dataframe(hist)

            # -----------------------------
            # Extra (A+ Feature)
            # -----------------------------
            st.subheader("📈 Moving Average (Extra Feature)")

            hist['MA_5'] = hist['Close'].rolling(5).mean()
            hist['MA_10'] = hist['Close'].rolling(10).mean()

            st.line_chart(hist[['Close', 'MA_5', 'MA_10']])

    except Exception as e:
        st.error("⚠️ Something went wrong")
        