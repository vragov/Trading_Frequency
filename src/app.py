import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
from matplotlib.ticker import FixedLocator
import math
import streamlit as st
from matplotlib.pyplot import rc
import datetime
import pandas_market_calendars as mcal
from PIL import Image
import seaborn as sns

def price_diff_loaded(dataset, startDate, endDate, dayprice = 'open'):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates the absolute price change (in $)
    '''
    price_diff = dataset.loc[endDate,dayprice] - dataset.loc[startDate,dayprice]
    return price_diff

def price_ratio_loaded(dataset, startDate, endDate, dayprice = 'open'):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates the relative price change
    '''
    price_ratio = dataset.loc[endDate,dayprice]/dataset.loc[startDate,dayprice]        
    return price_ratio

def dollar_cost_average_loaded(dataset, startDate, endDate, initial_investment = 0, regular_invest = 1000, freq = 10, dayprice = 'open'):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates final value of the portfolio as a result of the dollar cost averaging
    '''
 
    dict_list = []
   
    invested = [] #tracks amount of invested capital up to this point
    portfolio_value = [] #track protfolio value
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=startDate, end_date=endDate)
    startDate = early.index[0]
    endDate = early.index[-1]
    dca_dates = list(early[::freq].index)
    #dca_dates = investment_dates_all = pd.bdate_range(start = startDate, end = endDate, freq = str(freq)+"B") #tracks the days when regular investment is made
    
    current_value = initial_investment*price_ratio_loaded(dataset, startDate, startDate, dayprice) 
    invested = initial_investment
    previous_date = startDate
    history_dict = {'dates':startDate,'invested':initial_investment,'Portfolio Value':current_value}
    dict_list.append(history_dict)
    
    for date in dca_dates[1:]:
        #add to the sum to track both current and at the end values of the portfolio
        current_value = current_value*price_ratio_loaded(dataset, startDate = previous_date, endDate = date, dayprice = dayprice) + regular_invest 
        invested += regular_invest
        #log invested, portfolio_value
        tmp_dict = {'dates':date,'invested':invested,'Portfolio Value':current_value}
        dict_list.append(tmp_dict)
        previous_date = date   
    current_value = current_value*price_ratio_loaded(dataset, startDate = date, endDate = endDate, dayprice = dayprice)
    tmp_dict = {'dates':endDate,'invested':invested,'Portfolio Value':current_value}
    dict_list.append(tmp_dict)
    return pd.DataFrame(dict_list)  

@st.cache 
def read_data(file):
    data = pd.read_csv(file,parse_dates=['date'])
    data['date'] = data['date'].dt.tz_convert(None)
    data = data.set_index('date')
    return data



st.title('Trading Frequency Exploration')

asset_class_selection = st.selectbox(label = 'Select Asset Class', 
						   options = ['S&P500 ETF (SPY)',
						    		  'Vanguard Long-Term Treasury Index Fund ETF (VGLT)'])
if asset_class_selection == 'S&P500 ETF (SPY)':
	asset_class = 'SPY'
else:
	asset_class = 'VGLT'	

image = Image.open('./TradingvsInvesting.jpg')
st.sidebar.image(image, caption='', use_column_width=True)
#frequency = st.selectbox(label = "")

startDate = st.date_input(label = "Start Date", 
	min_value = datetime.datetime(2000,1,1), 
	max_value = datetime.datetime(2021,2,10),
	value = datetime.datetime(2018,7,10))

endDate = st.date_input(label = "End Date", 
	min_value = datetime.datetime(2000,1,1), 
	max_value = datetime.datetime(2021,2,10),
	value = datetime.datetime(2020,12,10))



df_data = read_data(f'./data/raw/{asset_class}_flattened.csv')
df = dollar_cost_average_loaded(df_data, startDate=startDate, endDate=endDate)
df = df.set_index('dates')
df['Percent Return'] = 100*(df['Portfolio Value'] - df['invested'])/(df['invested'] + 1)

fig, ax = plt.subplots()
#ax = df.plot(subplots = True, grid = True)
sns.set_style("whitegrid")
fig.set_size_inches(15,7)

ax.plot(df['Percent Return'], color ='black')
# Set Y axis format 
#ax.yaxis.set_major_formatter(tick) 
# Labels
ax.set_title('Dollar Cost Averaging Return', size=18)
ax.set_ylabel('Percent Return (%)', size=14)
ax.set_xlabel('Date', size=14)
# Show with Legend
plt.legend()

st.pyplot(plt)