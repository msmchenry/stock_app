import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

@st.cache_data
def fetch_data(ticker):
    stock_data = yf.Ticker(ticker)
    return stock_data.history(period="1y")["Close"]

st.title('Stock Price Ratio Visualization')

primary_ticker = st.text_input('Enter the primary stock ticker:')
comparison_tickers_input = st.text_input('Enter comparison stock tickers (comma separated):')
comparison_tickers = comparison_tickers_input.split(',')

if primary_ticker and comparison_tickers_input:
    primary_data = fetch_data(primary_ticker)

    fig = px.line(title=f'Normalized Price Ratio: {primary_ticker} vs Comparison Stocks')

    for comparison_ticker in comparison_tickers:
        comparison_ticker = comparison_ticker.strip()
        comparison_data = fetch_data(comparison_ticker)
        ratio_data = primary_data / comparison_data
        normalized_ratio = ratio_data / ratio_data.iloc[0] # Normalize the ratio

        fig.add_scatter(x=normalized_ratio.index, y=normalized_ratio, mode='lines', name=comparison_ticker)

    st.plotly_chart(fig)
else:
    st.warning('Please enter the primary stock ticker and at least one comparison ticker.')
