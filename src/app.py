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
import matplotlib.ticker as ticker

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
   
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=startDate, end_date=endDate)
    startDate = early.index[0]
    endDate = early.index[-1]
    dca_dates = list(early[::freq].index)
    #dca_dates = investment_dates_all = pd.bdate_range(start = startDate, end = endDate, freq = str(freq)+"B") #tracks the days when regular investment is made
    
    current_value = initial_investment*price_ratio_loaded(dataset, startDate, startDate, dayprice) 
    invested = initial_investment
    previous_date = startDate
    history_dict = {'Dates':startDate,'Invested':initial_investment,'Portfolio Value':current_value}
    dict_list.append(history_dict)
    
    for date in dca_dates[1:]:
        #add to the sum to track both current and at the end values of the portfolio
        current_value = current_value*price_ratio_loaded(dataset, startDate = previous_date, endDate = date, dayprice = dayprice) + regular_invest 
        invested += regular_invest
        #log invested, portfolio_value
        tmp_dict = {'Dates':date,'Invested':invested,'Portfolio Value':current_value}
        dict_list.append(tmp_dict)
        previous_date = date   
    current_value = current_value*price_ratio_loaded(dataset, startDate = date, endDate = endDate, dayprice = dayprice)
    tmp_dict = {'Dates':endDate,'Invested':invested,'Portfolio Value':current_value}
    dict_list.append(tmp_dict)
    return pd.DataFrame(dict_list)  

@st.cache 
def read_data(file):
    data = pd.read_csv(file,parse_dates=['date'])
    data['date'] = data['date'].dt.tz_convert(None)
    data = data.set_index('date')
    return data



st.title('Day Trading vs Buy-and-Hold')
'''
### What kind of return could you get by following traditional dollar cost averaging strategy? Typical mom-and-pop investor start with certain amount of money and are allocating certain amount of their salary bi-weekly or monthly to their investment account. 
'''
'''
You can choose among 3 asset classes (data pulled using tiingo API):
    
1. An ETF that tracks the S&P500 index
2. An ETF that tracks the US 10-year T-bonds
3. An ETF that tracks physical Gold


Choose the asset class, initial invesment, frequency (bi-weekly or monthly) and size of regular contribution, start and end date of the investigation period.   
'''

image = Image.open('./TradingvsInvesting.jpg')
st.sidebar.image(image, caption='', use_column_width=True)
#frequency = st.selectbox(label = "")

st.sidebar.header('Explore different trading strategies')
st.sidebar.subheader('Choose the option to visualize')

dca = st.sidebar.checkbox('Dollar Cost Averaging Calculator', value = True)

daily_trading = st.sidebar.checkbox('Daily Trading', value = False)



asset_class_selection = st.selectbox(label = 'Select Asset Class', 
						   options = ['S&P500 ETF (SPY)',
						    		  'Vanguard Long-Term Treasury Index Fund ETF (VGLT)',
						    		  'Physical Gold ETF (GLD)'])

if asset_class_selection == 'S&P500 ETF (SPY)':
	asset_class = 'SPY'
elif asset_class_selection == 'Vanguard Long-Term Treasury Index Fund ETF (VGLT)':
	asset_class = 'VGLT'
else:
	asset_class = 'GLD'	


initial_investment = st.slider('Select the size of the initial_investment', min_value = 1000, max_value = 100000, value = 10000)

contribution_selection = st.selectbox(label = 'Frequency of Contributions', 
						   options = ['Weekly','Bi-weekly',
						    		  'Monthly'])

if contribution_selection == 'Weekly':
	invest_freq = 5
elif contribution_selection == 'Bi-weekly':
	invest_freq = 10
else:
	invest_freq = 25

freq_investment = st.slider('Select the size of the regular contribution', min_value = 10, max_value = 5000, value = 1000)


startDate = st.date_input(label = "Investing Start Date", 
	min_value = datetime.datetime(2000,1,1), 
	max_value = datetime.datetime(2021,2,10),
	value = datetime.datetime(2014,7,10))

endDate = st.date_input(label = "Investment End Date", 
	min_value = datetime.datetime(2000,1,1), 
	max_value = datetime.datetime(2021,2,10),
	value = datetime.datetime(2020,12,10))



df_data = read_data(f'./data/raw/{asset_class}_flattened.csv')
df = dollar_cost_average_loaded(df_data, startDate=startDate, endDate=endDate, 
								initial_investment = initial_investment, regular_invest = freq_investment, 
								freq = invest_freq, dayprice = 'open')
df = df.set_index('Dates')
df['Percent Return'] = 100*(df['Portfolio Value'] - df['Invested'])/(df['Invested'] + 0.001)

fig, (ax1, ax2) = plt.subplots(2)
#ax = df.plot(subplots = True, grid = True)
sns.set_style("whitegrid")
fig.set_size_inches(20,18)

ax1.plot(df['Percent Return'], color ='black')
#tick = ticker.StrMethodFormatter('${x:,.0f}')
#ax1.yaxis.set_major_formatter(tick) 
# Labels
ax1.set_title('Dollar Cost Averaging Return', size=18)
ax1.set_ylabel('Percent Return (%)', size=14)
ax1.set_xlabel('Date', size=14)

ax2.plot(df['Portfolio Value'], color ='orange')
ax2.plot(df['Invested'], color ='green')
tick = ticker.StrMethodFormatter('${x:,.0f}')
ax2.yaxis.set_major_formatter(tick) 
# Labels
ax2.set_title('Amount Invested vs Portfolio Value', size=18)
ax2.set_ylabel('Amount ($)', size=14)
ax2.set_xlabel('Date', size=14)
ax2.legend(['Portfolio Value',"Amount Invested"], fontsize=18)

st.pyplot(plt)
#$st.write("Annulaized Rate of Return =", (1 + df['Percent Return'][-1]/100, 365/(df.index[-1] - df.index[0]).days)
st.write("Annualized Rate of Return (in %) =", ((1+df['Percent Return'][-1]/100)**(365/(df.index[-1] - df.index[0]).days) - 1)*100)