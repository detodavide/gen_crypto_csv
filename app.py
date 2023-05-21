import streamlit as st
import pandas as pd

from pagine.full_csv import main as gen_csv
from pagine.prophet_csv import main as prophet_csv
from utils.bg_image import add_bg_from_url
from utils.binance_client import bin_client
from binance import Client
import mplfinance as mpf

def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    add_bg_from_url()

    st.subheader("Generate a csv from Binance")

    client = bin_client()
    client.API_URL = "https://data.binance.us/api"
    tickers = client.get_all_tickers()
    search_ticker = st.text_input("Search for a ticker: ")

    if search_ticker:

        for ticker in tickers:
            ticker_symbol = ticker.get("symbol")
            if ticker_symbol == search_ticker:
                st.table(ticker)
                break
        
        st.write("Interval 1 Day, from Jan 2020 to today")
        historical = client.get_historical_klines(ticker_symbol, Client.KLINE_INTERVAL_1DAY, '1 Jan 2020')
        hist_df = pd.DataFrame(historical)
        hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                    'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
        hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit='s')
        hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit='s')
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
        hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)
        hist_df.set_index('Close Time')

        plot = mpf.plot(hist_df.set_index('Close Time').tail(120), 
                        type='candle', style='charles', 
                        volume=True, 
                        title=f'{ticker_symbol} Last 120 Days', 
                        mav=(10,20,30))
        st.pyplot(plot)

        st.subheader("Select the type of file to download")

        options = ['FULL CSV FILE', 'PROPHET READY FILE']
        selected_option = st.selectbox('Select an option: ', options)
    

        if selected_option == "FULL CSV FILE":
            gen_csv(hist_df)

        if selected_option == "PROPHET READY FILE":
            prophet_csv(hist_df)
        
    


if __name__ == '__main__':
    
    main()