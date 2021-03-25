import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

st.title("AC TDI 12-day Program Milestone")

# Get the stock ticker from the user 
ticker = st.sidebar.text_input("Enter ticker (e.g., AAPL)","A")

# Create a pull down menu for the years
years = ['2021', '2020', '2019', '2018', '2017', 
         '2016', '2015', '2014', '2013', '2012',
         '2011', '2020']
year = int(st.sidebar.selectbox('Choose a year', years))

# Create a pull down menu for the months
months = ["January","February","March",
         "April","May","June",
         "July","August","September",
         "October","November","December"]

monthdict = {"January":1,"February":2,"March":3,
         "April":4,"May":5,"June":6,
         "July":6,"August":8,"September":9,
         "October":10,"November":11,"December":12}

monthstr = st.sidebar.selectbox('Choose a month', months)


month = monthdict[monthstr]
         
mr = calendar.monthrange(year, month)
start = dt.datetime(year,month,1)
end = dt.datetime(year,month,mr[1])
if end >  dt.datetime.today():
    end = dt.datetime.today()
if start >  dt.datetime.today():
    start = dt.datetime.today()-dt.timedelta(365)
    st.write("Since you chose a future month, we show data for the last 365 days")
    st.write("But we certainly wish we could show you future prices!")

#start = dt.datetime.today()-dt.timedelta(2 * 365)
#end = dt.datetime.today()

df = yf.download(ticker,start,end)

if df.empty:
    st.write(ticker+": No data found, symbol may be delisted")
        
df = df.reset_index()
         
fig = go.Figure(
            data=go.Scatter(x=df['Date'], y=df['Adj Close'])
               )

fig.update_layout(
        title={
        'text': ticker+" Prices For "+monthstr+", "+str(year),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
          
st.plotly_chart(fig, use_container_width=True)

# Get finviz news for this ticker
finwiz_url = 'https://finviz.com/quote.ashx?t='
url = finwiz_url + ticker
st.write(url)

req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
response = urlopen(req)  

# Read the contents of the file into 'html'
html = BeautifulSoup(response)

# Find 'news-table' in the Soup and load it into 'news_table'
news_table = html.find(id='news-table')
hlinks = []
for i,link in enumerate(news_table.find_all('a')):
#    print(link.get('href'))
    hlinks.append(link.get('href'))
    if i == 11:
        break
# Get all the table rows tagged in HTML with <tr> into 'amzn_tr'
table_tr = news_table.findAll('tr')
for i, table_row in enumerate(table_tr):
    # Read the text of the element 'a' into 'link_text'
    a_text = table_row.a.text
    # Read the text of the element 'td' into 'data_text'
    td_text = table_row.td.text
    # Print the contents of 'link_text' and 'data_text' 
#    print(a_hlinks)
    st.write(hlinks[i])
    st.write(a_text)
    st.write(td_text)
    # Exit after printing 10 rows of data
    if i == 11:
        break
