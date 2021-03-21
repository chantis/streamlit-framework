import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("AC TDI 12-day Program Milestone")

# Get the stock ticker from the user 
ticker = st.sidebar.text_input("Enter ticker (e.g., AAPL)")
         
# Create two radio buttons 1. "Fundamental" 2. "Technical" analysis

infoType = st.sidebar.radio("Choose an info type",('Fundamental', 'Technical')) 

if(infoType == 'Fundamental'):
    st.write('Will build this later')
else:
    start = dt.datetime.today()-dt.timedelta(2 * 365)
    end = dt.datetime.today()
    df = yf.download(ticker,start,end)
    if df.empty:
        st.write(ticker+": No data found, symbol may be delisted")
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
