import streamlit as st
import yfinance as yf

# Set up the Streamlit app
st.title('Ticker Information from Yahoo Finance')

# Input for the stock ticker
ticker_symbol = st.text_input('Enter Stock Ticker Symbol (e.g., 4072.SA):', '4072.SA')

if ticker_symbol:
    # Fetch the ticker data
    ticker = yf.Ticker(ticker_symbol)

    # Get current stock info
    info = ticker.info
    last_price = info.get('currentPrice', 'N/A')
    change = info.get('regularMarketChange', 'N/A')
    market_cap = info.get('marketCap', 'N/A')
    
    # Display current price
    st.subheader('MBC Group Co')
    st.write(f"**Last Price:** {last_price}")
    st.write(f"**Change:** {change}")

    # Technical Indicators
    st.subheader("Technicals")
    
    # Fetch historical market data for technical indicators
    hist = ticker.history(period='1y')
    if len(hist) > 0:
        ma_7 = hist['Close'].rolling(window=7).mean().iloc[-1]
        ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        ma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
        
        # Display technical values
        st.write(f"**MA(7):** {ma_7:.2f}")
        st.write(f"**MA(50):** {ma_50:.2f}")
        st.write(f"**MA(200):** {ma_200:.2f}")

        # RSI and other indicators can be calculated similarly
        # For simplicity, let's just show MA values here

    # Financial Ratios
    st.subheader("Fundamentals")
    ebitda = info.get('ebitda', 'N/A')
    ev_ebitda = info.get('enterpriseToEbitda', 'N/A')
    
    # Display fundamentals
    st.write(f"**EBITDA:** {ebitda}")
    st.write(f"**EV / EBITDA:** {ev_ebitda}")
    
    # Financial Ratios
    st.subheader("Financial Ratios")
    current_ratio = info.get('currentRatio', 'N/A')
    price_book_ratio = info.get('priceToBook', 'N/A')
    debt_equity_ratio = info.get('debtToEquity', 'N/A')
    
    st.write(f"**Current Ratio:** {current_ratio}")
    st.write(f"**Price/Book Ratio:** {price_book_ratio}")
    st.write(f"**Debt/Equity Ratio:** {debt_equity_ratio}")

    # Dividends
    st.subheader("Dividends")
    dividends = info.get('dividendYield', 'N/A')
    st.write(f"**DPS:** {dividends}")

    # Display historical price data
    st.subheader("Price Performance")
    st.line_chart(hist['Close'])
