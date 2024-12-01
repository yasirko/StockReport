import streamlit as st
import yfinance as yf

# Set up the Streamlit app
st.title('Ticker Information from Yahoo Finance')

# Input for the stock ticker
ticker_symbol = st.text_input('Enter Stock Ticker Symbol (e.g., 4072.SA):', '4072.SA')

if ticker_symbol:
    # Fetch the ticker data
    ticker = yf.Ticker(ticker_symbol)

    # Get general info
    info = ticker.info

    # Profile section
    st.subheader("Profile")
    industry = info.get('industry', 'N/A')
    sector = info.get('sector', 'N/A')
    exchange = info.get('exchange', 'N/A')
    market_cap = info.get('marketCap', 'N/A') / 1e6  # Convert to million
    float_shares = info.get('floatShares', 'N/A') / 1e6  # Convert to million

    st.write(f"**Industry:** {industry}")
    st.write(f"**Sector:** {sector}")
    st.write(f"**Exchange:** {exchange}")
    st.write(f"**Capitalization:** {market_cap:.2f} mln")
    st.write(f"**Float:** {float_shares:.2f} mln")

    # Quote section
    st.subheader("Quote as of 11/28/2024")
    last_price = info.get('currentPrice', 'N/A')
    change = info.get('regularMarketChange', 'N/A')
    open_price = info.get('regularMarketOpen', 'N/A')
    low_price = info.get('regularMarketDayLow', 'N/A')
    high_price = info.get('regularMarketDayHigh', 'N/A')
    volume = info.get('volume', 'N/A')
    dollar_volume = volume * last_price if volume and last_price else 'N/A'
    avg_volume = info.get('averageVolume', 'N/A')

    st.write(f"**Last:** {last_price}")
    st.write(f"**Change:** {change} ({(change / last_price * 100):.2f}%)")
    st.write(f"**Open:** {open_price}")
    st.write(f"**Low:** {low_price}")
    st.write(f"**High:** {high_price}")
    st.write(f"**Volume:** {volume}")
    st.write(f"**$ Volume:** {dollar_volume}")
    st.write(f"**Avg Volume:** {avg_volume}")

    # Technical Indicators
    st.subheader("Technicals")

    # Fetching historical data for technical indicators
    try:
        hist = ticker.history(period='1y')

        # Moving Averages
        ma_7 = hist['Close'].rolling(window=7).mean().iloc[-1]
        ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        ma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
        
        st.write(f"**MA(7):** {ma_7:.2f}")
        st.write(f"**MA(50):** {ma_50:.2f}")
        st.write(f"**MA(200):** {ma_200:.2f}")

        # RSI (Relative Strength Index)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi_14 = 100 - (100 / (1 + rs))
        rsi_3 = rsi_14.iloc[-3]  # Approximation for 3 days
        rsi_7 = rsi_14.iloc[-7]  # Approximation for 7 days
        
        st.write(f"**RSI(3):** {rsi_3:.2f}")
        st.write(f"**RSI(7):** {rsi_7:.2f}")
        st.write(f"**RSI(14):** {rsi_14.iloc[-1]:.2f}")

        # CCI (Commodity Channel Index)
        typical_price = (hist['Close'] + hist['High'] + hist['Low']) / 3
        sma_typical_price = typical_price.rolling(window=14).mean()
        mean_deviation = (typical_price - sma_typical_price).abs().rolling(window=14).mean()
        cci_14 = (typical_price - sma_typical_price) / (0.015 * mean_deviation)
        st.write(f"**CCI(14):** {cci_14.iloc[-1]:.2f}")

        # ADX (Average Directional Index)
        adx_14 = "N/A"  # Placeholder for ADX calculation
        st.write(f"**ADX(14):** {adx_14}")

        # Momentum (MOM)
        mom_14 = hist['Close'].diff(periods=14).iloc[-1]
        st.write(f"**MOM(14):** {mom_14:.2f}")

        # Williams %R
        highest_high = hist['High'].rolling(window=14).max()
        lowest_low = hist['Low'].rolling(window=14).min()
        wr_14 = -100 * (highest_high - hist['Close']) / (highest_high - lowest_low)
        st.write(f"**W%R(14):** {wr_14.iloc[-1]:.2f}")

        # ATR (Average True Range)
        high_low = hist['High'] - hist['Low']
        high_prev_close = (hist['High'] - hist['Close'].shift(1)).abs()
        low_prev_close = (hist['Low'] - hist['Close'].shift(1)).abs()
        tr = high_low.combine(high_prev_close, max).combine(low_prev_close, max)
        atr_14 = tr.rolling(window=14).mean().iloc[-1]
        st.write(f"**ATR(14):** {atr_14:.2f}")

    except Exception as e:
        st.error(f"Error fetching technical indicators: {e}")

    # Relative Strength
    st.subheader("Relative Strength")
    
    # Calculating Relative Strength over different periods
    relative_strength = {
        "1-Week": (hist['Close'].iloc[-1] - hist['Close'].iloc[-6]) / hist['Close'].iloc[-6] * 100,
        "2-Week": (hist['Close'].iloc[-1] - hist['Close'].iloc[-13]) / hist['Close'].iloc[-13] * 100,
        "1-Month": (hist['Close'].iloc[-1] - hist['Close'].iloc[-22]) / hist['Close'].iloc[-22] * 100,
        "3-Month": (hist['Close'].iloc[-1] - hist['Close'].iloc[-66]) / hist['Close'].iloc[-66] * 100,
        "6-Month": (hist['Close'].iloc[-1] - hist['Close'].iloc[-132]) / hist['Close'].iloc[-132] * 100,
    }
    
    for period, value in relative_strength.items():
        st.write(f"**{period}:** {value:.2f}%")

    # Price Performance
    st.subheader("Price Performance")
    
    price_performance = {
        "1-Week": (hist['Close'].iloc[-1] - hist['Close'].iloc[-6]) / hist['Close'].iloc[-6] * 100,
        "1-Month": (hist['Close'].iloc[-1] - hist['Close'].iloc[-22]) / hist['Close'].iloc[-22] * 100,
        "3-Month": (hist['Close'].iloc[-1] - hist['Close'].iloc[-66]) / hist['Close'].iloc[-66] * 100,
        "6-Month": (hist['Close'].iloc[-1] - hist['Close'].iloc[-132]) / hist['Close'].iloc[-132] * 100,
    }
    
    for period, value in price_performance.items():
        st.write(f"**{period}:** {value:.2f}%")

    # Display historical price data
    st.subheader("Price Performance Chart")
    st.line_chart(hist['Close'])
