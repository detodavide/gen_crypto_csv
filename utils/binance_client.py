from binance import Client
import pandas as pd
import json
import streamlit as st

def bin_client():
    apikey = st.secrets['apikey']
    secret = st.secrets['apiprivate']
    client = Client(api_key=apikey, api_secret=secret)
    return client

def main():
    pass


if __name__ == '__main__':
    main()