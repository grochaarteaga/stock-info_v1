import json
import requests
import streamlit as st

# Streamlit app title
st.title("Stock Information App")

# Input field for stock symbols (comma-separated)
stock_symbols_input = st.text_input("Enter Stock Symbols (comma-separated, e.g., NVDA, AAPL, MSFT):")

# Split the input into individual stock symbols
stock_symbols = [symbol.strip() for symbol in stock_symbols_input.split(',') if symbol.strip()]

# Check if any stock symbols were entered
if stock_symbols:
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

    headers = {
        "X-RapidAPI-Key": "664e022805msha8134355088f8cfp1248e7jsn172fa95bde2e",
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    for stock_symbol in stock_symbols:
        querystring = {"symbol": stock_symbol, "region": "US"}

        response = requests.get(url, headers=headers, params=querystring)

        # Display stock information in a separate section for each stock
        st.header(f"Stock Information for {stock_symbol}")

        if response.status_code == 200:
            # Parse the JSON content from the response
            json_response = response.json()

            # Access and display financial data
            regular_market_previous_close = json_response.get("financialData", {}).get("currentPrice", {}).get("raw")
            st.write(f"Stock price: {regular_market_previous_close}")

            trailing_PE = json_response.get("summaryDetail", {}).get("trailingPE", {}).get("raw")
            st.write(f"PE ratio: {trailing_PE}")

            net_income = json_response.get("defaultKeyStatistics", {}).get("netIncomeToCommon", {}).get("raw")
            st.write(f"Net Income: {net_income}")

            revenue = json_response.get("financialData", {}).get("totalRevenue", {}).get("raw")
            st.write(f"Revenue: {revenue}")

            if revenue != 0:
                roic = (int(net_income) / int(revenue)) * 100  # Calculate ROIC as a percentage
                st.write(
                    f"Return on Invested Capital (ROIC): {roic:.2f}%")  # Display with 2 decimal places
            else:
                st.write("Revenue is zero. Cannot calculate ROIC.")
        else:
            st.write(f"Error: Unable to retrieve data for {stock_symbol}")
