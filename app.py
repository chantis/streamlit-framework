import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("S&P500 Stocks")
# Get S&P500 stock tickers
stocks = pd.read_csv('/Users/chantis/Desktop/ipynb_checkpoints/SP500.csv')
stocks.head()
symbols = stocks['Symbol'].sort_values().tolist()

ticker = st.sidebar.text_input("Enter ticker (e.g., AAPL)")

# Create a drop down menu for stock stickers
# This also will define the value of ticker in subsequent code
#ticker = st.sidebar.selectbox('Choose a S&P 500 Stock', symbols)  

#Connect ticker to yfinance 
stock = yf.Ticker(ticker)
st.title(ticker)
         
# Create two radio buttons 1. "Fundamental" 2. "Technical" analysis
# The buttons are given as Tuple
infoType = st.sidebar.radio("Choose an info type",('Fundamental', 'Technical')) 

if(infoType == 'Fundamental'):
    st.write('Will build this later')
else:
    start = dt.datetime.today()-dt.timedelta(2 * 365)
    end = dt.datetime.today()
    df = yf.download(ticker,start,end)
    df = df.reset_index()
         
    fig = go.Figure(
            data=go.Scatter(x=df['Date'], y=df['Adj Close'])
            )

    fig.update_layout(
        title={
            'text': "Stock Prices Over Past Two Years",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
          
    st.plotly_chart(fig, use_container_width=True)
